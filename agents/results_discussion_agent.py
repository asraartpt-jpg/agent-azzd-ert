from core.state import ResearchState
from agents.base_agent import BaseAgent
from agents.writing_agent import AcademicWritingAgent

class ResultsDiscussionAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Results and Discussions Agent",
            description="Specializes in writing Section 7 (Results & Discussions), reporting structural path coefficients (beta), t-statistics, p-values, R2, f2, Q2, 95% bootstrap CIs, stylized empirical discoveries, and comparative discussion against Q1 literature."
        )
        self.writer = AcademicWritingAgent()

    def process(self, state: ResearchState, user_input: str = None) -> ResearchState:
        style = user_input or (state.style_profile.publisher if state.style_profile else "Elsevier / Wiley / Emerald")
        res_content = self.writer._generate_rich_academic_section(state, "7. Results and Discussions", style)
        humanized = self.writer._humanize_academic_tone(res_content)
        state.manuscript_draft["7. Results and Discussions"] = humanized
        return state
