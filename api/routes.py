from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from typing import Optional, List
import uuid
import io

try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None

from core.state import ResearchState
from core.database import save_research_session, get_research_session
from agents.orchestrator import Orchestrator
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
from agents.style_agent import JournalStyleAgent
from agents.restructure_agent import RestructuringAgent
from agents.intelligence_agent import IntelligenceAgent
from agents.search_strategy_agent import SearchStrategyAgent
from agents.quality_verification_agent import QualityVerificationAgent
from agents.evidence_extraction_agent import EvidenceExtractionAgent
from agents.gap_synthesis_agent import GapSynthesisAgent
from agents.theory_agent import TheoryAgent
from agents.originality_agent import OriginalityAgent

router = APIRouter()

orchestrator = Orchestrator()
orchestrator.register_agent("planning", ResearchPlanningAgent())
orchestrator.register_agent("style", JournalStyleAgent())
orchestrator.register_agent("restructure", RestructuringAgent())
orchestrator.register_agent("discovery", LiteratureDiscoveryAgent())
orchestrator.register_agent("verification", CitationVerificationAgent())
orchestrator.register_agent("synthesis", LiteratureReviewAgent())
orchestrator.register_agent("methodology", MethodologyAgent())
orchestrator.register_agent("data", DataInterpretationAgent())
orchestrator.register_agent("writing", AcademicWritingAgent())
orchestrator.register_agent("citation", CitationIntegrationAgent())
orchestrator.register_agent("formatting", PublisherFormattingAgent())
orchestrator.register_agent("quality", QualityReviewAgent())

# New pipeline agents
orchestrator.register_agent("intelligence", IntelligenceAgent())
orchestrator.register_agent("search_strategy", SearchStrategyAgent())
orchestrator.register_agent("quality_verification", QualityVerificationAgent())
orchestrator.register_agent("evidence_extraction", EvidenceExtractionAgent())
orchestrator.register_agent("gap_synthesis", GapSynthesisAgent())
orchestrator.register_agent("theory", TheoryAgent())
orchestrator.register_agent("originality", OriginalityAgent())
class ChatRequest(BaseModel):
    session_id: Optional[str] = None
    phase: str
    message: str

class GeneratePaperRequest(BaseModel):
    session_id: Optional[str] = None
    title: str
    target_publisher: Optional[str] = None
    target_journal: Optional[str] = None
    article_type: Optional[str] = "Original Research Article"
    research_questions: Optional[List[str]] = None
    objectives: Optional[List[str]] = None
    hypotheses: Optional[List[str]] = None
    keywords: Optional[List[str]] = None
    preferred_methodology: Optional[str] = "Auto Recommend"
    publication_year_preference: Optional[str] = "Last 5 years"
    journal_quality_filter: Optional[List[str]] = ["Q1", "Q2", "Q3"]

def _get_or_create_state(session_id: str) -> ResearchState:
    if not session_id:
        return ResearchState(session_id=str(uuid.uuid4()))
        
    saved_data = get_research_session(session_id)
    if saved_data:
        return ResearchState(**saved_data)
        
    return ResearchState(session_id=session_id)

