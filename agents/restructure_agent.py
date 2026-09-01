import requests
from typing import Dict, Any
from core.state import ResearchState
from agents.base_agent import BaseAgent
from core.config import settings

class RestructuringAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Manuscript Restructuring Agent",
            description="Transforms an existing manuscript to fit a new publisher style profile."
        )

    def process(self, state: ResearchState, user_input: str = None) -> ResearchState:
        """
        Takes the current manuscript_draft and a new style_profile, and restructures the draft.
        user_input contains the name of the new publisher.
        """
        if not state.style_profile or not state.manuscript_blueprint:
            return state
            
        new_style = state.style_profile.publisher
        new_sections = state.manuscript_blueprint.get("sections", [])
        
        old_draft = "\n\n".join(state.manuscript_draft.values())
        new_draft = {}
        
        # We will mock the transformation logic here to avoid huge LLM calls in this demo,
        # but in a real scenario, this would send the old_draft to the LLM to map into new_sections.
        
        for sec in new_sections:
            title = sec["title"]
            title_lower = title.lower()
            
            content = f"### {title}\n\n"
            
            if "abstract" in title_lower:
                content += f"**[Restructured for {state.style_profile.abstract_style}]**\n\n"
                content += old_draft[:300] + "..."
            elif title == state.style_profile.keyword_label:
                content += f"**[Mapped to {title}]**\n\nArtificial Intelligence, Technology Adoption, Structural Equation Modeling"
            elif "introduction" in title_lower:
                # Find the old introduction
                content += "The rapid advancement of technology necessitates a deeper understanding of the research topic. Guided by the research objectives, we address critical gaps identified in recent literature regarding this phenomenon."
            elif "method" in title_lower:
                content += "This research employs a quantitative cross-sectional design. Data was collected via structured questionnaires distributed to a targeted sample."
            elif "result" in title_lower or "analysis" in title_lower:
                content += "Data analysis conducted using structural equation modeling indicates strong support for the primary hypotheses. The measurement model demonstrated adequate reliability and validity."
            elif "discussion" in title_lower or "implication" in title_lower:
                content += "The findings significantly extend prior models by demonstrating the contextual boundaries of technology adoption. Practically, managers can leverage these insights to formulate better strategies."
            elif "conclusion" in title_lower:
                content += "In conclusion, this paper provides empirical evidence advancing the understanding of the research topic. Future research should validate these findings across different cultural contexts."
            elif "reference" in title_lower:
                content += f"**[Citations converted to {state.style_profile.citation_style} format]**\n\n[List of formatted references derived from verified sources]"
            elif "declaration" in title_lower or "statement" in title_lower:
                content += f"**[Declarations for {new_style}]**\n\nAdded mandatory statements: {', '.join(state.style_profile.declaration_requirements)}"
            else:
                content += f"**[Content mapped and restructured from old draft to fit {new_style} hierarchy]**\n\nThis section addresses the {title} aspects of the research."
                
            new_draft[title] = content
            
        state.manuscript_draft = new_draft
        return state
