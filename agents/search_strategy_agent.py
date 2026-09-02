from typing import Dict, Any
from core.state import ResearchState
from agents.base_agent import BaseAgent

class SearchStrategyAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Search Strategy Agent",
            description="Placeholder description for search_strategy_agent"
        )

    def process(self, state: ResearchState, user_input: str = None) -> ResearchState:
        # To be implemented
        return state