@router.post("/upload_guidelines")
async def upload_guidelines(
    session_id: str = Form(...),
    file: UploadFile = File(...)
):
    state = _get_or_create_state(session_id)
    
    try:
        content = ""
        if file.filename.endswith('.pdf'):
            if PdfReader is None:
                raise Exception("pypdf is not installed")
            pdf = PdfReader(io.BytesIO(await file.read()))
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    content += text + "\n"
        else:
            content = (await file.read()).decode('utf-8')
            
        # Pass the extracted text to the Style Agent to parse and override the profile
        state = orchestrator.route_request(state, "style", user_input=f"CUSTOM_GUIDELINES|{content[:3000]}")
        
        save_research_session(state.session_id, state.model_dump())
        
        return {
            "session_id": state.session_id,
            "state": state.model_dump(),
            "message": f"Successfully processed guidelines from {file.filename}."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/upload_sources")
async def upload_sources(
    session_id: Optional[str] = Form(None),
    files: List[UploadFile] = File(...)
):
    if not session_id:
        session_id = str(uuid.uuid4())
    state = _get_or_create_state(session_id)
    
    try:
        from core.state import ResearchSource
        import uuid
        
        for file in files:
            content = ""
            if file.filename.endswith('.pdf'):
                if PdfReader is None:
                    continue # Skip if no pypdf
                pdf = PdfReader(io.BytesIO(await file.read()))
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        content += text + "\n"
                        
                # Add as verified source
                src = ResearchSource(
                    id=str(uuid.uuid4()),
                    title=f"Uploaded PDF: {file.filename}",
                    authors=["Unknown Uploaded"],
                    year=2026,
                    journal="User Uploaded PDF",
                    status="VERIFIED",
                    is_scopus_indexed=True,
                    is_wos_indexed=True,
                    quartile="Q1" # Automatically trust user PDF
                )
                src.metadata["abstract"] = content[:1500] # store some content
                state.sources.append(src)
                
            elif file.filename.endswith(('.csv', '.txt')):
                content = (await file.read()).decode('utf-8', errors='ignore')
                state.empirical_data += f"\n--- Data from {file.filename} ---\n{content}\n"
                
        save_research_session(state.session_id, state.model_dump())
        return {"session_id": state.session_id, "message": f"Successfully processed {len(files)} files."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate_paper")
async def generate_full_paper(request: GeneratePaperRequest):
    session_id = request.session_id or str(uuid.uuid4())
    state = _get_or_create_state(session_id)
    
    # Update state with incoming request parameters
    state.topic = request.title
    state.target_publisher = request.target_publisher
    state.target_journal = request.target_journal
    state.article_type = request.article_type
    state.research_questions = request.research_questions or []
    state.objectives = request.objectives or []
    state.hypotheses = request.hypotheses or []
    state.keywords = request.keywords or []
    state.preferred_methodology = request.preferred_methodology or "Auto Recommend"
    state.publication_year_preference = request.publication_year_preference or "Last 5 years"
    state.journal_quality_filter = request.journal_quality_filter or ["Q1", "Q2", "Q3"]
    
    try:
        # STEP 1-4: Input Validation & Research Intelligence
        state = orchestrator.route_request(state, "intelligence")
        
        # STEP 5: Search Strategy
        state = orchestrator.route_request(state, "search_strategy")
        
        # STEP 6-7: Scholarly Search
        state = orchestrator.route_request(state, "discovery", user_input=state.topic)
        
        # STEP 8-11: Verification & Q1/Q2/Q3 Filtering
        state = orchestrator.route_request(state, "quality_verification")
        
        # STEP 16-17: Evidence Extraction Matrix
        state = orchestrator.route_request(state, "evidence_extraction")
        
        # STEP 18: Research Gap Synthesis
        state = orchestrator.route_request(state, "gap_synthesis")
        
        # STEP 19: Theoretical Background
        state = orchestrator.route_request(state, "theory")
        
        # STEP 20: Methodology Plan
        state = orchestrator.route_request(state, "methodology")
        
        # STEP 21-22: Style Retrieval & Blueprint
        style_input = f"{request.target_publisher}|{request.target_journal}|{request.article_type}"
        state = orchestrator.route_request(state, "style", user_input=style_input)
        
        # Scaffold Manuscript Draft based on Blueprint
        if state.manuscript_blueprint and "sections" in state.manuscript_blueprint:
            for sec in state.manuscript_blueprint["sections"]:
                title = sec["title"]
                state.manuscript_draft[title] = ""
        else:
            state.manuscript_draft["1. Introduction"] = ""
        
        # STEP 37: Citation Integrity
        state = orchestrator.route_request(state, "citation")
        
        # STEP 38: Originality & Writing Quality
        state = orchestrator.route_request(state, "originality")
        
        # Enforce selected publisher style formatting using Writing Agent (This will now GENERATE the text)
        style_name = state.style_profile.publisher if state.style_profile else request.target_publisher
        state = orchestrator.route_request(state, "writing", user_input=style_name)
        
        # STEP 39: Journal Compliance Check (Dashboard)
        state = orchestrator.route_request(state, "quality")
        
        # Save final state to Supabase
        save_research_session(session_id, state.model_dump())
        
        return {
            "session_id": session_id,
            "state": state.model_dump(),
            "message": "Full automated paper generation complete."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/chat")
async def chat_with_agent(request: ChatRequest):
    state = _get_or_create_state(request.session_id)
    
    try:
        updated_state = orchestrator.route_request(
            state=state, 
            current_phase=request.phase, 
            user_input=request.message
        )
        
        # Save updated state to Supabase
        save_research_session(updated_state.session_id, updated_state.model_dump())
        
        if request.phase == "planning":
            reply = f"I've updated your research topic to: '{updated_state.topic}'. Should we define the problem statement next?"
        elif request.phase == "discovery":
            reply = f"I found {len(updated_state.sources)} sources related to '{updated_state.topic}'. They are currently pending verification."
        elif request.phase == "verification":
            reply = f"Verification complete. Check the 'Source Database' tab to see which ones passed the Q1-Q3 & Scopus/WoS checks."
        else:
            reply = f"Agent '{request.phase}' has processed your request and updated the manuscript draft."
            
        return {
            "session_id": updated_state.session_id,
            "state": updated_state.model_dump(),
            "response": reply
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

class SwitchStyleRequest(BaseModel):
    session_id: str
    target_publisher: str
    target_journal: Optional[str] = None
    article_type: str

@router.post("/switch_style")
async def switch_style(request: SwitchStyleRequest):
    state = _get_or_create_state(request.session_id)
    state.target_publisher = request.target_publisher
    state.target_journal = request.target_journal
    state.article_type = request.article_type
    
    try:
        # Phase 1-4: Generate New Style Blueprint
        style_input = f"{request.target_publisher}|{request.target_journal}|{request.article_type}"
        state = orchestrator.route_request(state, "style", user_input=style_input)
        
        # Phase 6-7: Restructure Manuscript
        state = orchestrator.route_request(state, "restructure", user_input=request.target_publisher)
        
        # Phase 8: Re-run Compliance Report
        state = orchestrator.route_request(state, "quality")
        
        save_research_session(state.session_id, state.model_dump())
        
        return {
            "session_id": state.session_id,
            "state": state.model_dump(),
            "message": f"Successfully switched manuscript style to {request.target_publisher}."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

