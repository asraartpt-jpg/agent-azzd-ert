from core.state import ResearchState
from agents.base_agent import BaseAgent
from agents.writing_agent import AcademicWritingAgent

class IntroductionWritingAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Introduction Writing Agent",
            description="Specializes in writing Section 1 (Introduction), establishing macro problem context, theoretical gaps, IV & DV definitions, RQs, ROs, and manuscript structure."
        )
        self.writer = AcademicWritingAgent()

    def process(self, state: ResearchState, user_input: str = None) -> ResearchState:
        style = user_input or (state.style_profile.publisher if state.style_profile else "Elsevier / Wiley / Emerald")
        intro_content = self.writer._generate_rich_academic_section(state, "1. Introduction", style)
        humanized = self.writer._humanize_academic_tone(intro_content)
        state.manuscript_draft["1. Introduction"] = humanized
        return state
