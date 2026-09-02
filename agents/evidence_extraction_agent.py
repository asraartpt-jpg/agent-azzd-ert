from typing import Dict, Any
from core.state import ResearchState
from agents.base_agent import BaseAgent

class EvidenceExtractionAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Evidence Extraction Agent",
            description="Placeholder description for evidence_extraction_agent"
        )

    def process(self, state: ResearchState, user_input: str = None) -> ResearchState:
        # To be implemented
        return state
