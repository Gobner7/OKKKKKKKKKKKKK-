from pydantic import BaseModel, Field
from typing import Optional


class BotConfig(BaseModel):
	budget_usd: float = Field(ge=0.0, default=50.0)
	max_open_positions: int = 5
	dry_run: bool = True
	csfloat_base_url: str = "https://csfloat.com"
	user_agent: Optional[str] = None
	headless: bool = True
	purchase_spread_min: float = 0.05
	target_roi_min: float = 0.03
	relist_markup: float = 0.04
	max_hold_hours: int = 72

from pydantic import BaseModel, Field
from typing import Optional

class BotConfig(BaseModel):
	budget_usd: float = Field(ge=0.0, default=50.0)
	max_open_positions: int = 5
	dry_run: bool = True
	csfloat_base_url: str = "https://csfloat.com"
	user_agent: Optional[str] = None
	headless: bool = True
	purchase_spread_min: float = 0.05
	target_roi_min: float = 0.03
	relist_markup: float = 0.04
	max_hold_hours: int = 72
