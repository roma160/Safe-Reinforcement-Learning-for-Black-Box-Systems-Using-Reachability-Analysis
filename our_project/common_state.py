import pickle
from dataclasses import dataclass

@dataclass
class DonkeyState:
	x: float
	y: float
	angle: float
	
	def __bytes__(self) -> bytes:
		return pickle.dumps(self)
	
	def load(bytes: bytes) -> 'DonkeyState':
		return pickle.loads(bytes)

	def __repr__(self) -> str:
		return f"({self.x}, {self.y}, {self.angle})"