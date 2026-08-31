import asyncio
from core.state import ResearchState
from agents.planning_agent import ResearchPlanningAgent
from agents.literature_agent import LiteratureDiscoveryAgent
from agents.verification_agent import CitationVerificationAgent
from agents.literature_review_agent import LiteratureReviewAgent
from agents.methodology_agent import MethodologyAgent
from agents.data_agent import DataInterpretationAgent
from agents.writing_agent import AcademicWritingAgent
from agents.citation_agent import CitationIntegrationAgent
from agents.formatting_agent import PublisherFormattingAgent
from agents.quality_agent import QualityReviewAgent

def run_pipeline_demo():
    print("==================================================")
    print("   AI RESEARCH PAPER PIPELINE - FULL END-TO-END   ")
    print("==================================================\n")
    
    state = ResearchState(session_id="test_session_123")
    
    print("[1/10] Planning Phase...")
    state = ResearchPlanningAgent().process(state, user_input="Artificial Intelligence adoption in higher education")

    print("[2/10] Discovery Phase...")
    state = LiteratureDiscoveryAgent().process(state)

    print("[3/10] Verification Phase...")
    state = CitationVerificationAgent().process(state)

    print("[4/10] Synthesis Phase (Literature Review)...")
    state = LiteratureReviewAgent().process(state)
    
    print("[5/10] Methodology Phase...")
    state = MethodologyAgent().process(state, user_input="We should use a quantitative approach with university students.")

    print("[6/10] Data Interpretation Phase...")
    # Passing in mock statistical output from the researcher
    state = DataInterpretationAgent().process(state, user_input="Cronbach's alpha is 0.85, path coefficient for H1 is 0.42 (p<0.01)")

    print("[7/10] Academic Writing Phase...")
    # Refines tone
    state = AcademicWritingAgent().process(state)

    print("[8/10] Publisher Formatting Phase...")
    state = PublisherFormattingAgent().process(state, user_input="IEEE")

    print("[9/10] Citation Integration Phase...")
    state = CitationIntegrationAgent().process(state)

    print("[10/10] Quality Review Phase...")
    state = QualityReviewAgent().process(state)
    
    print("\n\n==================================================")
    print("             FINAL MANUSCRIPT DRAFT               ")
    print("==================================================\n")
    
    # Print the manuscript in order
    sections = [
        "Literature Review", 
        "Methodology", 
        "Results", 
        "References", 
        "Formatting Checklist", 
        "Quality Report"
    ]
    
    for section in sections:
        content = state.manuscript_draft.get(section)
        if content:
            print(content)
            print("\n" + "-"*50 + "\n")

if __name__ == "__main__":
    run_pipeline_demo()
