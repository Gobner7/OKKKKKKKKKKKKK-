from __future__ import annotations
from typing import Optional
from .models import Listing, Opportunity


class PriceEstimator:
	def __init__(self):
		pass

	def estimate_fmv(self, listing: Listing) -> tuple[float, float]:
		# Placeholder heuristic: assumes FMV equals listing price initially.
		return listing.price_usd, 0.5


class OpportunityFinder:
	def __init__(self, min_spread: float = 0.05, min_roi: float = 0.03):
		self.min_spread = min_spread
		self.min_roi = min_roi

	def evaluate(self, listing: Listing, estimator: PriceEstimator) -> Optional[Opportunity]:
		fmv, confidence = estimator.estimate_fmv(listing)
		if fmv <= 0:
			return None
		roi = (fmv - listing.price_usd) / listing.price_usd
		if roi < self.min_roi:
			return None
		return Opportunity(listing=listing, estimated_fmv_usd=fmv, expected_roi=roi, confidence=confidence)

