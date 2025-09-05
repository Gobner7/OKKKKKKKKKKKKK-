from __future__ import annotations
from typing import Optional
from .models import Listing, Opportunity
import statistics


class PriceEstimator:
	def __init__(self, get_comps):
		self.get_comps = get_comps

	async def estimate_fmv(self, listing: Listing) -> tuple[float, float]:
		# Fetch comparable prices and compute robust FMV (trimmed mean)
		comps = await self.get_comps(listing.title)
		if not comps:
			return listing.price_usd, 0.4
		vals = sorted([v for v in comps if v > 0])
		if not vals:
			return listing.price_usd, 0.4
		k = max(1, int(0.1 * len(vals)))
		trimmed = vals[k:-k] if len(vals) > 2 * k else vals
		fmv = statistics.mean(trimmed)
		# Confidence grows with number of comps and tight dispersion
		spread = (max(trimmed) - min(trimmed)) / max(1e-6, fmv)
		confidence = max(0.3, min(0.95, 0.4 + 0.1 * len(trimmed) - 0.3 * spread))
		return fmv, confidence


class OpportunityFinder:
	def __init__(self, min_spread: float = 0.05, min_roi: float = 0.03):
		self.min_spread = min_spread
		self.min_roi = min_roi

	async def evaluate(self, listing: Listing, estimator: PriceEstimator) -> Optional[Opportunity]:
		fmv, confidence = await estimator.estimate_fmv(listing)
		if fmv <= 0:
			return None
		roi = (fmv - listing.price_usd) / listing.price_usd
		if roi < self.min_roi:
			return None
		return Opportunity(listing=listing, estimated_fmv_usd=fmv, expected_roi=roi, confidence=confidence)

