import requests
from typing import Dict, Any
from core.state import ResearchState
from agents.base_agent import BaseAgent
from core.config import settings

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
                if settings.MISTRAL_API_KEY:
                    refined_content = self._refine_tone_with_mistral(content, style_instruction, section)
                else:
                    refined_content = self._refine_tone_mock(content)
                state.manuscript_draft[section] = refined_content
                
        return state

    def _refine_tone_with_mistral(self, text: str, style: str, section: str) -> str:
        system_prompt = f"""
        You are an elite academic editor specializing in publications for Taylor & Francis and Routledge journals.
        Your task is to take a draft for the section '{section}' and rewrite it to perfectly match the tone, 
        rigor, and stylistic conventions required by high-impact Taylor & Francis logistics, management, and social science journals.
        
        TAYLOR & FRANCIS / ROUTLEDGE RULES:
        - Use British English spelling conventions (e.g., 'operationalisation', 'prioritise', 'recognise', 'behaviour').
        - Use Author-Date citation format with NO comma between author and year (e.g., "(Willis, Genchev, and Chen 2016)" or "Yang (2016)").
        - Maintain zero AI plagiarism footprint (do not use cliché AI phrases like "In today's rapidly evolving world", "Delve into", "Tapestry", "It is worth noting").
        - The language must be highly objective, precise, formal, and analytical. Use a passive, empirical voice where appropriate.
        - Do not change the underlying facts, data, or hypotheses.
        - Output ONLY the rewritten text for the section. Do not include meta-commentary.
        """
        
        headers = {
            "Authorization": f"Bearer {settings.MISTRAL_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": settings.DEFAULT_LLM,
            "temperature": 0.3,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Rewrite the following draft text:\n\n{text}"}
            ]
        }
        
        try:
            response = requests.post("https://api.mistral.ai/v1/chat/completions", headers=headers, json=payload)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
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
            
        return refined + "\n\n[Refined for Taylor & Francis / Routledge Style]"
