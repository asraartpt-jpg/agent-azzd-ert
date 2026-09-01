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

class ChatRequest(BaseModel):
    session_id: Optional[str] = None
    phase: str
    message: str

class GeneratePaperRequest(BaseModel):
    title: str
    target_publisher: Optional[str] = None
    target_journal: Optional[str] = None
    article_type: Optional[str] = "Original Research Article"
    research_questions: Optional[List[str]] = None
    objectives: Optional[List[str]] = None

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

@router.post("/generate_paper")
async def generate_full_paper(request: GeneratePaperRequest):
    session_id = str(uuid.uuid4())
    state = ResearchState(
        session_id=session_id,
        topic=request.title,
        target_publisher=request.target_publisher,
        target_journal=request.target_journal,
        article_type=request.article_type,
        research_questions=request.research_questions or [],
        objectives=request.objectives or []
    )
    
    try:
        # Phase 1-4: Generate Style Blueprint
        style_input = f"{request.target_publisher}|{request.target_journal}|{request.article_type}"
        state = orchestrator.route_request(state, "style", user_input=style_input)
        
        # Discovery and Verification
        state = orchestrator.route_request(state, "discovery", user_input=state.topic)
        state = orchestrator.route_request(state, "verification")
        
        # Scaffold Manuscript Draft based on Blueprint
        if state.manuscript_blueprint and "sections" in state.manuscript_blueprint:
            for sec in state.manuscript_blueprint["sections"]:
                title = sec["title"]
                state.manuscript_draft[title] = f"### {title}\n\n[Content for {title}]"
        else:
            # Fallback if blueprint generation failed
            state.manuscript_draft["1. Introduction"] = f"### 1. Introduction\n\nThis study explores {state.topic}."
        
        state = orchestrator.route_request(state, "synthesis")
        state = orchestrator.route_request(state, "methodology", user_input="Generate automated methodology matching the objectives.")
        state = orchestrator.route_request(state, "data", user_input="Simulate standard structural equation modeling results based on hypotheses.")
        
        # Enforce selected publisher style formatting using Writing Agent
        style_name = state.style_profile.publisher if state.style_profile else request.target_publisher
        state = orchestrator.route_request(state, "writing", user_input=style_name)
        state = orchestrator.route_request(state, "citation")
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

