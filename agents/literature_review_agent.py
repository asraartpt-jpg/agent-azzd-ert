from typing import Dict, Any, List
from core.state import ResearchState, SourceStatus
from agents.base_agent import BaseAgent

class LiteratureReviewAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Literature Review Agent",
            description="Synthesizes verified literature to identify themes, contradictions, and gaps."
        )

    def process(self, state: ResearchState, user_input: str = None) -> ResearchState:
        """
        Takes VERIFIED sources from the state and generates a synthesized literature review draft.
        """
        # Filter only verified sources for the review
        verified_sources = [source for source in state.sources if source.status == SourceStatus.VERIFIED]
        
        if not verified_sources:
            state.manuscript_draft["Literature Review"] = "[Requires verified sources before synthesis can begin.]"
            return state

        # Mocking the synthesis process using LLM
        synthesis_draft = self._mock_synthesize_literature(verified_sources, state.topic)
        
        # Save the synthesized text into the manuscript draft state
        state.manuscript_draft["Literature Review"] = synthesis_draft
        
        return state

    def _mock_synthesize_literature(self, sources: list, topic: str) -> str:
        """
        Simulates an LLM call generating a thematic synthesis rather than a simple list of summaries.
        """
        journal_names = [s.journal for s in sources]
        
        draft = f"### Thematic Synthesis on {topic if topic else 'the research topic'}\n\n"
        draft += (
            "Existing studies generally indicate a positive relationship within this domain; "
            "however, findings vary considerably across contexts. While prior research has "
            "predominantly focused on localized impacts, comparatively limited evidence is available "
            "from broader empirical settings.\n\n"
        )
        
        draft += "#### Methodological Patterns and Gaps\n"
        draft += (
            "A review of high-impact literature across Q1-Q3 journals (including " + ", ".join(journal_names) + ") "
            "reveals a heavy reliance on cross-sectional survey designs. Consequently, there is a distinct "
            "theoretical gap regarding longitudinal effects and causal mechanisms, which this present study aims to address."
        )
        
        return draft
