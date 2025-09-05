from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, Optional, List


@dataclass
class Position:
	id: str
	listing_id: str
	purchase_price_usd: float
	target_price_usd: float
	opened_at: datetime
	expire_at: datetime
	meta: dict = field(default_factory=dict)


class BudgetManager:
	def __init__(self, total_budget_usd: float, max_open_positions: int):
		self.total_budget_usd = float(total_budget_usd)
		self.max_open_positions = int(max_open_positions)
		self._reserved_usd: float = 0.0
		self._positions: Dict[str, Position] = {}

	@property
	def available_usd(self) -> float:
		return max(0.0, self.total_budget_usd - self._reserved_usd)

	@property
	def open_count(self) -> int:
		return len(self._positions)

	def can_open(self, cost_usd: float) -> bool:
		if self.open_count >= self.max_open_positions:
			return False
		return self.available_usd >= cost_usd

	def reserve(self, position: Position) -> bool:
		if not self.can_open(position.purchase_price_usd):
			return False
		self._reserved_usd += position.purchase_price_usd
		self._positions[position.id] = position
		return True

	def release(self, position_id: str):
		pos = self._positions.pop(position_id, None)
		if pos is not None:
			self._reserved_usd = max(0.0, self._reserved_usd - pos.purchase_price_usd)

	def get_positions(self) -> List[Position]:
		return list(self._positions.values())

