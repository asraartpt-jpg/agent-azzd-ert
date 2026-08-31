from abc import ABC, abstractmethod
from typing import Any, Dict
from core.state import ResearchState

class BaseAgent(ABC):
    """
    Base class for all agents in the Research Assistant Ecosystem.
    """
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    @abstractmethod
    def process(self, state: ResearchState, user_input: str = None) -> ResearchState:
        """
        Takes the current research state and user input, performs the agent's specific role,
        and returns the updated state.
        """
        pass
