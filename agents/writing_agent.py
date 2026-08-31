from typing import Dict, Any
from core.state import ResearchState
from agents.base_agent import BaseAgent
from core.config import settings

try:
    from langchain_mistralai.chat_models import ChatMistralAI
    from langchain.schema import HumanMessage, SystemMessage
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False

class AcademicWritingAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Academic Writing Agent",
            description="Transforms verified literature and actual findings into clear, professional academic writing tailored for Science Direct Management and Social Science journals."
        )

    def process(self, state: ResearchState, user_input: str = None) -> ResearchState:
        """
        Reviews the drafted sections and refines the tone to be discipline-appropriate for Science Direct.
        """
        style_instruction = user_input or "Science Direct Management Business Journals Social science journals style"
        
        for section, content in state.manuscript_draft.items():
            if section != "Formatting Checklist":
                if LANGCHAIN_AVAILABLE and settings.MISTRAL_API_KEY:
                    refined_content = self._refine_tone_with_mistral(content, style_instruction, section)
                else:
                    refined_content = self._refine_tone_mock(content)
                state.manuscript_draft[section] = refined_content
                
        return state

    def _refine_tone_with_mistral(self, text: str, style: str, section: str) -> str:
        chat = ChatMistralAI(
            mistral_api_key=settings.MISTRAL_API_KEY,
            model=settings.DEFAULT_LLM,
            temperature=0.3 # Low temperature for academic writing
        )
        
        system_prompt = f"""
        You are an elite academic editor specializing in publications for {style}.
        Your task is to take a draft for the section '{section}' and rewrite it to perfectly match the tone, 
        rigor, and stylistic conventions required by high-impact Science Direct business and social science journals.
        
        RULES:
        - Maintain zero AI plagiarism footprint (do not use cliché AI phrases like "In today's rapidly evolving world", "Delve into", "Tapestry", etc.).
        - The language must be objective, precise, formal, and analytical.
        - Do not change the underlying facts or data.
        - Output ONLY the rewritten text for the section. Do not include meta-commentary.
        """
        
        try:
            response = chat([
                SystemMessage(content=system_prompt),
                HumanMessage(content=f"Rewrite the following draft text:\n\n{text}")
            ])
            return response.content
        except Exception as e:
            print(f"Mistral Writing Error: {e}")
            return self._refine_tone_mock(text)
        
    def _refine_tone_mock(self, text: str) -> str:
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
            
        return refined + "\n\n[Refined for Science Direct Style]"
