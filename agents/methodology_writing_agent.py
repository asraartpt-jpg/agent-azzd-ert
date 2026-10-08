from core.state import ResearchState
from agents.base_agent import BaseAgent
from agents.writing_agent import AcademicWritingAgent

class MethodologyWritingAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Methodology Writing Agent",
            description="Specializes in writing Section 5 (Methodology & Research Design), detailing sampling frames, G*Power calculations (N=308/410), measurement scales, Harman CMV tests (<50%), and VIF collinearity checks (<3.3)."
        )
        self.writer = AcademicWritingAgent()

    def process(self, state: ResearchState, user_input: str = None) -> ResearchState:
        style = user_input or (state.style_profile.publisher if state.style_profile else "Elsevier / Wiley / Emerald")
        meth_content = self.writer._generate_rich_academic_section(state, "5. Methodology and Research Design", style)
        humanized = self.writer._humanize_academic_tone(meth_content)
        state.manuscript_draft["5. Methodology and Research Design"] = humanized
        return state
