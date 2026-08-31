from typing import Dict, Any
from core.state import ResearchState
from agents.base_agent import BaseAgent

class AcademicWritingAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Academic Writing Agent",
            description="Transforms verified literature and actual findings into clear, professional academic writing."
        )

    def process(self, state: ResearchState, user_input: str = None) -> ResearchState:
        """
        Reviews the drafted sections and refines the tone to be discipline-appropriate,
        removing robotic phrases ("In today's rapidly evolving world").
        """
        for section, content in state.manuscript_draft.items():
            if section != "Formatting Checklist":
                # Mock rewriting logic to improve tone
                refined_content = self._refine_tone(content)
                state.manuscript_draft[section] = refined_content
                
        return state
        
    def _refine_tone(self, text: str) -> str:
        # Simple string replacements to simulate removing robotic AI language
        banned_phrases = {
            "In today's rapidly evolving world": "Contemporary research indicates",
            "It is worth mentioning": "Notably",
            "Delve into": "Investigate",
            "Furthermore": "Additionally"
        }
        
        refined = text
        for bad, good in banned_phrases.items():
            refined = refined.replace(bad, good)
            
        return refined
