from typing import Dict, Any
from core.state import ResearchState, SourceStatus
from agents.base_agent import BaseAgent

class CitationIntegrationAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Citation Integration Agent",
            description="Ensures all in-text citations correspond to verified references and are formatted correctly."
        )

    def process(self, state: ResearchState, user_input: str = None) -> ResearchState:
        """
        Generates the final Reference List based on VERIFIED sources and the selected citation style.
        """
        style = state.formatting_requirements.get("citation_style", "APA 7th")
        verified_sources = [s for s in state.sources if s.status == SourceStatus.VERIFIED]
        
        references_text = f"### References ({style} Format)\n\n"
        
        for idx, source in enumerate(verified_sources):
            if "APA" in style:
                # Mock APA format: Authors (Year). Title. Journal. DOI
                authors_str = ", ".join(source.authors)
                references_text += f"{authors_str} ({source.year}). {source.title}. *{source.journal}*. https://doi.org/{source.doi}\n\n"
            elif "IEEE" in style:
                # Mock IEEE format: [1] Authors, "Title," Journal, Year.
                authors_str = ", ".join(source.authors)
                references_text += f"[{idx + 1}] {authors_str}, \"{source.title},\" *{source.journal}*, {source.year}. DOI: {source.doi}\n\n"
            else: # Fallback to standard
                references_text += f"- {source.title} ({source.year}) - {source.journal}\n"
                
        state.manuscript_draft["References"] = references_text
        return state
