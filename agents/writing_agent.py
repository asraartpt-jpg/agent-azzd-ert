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
        Generates the manuscript sections based on empirical data, verified sources, and blueprint.
        """
        style_instruction = user_input or "Science Direct Management Business Journals Social science journals style"
        
        # Build context
        context = f"Topic: {state.topic}\n"
        if state.research_questions:
            context += f"Research Questions: {', '.join(state.research_questions)}\n"
        if state.objectives:
            context += f"Objectives: {', '.join(state.objectives)}\n"
        if state.hypotheses:
            context += f"Hypotheses: {', '.join(state.hypotheses)}\n"
        
        context += "\n--- Verified Literature References ---\n"
        for src in state.sources:
            context += f"Title: {src.title}\nAuthors: {', '.join(src.authors)}\nAbstract: {src.metadata.get('abstract', '')[:300]}\n\n"
            
        context += f"\n--- Empirical Data ---\n{state.empirical_data[:3000]}\n"
        
        for section, content in state.manuscript_draft.items():
            if section != "Formatting Checklist":
                if settings.MISTRAL_API_KEY:
                    generated_content = self._generate_with_mistral(context, style_instruction, section)
                else:
                    generated_content = self._refine_tone_mock(content, style_instruction)
                state.manuscript_draft[section] = f"### {section}\n\n" + generated_content
                
        return state

    def _generate_with_mistral(self, context: str, style: str, section: str) -> str:
        system_prompt = f"""
        You are an elite academic writer for {style} journals.
        Your task is to WRITE the content for the section '{section}'.
        
        GENERAL PUBLISHER RULES:
        - If {style} is Taylor & Francis or Emerald: Use British English.
        - If {style} is IEEE: Use numbered citation format [1].
        - Use standard APA Author-Date format otherwise.
        - Maintain zero AI plagiarism footprint. Be highly objective, precise, and formal.
        - Output ONLY the written text for the section. Do not include meta-commentary.
        """
        
        headers = {
            "Authorization": f"Bearer {settings.MISTRAL_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": settings.DEFAULT_LLM,
            "temperature": 0.4,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Write the section '{section}' based on the following research context, literature, and empirical data:\n\n{context}"}
            ]
        }
        
        try:
            response = requests.post("https://api.mistral.ai/v1/chat/completions", headers=headers, json=payload)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"Mistral Writing Error: {e}")
            return f"[Error connecting to Mistral API: {str(e)}. Ensure MISTRAL_API_KEY is configured in Vercel.]"
        
    def _refine_tone_mock(self, text: str, style: str = "Standard") -> str:
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
            
        return refined + f"\n\n[Refined for {style} Style]"
