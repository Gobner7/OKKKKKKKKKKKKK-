from __future__ import annotations
from typing import Optional
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

	async def fetch_latest_listings(self, query: str = "", limit: int = 50):
		# Placeholder: navigate and attempt to read listing cards for PoC.
		await self._page.goto(f"{self.base_url}/market")
		cards = await self._page.locator('[data-testid="listing-card"]').all()
		results = []
		for card in cards[:limit]:
			try:
				title = await card.locator('.title').inner_text()
				price_text = await card.locator('.price').inner_text()
				price = float(price_text.replace('$','').replace(',',''))
				url = await card.locator('a').first.get_attribute('href')
				results.append({"title": title, "price": price, "url": url})
			except Exception:
				continue
		return results

	async def attempt_purchase(self, listing_url: str) -> bool:
		# Placeholder: navigates to listing and finds buy button (dry-run only).
		await self._page.goto(listing_url)
		buy_button = self._page.locator('button:has-text("Buy")')
		if await buy_button.count() == 0:
			return False
		logger.info(f"Found buy button at {listing_url} (dry-run only)")
		return True

