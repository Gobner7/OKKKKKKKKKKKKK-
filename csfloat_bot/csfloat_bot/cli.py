from __future__ import annotations
import asyncio
from typing import List
from loguru import logger
from typer import Typer, Option
from pathlib import Path
from datetime import datetime, timedelta

from .config import BotConfig
from .storage import CookieStore
from .csfloat_client import CSFloatWebClient
from .models import Listing
from .pricing import PriceEstimator, OpportunityFinder
from .risk import BudgetManager, Position
from .strategy import ThompsonBandit, categorize_listing, score_opportunity
from .features import extract_features
from .bandit import LinUCB


app = Typer()


@app.command()
def run(
	dry_run: bool = Option(True, help="Run without buying"),
	budget: float = Option(50.0, help="USD budget"),
	headless: bool = Option(True),
	cookie_file: str = Option(str(Path.home() / ".csfloat/cookies.json")),
	cycles: int = Option(1, help="Number of scan cycles"),
	scan_limit: int = Option(25, help="Listings to inspect per cycle"),
):
	config = BotConfig(dry_run=dry_run, budget_usd=budget, headless=headless)
	cookie_store = CookieStore(Path(cookie_file))

	async def main():
		async with CSFloatWebClient(
			config.csfloat_base_url,
			cookie_store,
			headless=config.headless,
			user_agent=config.user_agent,
		) as client:
			await client.ensure_logged_in()

			budget_mgr = BudgetManager(total_budget_usd=config.budget_usd, max_open_positions=config.max_open_positions)
			bandit_simple = ThompsonBandit()
			linucb = LinUCB(alpha=0.6, dim=8, state_path=Path.home() / ".csfloat/linucb.json")
			estimator = PriceEstimator(get_comps=lambda q: client.fetch_comparable_prices(q, limit=40))
			finder = OpportunityFinder(min_spread=config.purchase_spread_min, min_roi=config.target_roi_min)

			for _ in range(max(1, cycles)):
				raw = await client.fetch_latest_listings(limit=scan_limit)
				listings: List[Listing] = []
				for r in raw:
					if not r:
						continue
					listings.append(
						Listing(
							id=r.get("url", ""),
							title=r.get("title", ""),
							price_usd=r.get("price", 0.0),
							float_value=None,
							stickers=[],
							url=r.get("url", ""),
						)
					)

				scored: list[tuple[float, Listing]] = []
				for listing in listings:
					opp = await finder.evaluate(listing, estimator)
					if not opp:
						continue
					arm = categorize_listing(listing)
					arm_score = bandit_simple.sample(arm)
					feat = extract_features(listing)
					feat_keys = ["bias","price","log_price","is_knife","is_glove","is_popular","has_sticker","float"]
					ctx_score = linucb.score(feat, feat_keys)
					s = score_opportunity(opp, arm_score) * (0.5 + 0.5 * max(0.0, min(1.0, ctx_score)))
					scored.append((s, listing))

				scored.sort(reverse=True, key=lambda x: x[0])
				for score, listing in scored[:5]:
					if not budget_mgr.can_open(listing.price_usd):
						continue
					# Kelly sizing proxy: fraction = clamp(expected_roi / variance)
					fraction = max(0.05, min(0.5, max(0.0, score)))
					allocation = min(budget_mgr.available_usd, listing.price_usd * fraction)
					if allocation < listing.price_usd:
						continue
					target_price = listing.price_usd * (1.0 + config.relist_markup)
					pos = Position(
						id=listing.id,
						listing_id=listing.id,
						purchase_price_usd=listing.price_usd,
						target_price_usd=target_price,
						opened_at=datetime.utcnow(),
						expire_at=datetime.utcnow() + timedelta(hours=config.max_hold_hours),
						meta={"title": listing.title},
					)
					if not budget_mgr.reserve(pos):
						continue
					logger.info(f"Selected: {listing.title} ${listing.price_usd:.2f} score={score:.3f}")
					if not config.dry_run:
						ok = await client.attempt_purchase(listing.url)
						logger.info(f"Purchase attempted: {ok}")
					# Update bandits with pseudo-reward = score clipped to [0,1]
					arm = categorize_listing(listing)
					reward = max(0.0, min(1.0, score))
					bandit_simple.update(arm, reward)
					linucb.update(feat, reward, feat_keys)

	asyncio.run(main())


if __name__ == "__main__":
	app()

