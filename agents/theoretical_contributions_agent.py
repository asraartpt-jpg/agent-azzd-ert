from core.state import ResearchState
from agents.base_agent import BaseAgent
from agents.writing_agent import AcademicWritingAgent

class TheoreticalContributionsAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Theoretical Contributions Agent",
            description="Specializes in writing Section 8 (Theoretical Contributions & Practical Implications), detailing theoretical advancements (extending TPB/MOA/TCV/TOE) and actionable practice/policy implications."
        )
        self.writer = AcademicWritingAgent()

    def process(self, state: ResearchState, user_input: str = None) -> ResearchState:
        style = user_input or (state.style_profile.publisher if state.style_profile else "Elsevier / Wiley / Emerald")
        contrib_content = self.writer._generate_rich_academic_section(state, "8. Theoretical Contributions", style)
        humanized = self.writer._humanize_academic_tone(contrib_content)
        state.manuscript_draft["8. Theoretical Contributions"] = humanized
        return state
