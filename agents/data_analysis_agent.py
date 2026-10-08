from core.state import ResearchState
from agents.base_agent import BaseAgent
from agents.writing_agent import AcademicWritingAgent

class DataAnalysisAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Data Analysis and Interpretation Agent",
            description="Specializes in writing Section 6 (Data Analysis & Interpretation) & Section 7 (Results & Discussions), reporting factor loadings (>=0.70), Cronbach's alpha, CR, AVE, Fornell-Larcker, HTMT (<0.90), PLS-SEM path coefficients (beta), t-values, p-values, R2, f2, Q2, 95% bootstrap CIs [LL, UL], mediation analysis, and Multi-Group Analysis (MGA)."
        )
        self.writer = AcademicWritingAgent()

    def process(self, state: ResearchState, user_input: str = None) -> ResearchState:
        style = user_input or (state.style_profile.publisher if state.style_profile else "Elsevier / Wiley / Emerald")
        
        # Write both Section 6 and Section 7
        data_content = self.writer._generate_rich_academic_section(state, "6. Data Analysis and Interpretation", style)
        results_content = self.writer._generate_rich_academic_section(state, "7. Results and Discussions", style)
        
        state.manuscript_draft["6. Data Analysis and Interpretation"] = self.writer._humanize_academic_tone(data_content)
        state.manuscript_draft["7. Results and Discussions"] = self.writer._humanize_academic_tone(results_content)
        return state
