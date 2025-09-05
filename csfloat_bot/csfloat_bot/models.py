from __future__ import annotations
from dataclasses import dataclass
from typing import Optional


@dataclass
class Listing:
	id: str
	title: str
	price_usd: float
	float_value: Optional[float]
	stickers: list[str]
	url: str
	seller_reputation: Optional[float] = None
	wear: Optional[str] = None
	paint_seed: Optional[int] = None


@dataclass
class Opportunity:
	listing: Listing
	estimated_fmv_usd: float
	expected_roi: float
	confidence: float

