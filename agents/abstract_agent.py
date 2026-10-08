from core.state import ResearchState
from agents.base_agent import BaseAgent
from agents.writing_agent import AcademicWritingAgent

class AbstractWritingAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Abstract Writing Agent",
            description="Specializes in writing publication-ready structured and unstructured abstracts matching top-tier Q1 journal standards (Elsevier RCR / JCP / JBR, Wiley BSD, Emerald, IEEE)."
        )
        self.writer = AcademicWritingAgent()

    def process(self, state: ResearchState, user_input: str = None) -> ResearchState:
        style = user_input or (state.style_profile.publisher if state.style_profile else "Elsevier / Wiley / Emerald")
        abstract_content = self.writer._generate_rich_academic_section(state, "Abstract", style)
        humanized = self.writer._humanize_academic_tone(abstract_content)
        state.manuscript_draft["Abstract"] = humanized
        return state
