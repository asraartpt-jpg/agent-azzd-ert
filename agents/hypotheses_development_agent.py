from core.state import ResearchState
from agents.base_agent import BaseAgent
from agents.writing_agent import AcademicWritingAgent

class HypothesesDevelopmentAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Hypotheses Development Agent",
            description="Specializes in writing Section 4 (Hypotheses Framework), synthesizing theoretical anchors with 4-5 unique Q1/Q2 citations per hypothesis without repetition and clear italicized directional statements."
        )
        self.writer = AcademicWritingAgent()

    def process(self, state: ResearchState, user_input: str = None) -> ResearchState:
        style = user_input or (state.style_profile.publisher if state.style_profile else "Elsevier / Wiley / Emerald")
        hypo_content = self.writer._generate_rich_academic_section(state, "4. Hypotheses Framework", style)
        humanized = self.writer._humanize_academic_tone(hypo_content)
        state.manuscript_draft["4. Hypotheses Framework"] = humanized
        return state
