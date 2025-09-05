from __future__ import annotations
import json
from pathlib import Path
from typing import Dict, List
import numpy as np


class LinUCB:
	def __init__(self, alpha: float = 0.5, dim: int = 8, state_path: Path | None = None):
		self.alpha = float(alpha)
		self.dim = int(dim)
		self.A = np.eye(self.dim)
		self.b = np.zeros((self.dim, 1))
		self.state_path = state_path
		if state_path and state_path.exists():
			try:
				data = json.loads(state_path.read_text())
				self.A = np.array(data["A"]) if "A" in data else self.A
				self.b = np.array(data["b"]) if "b" in data else self.b
			except Exception:
				pass

	def _phi(self, features: Dict[str, float], keys: List[str]) -> np.ndarray:
		vec = np.zeros((self.dim, 1))
		for i, k in enumerate(keys[: self.dim]):
			vec[i, 0] = float(features.get(k, 0.0))
		return vec

	def score(self, features: Dict[str, float], keys: List[str]) -> float:
		A_inv = np.linalg.inv(self.A)
		x = self._phi(features, keys)
		theta = A_inv @ self.b
		p = float((theta.T @ x) + self.alpha * np.sqrt(x.T @ A_inv @ x))
		return p

	def update(self, features: Dict[str, float], reward: float, keys: List[str]):
		x = self._phi(features, keys)
		self.A += x @ x.T
		self.b += x * float(reward)
		self._persist()

	def _persist(self):
		if not self.state_path:
			return
		try:
			payload = {"A": self.A.tolist(), "b": self.b.tolist()}
			self.state_path.parent.mkdir(parents=True, exist_ok=True)
			self.state_path.write_text(json.dumps(payload))
		except Exception:
			pass

