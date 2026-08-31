from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import uuid

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

router = APIRouter()

orchestrator = Orchestrator()
orchestrator.register_agent("planning", ResearchPlanningAgent())
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
    target_journal: Optional[str] = None
    research_questions: Optional[List[str]] = None
    objectives: Optional[List[str]] = None

def _get_or_create_state(session_id: str) -> ResearchState:
    if not session_id:
        return ResearchState(session_id=str(uuid.uuid4()))
        
    # Attempt to load from Supabase
    saved_data = get_research_session(session_id)
    if saved_data:
        return ResearchState(**saved_data)
        
    return ResearchState(session_id=session_id)

@router.post("/generate_paper")
async def generate_full_paper(request: GeneratePaperRequest):
    session_id = str(uuid.uuid4())
    state = ResearchState(
        session_id=session_id,
        topic=request.title,
        target_journal=request.target_journal,
        research_questions=request.research_questions or [],
        objectives=request.objectives or []
    )
    
    try:
        if state.target_journal:
            state = orchestrator.route_request(state, "formatting", user_input=state.target_journal)
        state = orchestrator.route_request(state, "discovery", user_input=state.topic)
        state = orchestrator.route_request(state, "verification")
        
        state.manuscript_draft["Introduction"] = f"### Introduction\n\nThis study explores {state.topic}. Guided by the research objectives, we address critical gaps identified in {state.target_journal or 'recent literature'}."
        state.manuscript_draft["Theoretical Background"] = f"### Theoretical Background\n\nDrawing upon foundational theories related to {state.topic}..."
        
        state = orchestrator.route_request(state, "synthesis")
        state = orchestrator.route_request(state, "methodology", user_input="Generate automated methodology matching the objectives.")
        state = orchestrator.route_request(state, "data", user_input="Simulate standard structural equation modeling results based on hypotheses.")
        
        state.manuscript_draft["Conclusion & Future Research"] = f"### Conclusion\n\nThis paper concludes the investigation into {state.topic}."
        
        state = orchestrator.route_request(state, "writing")
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
