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
        standard_10_sections = [
            "1. Introduction",
            "2. Theoretical Background",
            "3. Literature Review",
            "4. Hypotheses Framework",
            "5. Methodology and Research Design",
            "6. Data Analysis and Interpretation",
            "7. Results and Discussions",
            "8. Theoretical Contributions",
            "9. Conclusions",
            "10. Limitations and Future Research"
        ]

        if "wiley" in pub_lower:
            profile.abstract_style = "Structured / Abstract"
            profile.abstract_sections = ["Background", "Methods", "Results", "Conclusions"]
            profile.main_sections = [
                "1 | INTRODUCTION",
                "2 | THEORETICAL BACKGROUND",
                "3 | LITERATURE REVIEW",
                "4 | HYPOTHESES FRAMEWORK",
                "5 | METHODOLOGY AND RESEARCH DESIGN",
                "6 | DATA ANALYSIS AND INTERPRETATION",
                "7 | RESULTS AND DISCUSSIONS",
                "8 | THEORETICAL CONTRIBUTIONS",
                "9 | CONCLUSIONS",
                "10 | LIMITATIONS AND FUTURE RESEARCH"
            ]
            profile.citation_style = "APA 7th / Harvard"
            profile.reference_style = "APA 7th"
            profile.declaration_requirements = ["CRediT Authorship Contribution Statement", "Conflict of Interest Statement", "Data Availability Statement", "Funding Statement"]
            profile.formatting_notes = ["Use pipe delimiter hierarchy '1 | INTRODUCTION'", "High focus on organizational relevance & structural empirical rigor"]
            
        elif "sciencedirect" in pub_lower or "elsevier" in pub_lower:
            profile.abstract_style = "Unstructured Paragraph + Optional Graphical Abstract"
            profile.main_sections = standard_10_sections
            profile.citation_style = "APA / Vancouver"
            profile.reference_style = "APA 7th"
            profile.declaration_requirements = ["Highlights (3-5 Bullet Points)", "CRediT Authorship Contribution Statement", "Declaration of Competing Interest", "Data Availability Statement"]
            profile.formatting_notes = ["Rigorous numbered sections", "Clear separation of empirical results from discussion & implications"]
            
        elif "ieee" in pub_lower:
            profile.abstract_style = "Single Paragraph"
            profile.keyword_label = "Index Terms"
            profile.main_sections = [
                "I. INTRODUCTION",
                "II. THEORETICAL BACKGROUND",
                "III. LITERATURE REVIEW",
                "IV. HYPOTHESES FRAMEWORK",
                "V. METHODOLOGY AND RESEARCH DESIGN",
                "VI. DATA ANALYSIS AND INTERPRETATION",
                "VII. RESULTS AND DISCUSSIONS",
                "VIII. THEORETICAL CONTRIBUTIONS",
                "IX. CONCLUSIONS",
                "X. LIMITATIONS AND FUTURE RESEARCH"
            ]
            profile.citation_style = "IEEE Numbered"
            profile.reference_style = "IEEE Numbered"
            profile.declaration_requirements = ["Acknowledgment", "Conflict of Interest"]
            profile.formatting_notes = ["Use Roman numeral section hierarchy (I., II., III.)", "Bracketed citations [1], [2] throughout text", "Concise, technical, quantitative tone"]
            
        elif "springer" in pub_lower:
            profile.abstract_style = "Unstructured Paragraph (150-250 words)"
            profile.main_sections = standard_10_sections
            profile.citation_style = "Springer Basic (Author-Date) or Numbered"
            profile.reference_style = "Springer Basic / APA"
            profile.declaration_requirements = ["Funding Information", "Competing Interests", "Ethical Approval", "Consent to Participate", "Data Availability"]
            profile.formatting_notes = ["IMRaD section flow", "Exhaustive ethics and declarations subsections"]
            
        elif "taylor" in pub_lower or "routledge" in pub_lower:
            profile.abstract_style = "Unstructured (up to 200 words)"
            profile.main_sections = standard_10_sections
            profile.citation_style = "Harvard / APA (Author-Date)"
            profile.reference_style = "Harvard / APA"
            profile.declaration_requirements = ["Disclosure Statement", "Data Availability Statement", "Funding Details"]
            profile.formatting_notes = ["British English spelling conventions", "Thorough theoretical grounding and managerial takeaways"]
            
        elif "igi" in pub_lower:
            profile.abstract_style = "Unstructured Paragraph"
            profile.keyword_label = "Keywords"
            profile.main_sections = [
                "1. INTRODUCTION",
                "2. THEORETICAL BACKGROUND",
                "3. LITERATURE REVIEW",
                "4. HYPOTHESES FRAMEWORK",
                "5. METHODOLOGY AND RESEARCH DESIGN",
                "6. DATA ANALYSIS AND INTERPRETATION",
                "7. RESULTS AND DISCUSSIONS",
                "8. THEORETICAL CONTRIBUTIONS",
                "9. CONCLUSIONS",
                "10. LIMITATIONS AND FUTURE RESEARCH"
            ]
            profile.citation_style = "APA 7th"
            profile.reference_style = "Compilation of References"
            profile.declaration_requirements = ["KEY TERMS AND DEFINITIONS (Dictionary Definitions)", "Conflict of Interest Statement", "Funding Acknowledgement"]
            profile.formatting_notes = ["ALL CAPS section titles", "Includes 7-10 formal dictionary definitions under Key Terms and Definitions"]
            
        elif "inderscience" in pub_lower:
            profile.abstract_style = "Unstructured Paragraph (100-150 words)"
            profile.keyword_label = "Keywords"
            profile.main_sections = standard_10_sections
            profile.citation_style = "Inderscience Harvard (Author-Date)"
            profile.reference_style = "Inderscience Harvard"
            profile.declaration_requirements = ["Biographical Notes", "Conflict of Interest", "Copyright & Permissions Notice"]
            profile.formatting_notes = ["Compact mathematical notation", "Author biographical notes required"]
            
        else: # Emerald or Default
            profile.abstract_style = "Structured (Emerald Style)"
            profile.abstract_sections = ["Purpose", "Design/methodology/approach", "Findings", "Research limitations/implications", "Practical implications", "Originality/value"]
            profile.main_sections = standard_10_sections
            profile.citation_style = "Harvard (Emerald)"
            profile.reference_style = "Harvard (Emerald)"
            profile.declaration_requirements = ["Data Availability Statement", "Conflict of Interest", "Funding Statement"]
            profile.formatting_notes = ["Emerald 6-part structured abstract", "Explicit managerial & social implications"]

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
