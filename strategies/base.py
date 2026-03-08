from abc import ABC, abstractmethod
from typing import Dict, Any, List

class BaseStrategy(ABC):
    @abstractmethod
    def decide_action(self, observation: Any, info: Dict[str, Any]) -> Dict[str, Any]:
        """Returns an action dictionary compatible with the environment."""
        pass
