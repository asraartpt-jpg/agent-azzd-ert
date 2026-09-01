import json
from typing import Dict, Any
from core.state import ResearchState, StyleProfile
from agents.base_agent import BaseAgent

class JournalStyleAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Journal Style Agent",
            description="Analyzes target publisher/journal to generate a strict style profile and manuscript blueprint."
        )

    def process(self, state: ResearchState, user_input: str = None) -> ResearchState:
        """
        Determines the publisher profile and creates a manuscript blueprint.
        """
        # Set target publisher/journal if provided in user_input
        # Format expected: publisher|journal|article_type OR CUSTOM_GUIDELINES|text
        if user_input:
            parts = user_input.split("|", 1)
            if parts[0] == "CUSTOM_GUIDELINES":
                text = parts[1]
                if not state.style_profile:
                    state.style_profile = self._generate_publisher_profile("Custom", "Custom Journal", "Custom Article")
                
                # Mock extracting details from text
                state.style_profile.source = "User-Uploaded Journal Guidelines"
                state.style_profile.verification_status = "Custom Override"
                if "APA" in text:
                    state.style_profile.citation_style = "APA (Extracted)"
                elif "IEEE" in text:
                    state.style_profile.citation_style = "IEEE (Extracted)"
                
                if "structured abstract" in text.lower():
                    state.style_profile.abstract_style = "Structured (Extracted)"
                
                # Update the blueprint to match the new custom profile
                state.manuscript_blueprint = self._generate_blueprint(state.style_profile)
                self._last_message = "Successfully analyzed and applied custom uploaded guidelines."
                return state
                
            parts = user_input.split("|")
            if len(parts) > 0 and parts[0]:
                state.target_publisher = parts[0]
            if len(parts) > 1 and parts[1]:
                state.target_journal = parts[1]
            if len(parts) > 2 and parts[2]:
                state.article_type = parts[2]

        if not state.target_publisher:
            state.target_publisher = "Taylor & Francis / Routledge" # default

        # Generate Style Profile
        profile = self._generate_publisher_profile(state.target_publisher, state.target_journal, state.article_type)
        state.style_profile = profile

        # Generate Manuscript Blueprint
        blueprint = self._generate_blueprint(profile)
        state.manuscript_blueprint = blueprint
        
        # We need the user to approve the blueprint. So we format a message for the orchestrator to show.
        self._last_message = self._format_blueprint_display(blueprint, profile)
        
        return state

    def _generate_publisher_profile(self, publisher: str, journal: str, article_type: str) -> StyleProfile:
        profile = StyleProfile(
            publisher=publisher,
            journal=journal or "Unspecified Journal",
            article_type=article_type or "Original Research Article"
        )
        
        pub_lower = publisher.lower()
        if "emerald" in pub_lower:
            profile.abstract_style = "Structured"
            profile.abstract_sections = ["Purpose", "Design/methodology/approach", "Findings", "Originality/value"]
            profile.main_sections = ["Introduction", "Literature Review", "Theoretical Foundation", "Research Methodology", "Findings", "Discussion", "Implications", "Conclusion"]
            profile.citation_style = "Harvard"
            profile.reference_style = "Harvard"
            profile.declaration_requirements = ["Data Availability", "Conflict of Interest"]
            profile.formatting_notes = ["Emphasize clear managerial relevance", "Explicit theoretical contribution"]
        
        elif "ieee" in pub_lower:
            profile.abstract_style = "Single Paragraph"
            profile.keyword_label = "Index Terms"
            profile.main_sections = ["I. INTRODUCTION", "II. RELATED WORK", "III. METHODOLOGY", "IV. RESULTS AND ANALYSIS", "V. DISCUSSION", "VI. CONCLUSION"]
            profile.citation_style = "IEEE Numbered"
            profile.reference_style = "IEEE Numbered"
            profile.declaration_requirements = ["Acknowledgment"]
            profile.formatting_notes = ["Use numbered section hierarchy (Roman Numerals)", "Technical, precise, concise tone"]
            
        elif "elsevier" in pub_lower or "science direct" in pub_lower:
            profile.abstract_style = "Unstructured Paragraph + Optional Graphical Abstract"
            profile.main_sections = ["1. INTRODUCTION", "2. LITERATURE REVIEW", "3. METHODOLOGY", "4. RESULTS", "5. DISCUSSION", "6. CONCLUSION"]
            profile.citation_style = "APA / Vancouver"
            profile.reference_style = "APA / Vancouver"
            profile.declaration_requirements = ["Highlights", "CRediT Authorship Contribution Statement", "Declaration of Competing Interest"]
            profile.formatting_notes = ["Clear scientific argument", "Results separated from interpretation"]
            
        elif "springer" in pub_lower:
            profile.abstract_style = "Unstructured Paragraph"
            profile.main_sections = ["Introduction", "Methodology", "Results", "Discussion", "Conclusion"]
            profile.citation_style = "Springer Basic (Author-Date) or Numbered"
            profile.reference_style = "Springer Basic"
            profile.declaration_requirements = ["Declarations", "Funding", "Competing Interests"]
            profile.formatting_notes = ["Use IMRaD logic where appropriate"]
            
        else: # Taylor & Francis or Generic
            profile.abstract_style = "Unstructured (up to 200 words)"
            profile.main_sections = ["Introduction", "Literature Review", "Theoretical Background", "Methodology", "Results", "Discussion", "Conclusion"]
            profile.citation_style = "APA / Harvard / Chicago"
            profile.reference_style = "APA / Harvard"
            profile.declaration_requirements = ["Disclosure Statement", "Data Availability Statement"]
            profile.formatting_notes = ["Use British English spelling conventions", "Highly objective, precise academic tone"]

        return profile

    def _generate_blueprint(self, profile: StyleProfile) -> Dict[str, Any]:
        blueprint = {
            "metadata": {
                "publisher": profile.publisher,
                "journal": profile.journal,
                "article_type": profile.article_type,
                "citation_style": profile.citation_style
            },
            "sections": []
        }
        
        # Add abstract
        blueprint["sections"].append({
            "title": "Abstract",
            "type": profile.abstract_style,
            "details": profile.abstract_sections if profile.abstract_sections else "1 paragraph"
        })
        
        # Add keywords
        blueprint["sections"].append({
            "title": profile.keyword_label,
            "details": f"{profile.keyword_count} terms"
        })
        
        # Add main sections
        for sec in profile.main_sections:
            blueprint["sections"].append({
                "title": sec,
                "details": "Standard section"
            })
            
        # Add declarations
        if profile.declaration_requirements:
            blueprint["sections"].append({
                "title": "Declarations & Statements",
                "details": profile.declaration_requirements
            })
            
        blueprint["sections"].append({
            "title": "References",
            "details": profile.reference_style
        })
        
        return blueprint

    def _format_blueprint_display(self, blueprint: Dict[str, Any], profile: StyleProfile) -> str:
        md = f"### MANUSCRIPT BLUEPRINT GENERATED\n\n"
        md += f"**Publisher:** {blueprint['metadata']['publisher']}\n"
        md += f"**Journal:** {blueprint['metadata']['journal']}\n"
        md += f"**Article Type:** {blueprint['metadata']['article_type']}\n"
        md += f"**Citation Style:** {blueprint['metadata']['citation_style']}\n\n"
        
        md += f"**Note:** Publisher-level style profile applied. Specific journal requirements may override this structure.\n\n"
        md += f"---\n\n"
        
        for i, sec in enumerate(blueprint['sections']):
            md += f"**SECTION {i+1}: {sec['title']}**\n"
            if isinstance(sec['details'], list):
                for item in sec['details']:
                    md += f"- {item}\n"
            else:
                md += f"- {sec['details']}\n"
            md += "\n"
            
        md += "---\n\nPlease review this blueprint. If you approve, you can proceed to manuscript generation."
        return md
