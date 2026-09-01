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
            if title == "Abstract" or "Abstract" in title:
                new_draft[title] = f"### {title}\n\n[Restructured to match {state.style_profile.abstract_style} format for {new_style}]\n\n{old_draft[:200]}..."
            elif title == state.style_profile.keyword_label:
                new_draft[title] = f"### {title}\n\n[Keywords mapped to {title} for {new_style}]"
            elif title == "References":
                new_draft[title] = f"### References\n\n[Citations converted to {state.style_profile.citation_style} format]"
            elif title == "Declarations & Statements":
                new_draft[title] = f"### Declarations\n\n[Added mandatory statements: {', '.join(state.style_profile.declaration_requirements)}]"
            else:
                new_draft[title] = f"### {title}\n\n[Content mapped and restructured from old draft to fit {new_style} hierarchy]"
                
        state.manuscript_draft = new_draft
        return state
