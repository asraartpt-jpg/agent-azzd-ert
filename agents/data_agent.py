from typing import Dict, Any
from core.state import ResearchState
from agents.base_agent import BaseAgent

class DataInterpretationAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Data Interpretation Agent",
            description="Explains statistical or qualitative results based ONLY on researcher-provided data."
        )

    def process(self, state: ResearchState, user_input: str = None) -> ResearchState:
        """
        Takes raw statistical output (e.g., from SPSS, R, PLS) provided by the user
        and translates it into the Results and Discussion section.
        STRICT RULE: Never invent data.
        """
        if not user_input:
            state.manuscript_draft["Results"] = "[Awaiting actual data/statistical output from the researcher to interpret.]"
            return state

        # Mocking the interpretation of provided data
        # Example user_input: "Cronbach's alpha is 0.85, path coefficient for H1 is 0.42 (p<0.01)"
        draft = f"### Results and Analysis\n\n"
        draft += f"Based on the provided dataset and statistical output, the analysis yields the following interpretations:\n\n"
        
        if "alpha" in user_input.lower():
            draft += "Reliability analysis indicates high internal consistency among the construct items. "
            
        if "p<0.01" in user_input.lower() or "p < .01" in user_input.lower():
            draft += "The structural model reveals a statistically significant relationship, thereby providing strong empirical support for the proposed hypothesis.\n"
            
        draft += "\n*(Note: This interpretation is derived strictly from the researcher-supplied statistical metrics.)*"
        
        state.manuscript_draft["Results"] = draft
        return state
