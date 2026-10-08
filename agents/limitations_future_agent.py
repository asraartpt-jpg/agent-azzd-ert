from core.state import ResearchState
from agents.base_agent import BaseAgent
from agents.writing_agent import AcademicWritingAgent

class LimitationsFutureAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Limitations and Future Research Agent",
            description="Specializes in writing Section 10 (Limitations and Future Research), detailing methodological boundaries and formal future research propositions."
        )
        self.writer = AcademicWritingAgent()

    def process(self, state: ResearchState, user_input: str = None) -> ResearchState:
        style = user_input or (state.style_profile.publisher if state.style_profile else "Elsevier / Wiley / Emerald")
        lim_content = self.writer._generate_rich_academic_section(state, "10. Limitations and Future Research", style)
        humanized = self.writer._humanize_academic_tone(lim_content)
        state.manuscript_draft["10. Limitations and Future Research"] = humanized
        return state
