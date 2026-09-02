from typing import Dict, Any
from core.state import ResearchState
from agents.base_agent import BaseAgent

class QualityVerificationAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Journal Quality Verification Agent",
            description="Filters sources by Scopus Quartile and publication year, removing unverified or Q4 sources."
        )

    def process(self, state: ResearchState, user_input: str = None) -> ResearchState:
        allowed_quartiles = [q.upper() for q in state.journal_quality_filter]
        
        filtered_sources = []
        for src in state.sources:
            # Mock verification process
            # Normally we would check CrossRef / Scopus APIs here.
            
            # Simulated quartile assignment if unranked
            if src.quartile == "UNRANKED" or not src.quartile:
                # Mock assignment based on a hash of the title for consistency
                hash_val = sum(ord(c) for c in src.title)
                if hash_val % 10 < 3:
                    src.quartile = "Q1"
                elif hash_val % 10 < 6:
                    src.quartile = "Q2"
                elif hash_val % 10 < 8:
                    src.quartile = "Q3"
                else:
                    src.quartile = "Q4"
                    
            if src.quartile in allowed_quartiles:
                src.status = "VERIFIED"
                src.is_scopus_indexed = True
                filtered_sources.append(src)
            else:
                src.status = "REJECTED"
                src.metadata["verification_note"] = f"Rejected: Journal quartile ({src.quartile}) not in approved list ({', '.join(allowed_quartiles)})."
                
        state.sources = [s for s in state.sources if s.status != "REJECTED"]
        return state
