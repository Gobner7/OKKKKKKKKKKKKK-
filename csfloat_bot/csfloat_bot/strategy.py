from __future__ import annotations
import math
import random
from dataclasses import dataclass
from typing import Dict, Tuple, List
from .models import Listing, Opportunity


@dataclass
class ArmKey:
	category: str
	price_bucket: str


class ThompsonBandit:
	def __init__(self):
		self._alpha_beta: Dict[ArmKey, Tuple[float, float]] = {}

	def _get(self, key: ArmKey) -> Tuple[float, float]:
		return self._alpha_beta.get(key, (1.0, 1.0))

	def sample(self, key: ArmKey) -> float:
		alpha, beta = self._get(key)
		# Beta distribution sampling using Python's random.gammavariate
		x = random.gammavariate(alpha, 1.0)
		y = random.gammavariate(beta, 1.0)
		return x / (x + y)

	def update(self, key: ArmKey, reward: float):
		alpha, beta = self._get(key)
		# Map reward in [0,1] to success/failure mass
		alpha += max(0.0, reward)
		beta += max(0.0, 1.0 - reward)
		self._alpha_beta[key] = (alpha, beta)


def categorize_listing(listing: Listing) -> ArmKey:
	# Simple category based on title keywords + price bucket
	name = listing.title.lower()
	if any(k in name for k in ["knife", "karambit", "bayonet", "m9"]):
		category = "knife"
	elif any(k in name for k in ["glove", "gloves"]):
		category = "gloves"
	elif any(k in name for k in ["ak-47", "m4a1-s", "m4a4", "awp", "usp", "deagle"]):
		category = "popular"
	else:
		category = "other"

	price = listing.price_usd
	if price < 5:
		bucket = "lt5"
	elif price < 20:
		bucket = "5-20"
	elif price < 100:
		bucket = "20-100"
	else:
		bucket = "100+"

	return ArmKey(category=category, price_bucket=bucket)


def score_opportunity(opp: Opportunity, arm_score: float) -> float:
	# Combined score: ROI weighted by estimator confidence and bandit prior
	return opp.expected_roi * (0.5 + 0.5 * opp.confidence) * (0.5 + 0.5 * arm_score)

