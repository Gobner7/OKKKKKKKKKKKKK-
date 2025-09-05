from __future__ import annotations
from typing import Dict
from .models import Listing


def extract_features(listing: Listing) -> Dict[str, float]:
	name = listing.title.lower()
	features: Dict[str, float] = {}
	features["bias"] = 1.0
	features["price"] = float(listing.price_usd)
	features["log_price"] = 0.0 if listing.price_usd <= 0 else __import__("math").log(listing.price_usd)
	features["is_knife"] = 1.0 if any(k in name for k in ["knife", "karambit", "bayonet", "m9"]) else 0.0
	features["is_glove"] = 1.0 if any(k in name for k in ["glove", "gloves"]) else 0.0
	features["is_popular"] = 1.0 if any(k in name for k in ["ak-47", "m4a1-s", "m4a4", "awp", "usp", "deagle"]) else 0.0
	features["has_sticker"] = 1.0 if listing.stickers else 0.0
	if listing.float_value is not None:
		features["float"] = float(listing.float_value)
	return features

