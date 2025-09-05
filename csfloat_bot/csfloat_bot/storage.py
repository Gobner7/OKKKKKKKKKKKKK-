from loguru import logger
from pathlib import Path
import json
from typing import Optional


class CookieStore:
	def __init__(self, path: Path):
		self.path = path
		self.path.parent.mkdir(parents=True, exist_ok=True)

	def save(self, cookies: list[dict]):
		self.path.write_text(json.dumps(cookies))
		logger.info(f"Saved cookies to {self.path}")

	def load(self) -> Optional[list[dict]]:
		if not self.path.exists():
			return None
		try:
			return json.loads(self.path.read_text())
		except Exception as exc:
			logger.warning(f"Failed to load cookies: {exc}")
			return None

