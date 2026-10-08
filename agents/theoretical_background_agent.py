from core.state import ResearchState
from agents.base_agent import BaseAgent
from agents.writing_agent import AcademicWritingAgent

class TheoreticalBackgroundAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Theoretical Background Agent",
            description="Specializes in writing Section 2 (Theoretical Background), establishing theoretical foundations in TPB, TRA, MOA, TCV, TOE, NAM, and NEP frameworks with AMO blueprint tables."
        )
        self.writer = AcademicWritingAgent()

    def process(self, state: ResearchState, user_input: str = None) -> ResearchState:
        style = user_input or (state.style_profile.publisher if state.style_profile else "Elsevier / Wiley / Emerald")
        theory_content = self.writer._generate_rich_academic_section(state, "2. Theoretical Background", style)
        humanized = self.writer._humanize_academic_tone(theory_content)
        state.manuscript_draft["2. Theoretical Background"] = humanized
        return state
