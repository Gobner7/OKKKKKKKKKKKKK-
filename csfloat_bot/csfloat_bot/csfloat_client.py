from __future__ import annotations
from typing import Optional, List, Dict, Any
from playwright.async_api import async_playwright, Browser
from loguru import logger
from .storage import CookieStore


class CSFloatWebClient:
	def __init__(self, base_url: str, cookie_store: CookieStore, headless: bool = True, user_agent: Optional[str] = None):
		self.base_url = base_url.rstrip('/')
		self.cookie_store = cookie_store
		self.headless = headless
		self.user_agent = user_agent
		self._browser: Optional[Browser] = None

	async def __aenter__(self):
		self._playwright = await async_playwright().start()
		self._browser = await self._playwright.chromium.launch(headless=self.headless)
		context_args = {}
		if self.user_agent:
			context_args["user_agent"] = self.user_agent
		self._context = await self._browser.new_context(**context_args)
		cookies = self.cookie_store.load()
		if cookies:
			try:
				await self._context.add_cookies(cookies)
			except Exception as exc:
				logger.warning(f"Failed adding cookies: {exc}")
		self._page = await self._context.new_page()
		return self

	async def __aexit__(self, exc_type, exc, tb):
		try:
			cookies = await self._context.cookies()
			self.cookie_store.save(cookies)
		except Exception as e:
			logger.warning(f"Could not persist cookies: {e}")
		await self._context.close()
		await self._browser.close()
		await self._playwright.stop()

	async def ensure_logged_in(self):
		await self._page.goto(f"{self.base_url}")
		# Heuristic: if avatar/login button present -> require manual login once.
		if await self._page.locator("text=Sign In").count():
			logger.info("Please login to CSFloat in the opened browser window.")
			# Wait for URL to indicate logged-in area or disappearance of Sign In button
			await self._page.wait_for_function("() => !document.body.innerText.includes('Sign In')", timeout=600_000)
			logger.info("Detected login, proceeding.")

	async def fetch_latest_listings(self, query: str = "", limit: int = 50) -> List[Dict[str, Any]]:
		await self._page.goto(f"{self.base_url}/market")
		if query:
			search = self._page.locator('input[placeholder*="Search"], input[type="search"]')
			if await search.count():
				await search.first.fill("")
				await search.first.type(query, delay=20)
				await self._page.keyboard.press('Enter')
				await self._page.wait_for_timeout(500)

		try:
			listings = await self._page.evaluate(
				r"""
		(() => {
		  const results = [];
		  const candidates = Array.from(document.querySelectorAll('[data-testid="listing-card"], .listing-card, a[href*="/item/"]'));
		  const seen = new Set();
		  for (const el of candidates) {
		    let url = null;
		    if (el.tagName === 'A' && el.href) url = el.href;
		    const a = el.querySelector('a[href*="/item/"]');
		    if (!url && a && a.href) url = a.href;
		    if (!url) continue;
		    if (seen.has(url)) continue;
		    seen.add(url);
		    const text = el.innerText || '';
		    const m = text.match(/\$\s*([0-9]{1,3}(?:,[0-9]{3})*(?:\.[0-9]{2})?|[0-9]+(?:\.[0-9]{2})?)/);
		    if (!m) continue;
		    const price = parseFloat(m[1].replace(/,/g, ''));
		    let titleEl = el.querySelector('.title, .listing-title, [data-testid="title"]');
		    let title = titleEl ? (titleEl.textContent || '').trim() : null;
		    if (!title) {
		      const lines = text.split('\n').map(s => s.trim()).filter(Boolean);
		      title = (lines.find(s => !s.startsWith('$')) || 'Unknown').slice(0, 200);
		    }
		    results.push({ title, price, url });
		  }
		  return results;
		})()
		"""
			)
		except Exception:
			cards = await self._page.locator('[data-testid="listing-card"], .listing-card, a[href*="/item/"]').all()
			listings = []
			for card in cards:
				try:
					text = await card.inner_text()
					price_line = next((ln for ln in text.split("\n") if "$" in ln), None)
					if not price_line:
						continue
					pt = price_line.replace("$", "").strip().replace(",", "")
					price = float(pt)
					a = card.locator('a[href*="/item/"]').first
					url = await a.get_attribute('href') if await a.count() else None
					title_el = card.locator('.title, .listing-title, [data-testid="title"]').first
					title = await title_el.inner_text() if await title_el.count() else None
					if not title:
						lines = [ln.strip() for ln in text.split("\n") if ln.strip()]
						title = next((ln for ln in lines if not ln.startswith("$")), "Unknown")
					listings.append({"title": title, "price": price, "url": url})
				except Exception:
					continue

		normalized: List[Dict[str, Any]] = []
		for r in listings[:limit]:
			url: str = r.get("url", "")
			if url and url.startswith('/'):
				r["url"] = f"{self.base_url}{url}"
			normalized.append(r)
		return normalized

	async def fetch_comparable_prices(self, query: str, limit: int = 30) -> List[float]:
		await self._page.goto(f"{self.base_url}/market")
		search = self._page.locator('input[placeholder*="Search"], input[type="search"]')
		if not await search.count():
			return []
		await search.first.fill("")
		await search.first.type(query, delay=10)
		await self._page.keyboard.press('Enter')
		await self._page.wait_for_timeout(600)
		try:
			data = await self._page.evaluate(
				r"""
		(() => {
		  const prices = [];
		  const candidates = Array.from(document.querySelectorAll('[data-testid="listing-card"], .listing-card, a[href*="/item/"]'));
		  for (const el of candidates) {
		    const text = el.innerText || '';
		    const m = text.match(/\$\s*([0-9]{1,3}(?:,[0-9]{3})*(?:\.[0-9]{2})?|[0-9]+(?:\.[0-9]{2})?)/);
		    if (!m) continue;
		    prices.push(parseFloat(m[1].replace(/,/g, '')));
		  }
		  return prices;
		})()
		"""
			)
		except Exception:
			cards = await self._page.locator('[data-testid="listing-card"], .listing-card, a[href*="/item/"]').all()
			vals = []
			for card in cards:
				try:
					text = await card.inner_text()
					price_line = next((ln for ln in text.split("\n") if "$" in ln), None)
					if not price_line:
						continue
					pt = price_line.replace("$", "").strip().replace(",", "")
					vals.append(float(pt))
				except Exception:
					continue
			data = vals
		return list(map(float, data[:limit]))

	async def attempt_purchase(self, listing_url: str) -> bool:
		await self._page.goto(listing_url)
		buy = self._page.locator('button:has-text("Buy"), button:has-text("Purchase"), button:has-text("Buy Now"), [role="button"]:has-text("Buy")')
		if not await buy.count():
			await self._page.wait_for_timeout(200)
			if not await buy.count():
				return False
		await buy.first.click()
		confirm = self._page.locator('button:has-text("Confirm"), button:has-text("Pay"), button:has-text("Checkout")')
		if await confirm.count():
			await confirm.first.click()
		await self._page.wait_for_timeout(800)
		toast_success = await self._page.locator('text=Awaiting seller, text=Order placed, text=Success').count()
		if toast_success:
			return True
		error = await self._page.locator('text=Insufficient, text=Error, text=Failed').count()
		return bool(toast_success and not error)

