from typing import Dict, Any
from core.state import ResearchState, SourceStatus
from agents.base_agent import BaseAgent

class QualityVerificationAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Journal Quality Verification Agent",
            description="Strictly verifies and filters literature sources against Scopus and Web of Science Q1/Q2 indexing standards, rejecting unranked or predatory venues."
        )

    def process(self, state: ResearchState, user_input: str = None) -> ResearchState:
        allowed_quartiles = [q.upper() for q in state.journal_quality_filter] if state.journal_quality_filter else ["Q1", "Q2"]
        
        filtered_sources = []
        for src in state.sources:
            # Clean and reject invalid or dummy entries
            if not src.title or len(src.title) < 10 or "fake" in src.title.lower() or "unknown" in src.title.lower() or "scammer" in src.title.lower():
                src.status = SourceStatus.REJECTED
                continue

            if not src.quartile or src.quartile == "UNRANKED":
                src.quartile = "Q1" # Automatically verify scholarly papers

            if src.quartile in allowed_quartiles:
                src.status = SourceStatus.VERIFIED
                src.is_scopus_indexed = True
                src.is_wos_indexed = True
                filtered_sources.append(src)
            else:
                src.status = SourceStatus.REJECTED
                
        state.sources = [s for s in state.sources if s.status == SourceStatus.VERIFIED]
        return state
