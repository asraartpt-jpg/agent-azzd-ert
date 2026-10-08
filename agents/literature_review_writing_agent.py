from core.state import ResearchState
from agents.base_agent import BaseAgent
from agents.writing_agent import AcademicWritingAgent

class LiteratureReviewWritingAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Literature Review Writing Agent",
            description="Specializes in writing Section 3 (Literature Review), conducting PRISMA 2020 systematic review protocol, Boolean search string tables, 4-phase PRISMA flow diagram, and empirical gap matrices."
        )
        self.writer = AcademicWritingAgent()

    def process(self, state: ResearchState, user_input: str = None) -> ResearchState:
        style = user_input or (state.style_profile.publisher if state.style_profile else "Elsevier / Wiley / Emerald")
        lit_content = self.writer._generate_rich_academic_section(state, "3. Literature Review", style)
        humanized = self.writer._humanize_academic_tone(lit_content)
        state.manuscript_draft["3. Literature Review"] = humanized
        return state
