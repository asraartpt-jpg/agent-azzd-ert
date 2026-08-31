from typing import Dict, Any, List
from core.state import ResearchState
from agents.base_agent import BaseAgent

class MethodologyAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Research Methodology Agent",
            description="Assists in developing an appropriate research design and analysis plan."
        )

    def process(self, state: ResearchState, user_input: str = None) -> ResearchState:
        """
        Interactively develops the methodology based on the research topic and synthesized gap.
        """
        # If methodology is already approved, skip
        if state.methodology_approved:
            return state

        # Mocking methodology generation based on user input or state
        if user_input and "quantitative" in user_input.lower():
            state.methodology = {
                "approach": "Quantitative",
                "design": "Cross-sectional survey",
                "population": "University students in North America",
                "sampling": "Stratified random sampling",
                "analysis_plan": "Structural Equation Modeling (SEM) using PLS-SEM",
                "ethical_considerations": "IRB approval required, informed consent for all participants."
            }
            state.manuscript_draft["Methodology"] = self._generate_methodology_text(state.methodology)
        elif user_input and "qualitative" in user_input.lower():
            state.methodology = {
                "approach": "Qualitative",
                "design": "Multiple case study",
                "population": "Higher education administrators",
                "sampling": "Purposive sampling",
                "analysis_plan": "Thematic analysis",
                "ethical_considerations": "Anonymity of institutions and participants."
            }
            state.manuscript_draft["Methodology"] = self._generate_methodology_text(state.methodology)
        elif not state.methodology:
            # Provide initial recommendations if none exists
            state.methodology = {
                "recommendation": "Based on your topic, a mixed-methods approach might be suitable. Do you prefer a primarily quantitative or qualitative approach?"
            }

        return state

    def _generate_methodology_text(self, methodology_dict: Dict[str, Any]) -> str:
        """
        Transforms the structured methodology into academic text.
        """
        draft = f"### Research Methodology\n\n"
        draft += f"This study adopts a **{methodology_dict.get('approach')}** research approach, utilizing a **{methodology_dict.get('design')}** design. "
        draft += f"The target population comprises **{methodology_dict.get('population')}**, selected through **{methodology_dict.get('sampling')}** techniques. "
        draft += f"Data will be analyzed using **{methodology_dict.get('analysis_plan')}** to test the proposed hypotheses and address the research objectives.\n\n"
        draft += f"#### Ethical Considerations\n"
        draft += f"{methodology_dict.get('ethical_considerations')}"
        
        return draft
