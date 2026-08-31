from typing import Dict, Any
from core.state import ResearchState
from agents.base_agent import BaseAgent

class PublisherFormattingAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Publisher Formatting Agent",
            description="Analyzes journal guidelines and applies structural and citation formatting rules."
        )

    def process(self, state: ResearchState, user_input: str = None) -> ResearchState:
        """
        Takes the current manuscript draft and formats it according to specified publisher rules.
        """
        # Mocking user input for journal selection
        if user_input:
            target_journal = user_input.lower()
            
            if "emerald" in target_journal:
                state.formatting_requirements = self._get_emerald_guidelines()
            elif "ieee" in target_journal:
                state.formatting_requirements = self._get_ieee_guidelines()
            else:
                state.formatting_requirements = self._get_standard_guidelines()

        # Apply formatting checklist if requirements exist
        if state.formatting_requirements:
            self._apply_formatting_checks(state)

        return state

    def _get_emerald_guidelines(self) -> Dict[str, Any]:
        return {
            "publisher": "Emerald Publishing",
            "citation_style": "Harvard",
            "abstract_format": "Structured (Purpose, Design, Findings, Originality)",
            "mandatory_sections": ["Data Availability", "Conflict of Interest"],
            "max_words": 8000
        }

    def _get_ieee_guidelines(self) -> Dict[str, Any]:
        return {
            "publisher": "IEEE",
            "citation_style": "IEEE Numbered",
            "abstract_format": "Unstructured paragraph",
            "mandatory_sections": ["Acknowledgment"],
            "max_words": 10000
        }

    def _get_standard_guidelines(self) -> Dict[str, Any]:
        return {
            "publisher": "Standard APA",
            "citation_style": "APA 7th",
            "abstract_format": "Unstructured",
            "mandatory_sections": [],
            "max_words": 7000
        }

    def _apply_formatting_checks(self, state: ResearchState):
        """
        Generates a compliance checklist based on the current draft vs guidelines.
        """
        reqs = state.formatting_requirements
        
        checklist = f"### {reqs['publisher']} Formatting Compliance Checklist\n\n"
        checklist += f"- **Citation Style**: {reqs['citation_style']} (Check required)\n"
        checklist += f"- **Abstract Format**: {reqs['abstract_format']} (Pending structuring)\n"
        
        # Check mandatory sections
        for section in reqs['mandatory_sections']:
            status = "Pass" if section in state.manuscript_draft else "Missing - Action Required"
            checklist += f"- **{section}**: {status}\n"
            
        state.manuscript_draft["Formatting Checklist"] = checklist
