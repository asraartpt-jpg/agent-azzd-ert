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
            
            if "wiley" in target_journal:
                state.formatting_requirements = self._get_wiley_guidelines()
            elif "emerald" in target_journal:
                state.formatting_requirements = self._get_emerald_guidelines()
            elif "ieee" in target_journal:
                state.formatting_requirements = self._get_ieee_guidelines()
            elif "taylor" in target_journal or "routledge" in target_journal:
                state.formatting_requirements = self._get_taylor_francis_guidelines()
            elif "elsevier" in target_journal or "science direct" in target_journal or "sciencedirect" in target_journal:
                state.formatting_requirements = self._get_elsevier_guidelines()
            elif "springer" in target_journal:
                state.formatting_requirements = self._get_springer_guidelines()
            elif "igi" in target_journal:
                state.formatting_requirements = self._get_igi_guidelines()
            elif "inderscience" in target_journal:
                state.formatting_requirements = self._get_inderscience_guidelines()
            else:
                state.formatting_requirements = self._get_standard_guidelines()

        # Apply formatting checklist if requirements exist
        if state.formatting_requirements:
            self._apply_formatting_checks(state)

        return state

    def _get_wiley_guidelines(self) -> Dict[str, Any]:
        return {
            "publisher": "Wiley",
            "citation_style": "APA 7th / Harvard",
            "abstract_format": "Structured / Unstructured (Background, Methods, Results, Conclusions)",
            "mandatory_sections": ["CRediT Authorship Contribution Statement", "Conflict of Interest Statement", "Data Availability Statement"],
            "max_words": 9000
        }

    def _get_emerald_guidelines(self) -> Dict[str, Any]:
        return {
            "publisher": "Emerald Publishing",
            "citation_style": "Harvard (Emerald)",
            "abstract_format": "Structured (Purpose, Design, Findings, Practical Implications, Originality)",
            "mandatory_sections": ["Data Availability Statement", "Conflict of Interest", "Funding Statement"],
            "max_words": 8500
        }

    def _get_ieee_guidelines(self) -> Dict[str, Any]:
        return {
            "publisher": "IEEE",
            "citation_style": "IEEE Numbered [1], [2]",
            "abstract_format": "Single Paragraph (Index Terms)",
            "mandatory_sections": ["Acknowledgment", "Conflict of Interest"],
            "max_words": 10000
        }

    def _get_taylor_francis_guidelines(self) -> Dict[str, Any]:
        return {
            "publisher": "Taylor & Francis / Routledge",
            "citation_style": "Harvard / APA (Author-Date)",
            "abstract_format": "Unstructured (up to 200 words)",
            "mandatory_sections": ["Disclosure Statement", "Data Availability Statement", "Funding Details"],
            "max_words": 8500
        }

    def _get_elsevier_guidelines(self) -> Dict[str, Any]:
        return {
            "publisher": "Elsevier / ScienceDirect",
            "citation_style": "APA 7th / Vancouver",
            "abstract_format": "Unstructured paragraph + Highlights (3-5 bullet points)",
            "mandatory_sections": ["Highlights", "CRediT Authorship Contribution Statement", "Declaration of Competing Interest", "Data Availability Statement"],
            "max_words": 9500
        }

    def _get_springer_guidelines(self) -> Dict[str, Any]:
        return {
            "publisher": "Springer",
            "citation_style": "Springer Basic (Author-Date) or Numbered",
            "abstract_format": "Unstructured Paragraph (150-250 words)",
            "mandatory_sections": ["Funding Information", "Competing Interests", "Ethical Approval", "Data Availability"],
            "max_words": 8500
        }

    def _get_igi_guidelines(self) -> Dict[str, Any]:
        return {
            "publisher": "IGI Global",
            "citation_style": "APA 7th",
            "abstract_format": "Unstructured Paragraph",
            "mandatory_sections": ["KEY TERMS AND DEFINITIONS", "Conflict of Interest Statement", "Funding Acknowledgement"],
            "max_words": 8000
        }

    def _get_inderscience_guidelines(self) -> Dict[str, Any]:
        return {
            "publisher": "Inderscience",
            "citation_style": "Inderscience Harvard (Author-Date)",
            "abstract_format": "Unstructured Paragraph (100-150 words)",
            "mandatory_sections": ["Biographical Notes", "Conflict of Interest", "Copyright & Permissions Notice"],
            "max_words": 7500
        }

    def _get_standard_guidelines(self) -> Dict[str, Any]:
        return {
            "publisher": "Standard Academic Journal",
            "citation_style": "APA 7th",
            "abstract_format": "Unstructured",
            "mandatory_sections": ["Declarations", "References"],
            "max_words": 8000
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
