from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from enum import Enum

class SourceStatus(str, Enum):
    VERIFIED = "VERIFIED"
    PENDING = "PENDING"
    UNVERIFIED = "UNVERIFIED"
    REJECTED = "REJECTED"

class JournalRank(str, Enum):
    Q1 = "Q1"
    Q2 = "Q2"
    Q3 = "Q3"
    Q4 = "Q4"
    UNRANKED = "UNRANKED"

class ResearchSource(BaseModel):
    id: str
    title: str
    authors: List[str]
    year: int
    journal: str
    doi: Optional[str] = None
    url: Optional[str] = None
    status: SourceStatus = SourceStatus.PENDING
    is_scopus_indexed: bool = False
    is_wos_indexed: bool = False
    quartile: JournalRank = JournalRank.UNRANKED
    metadata: Dict[str, Any] = Field(default_factory=dict)

class ResearchState(BaseModel):
    """
    Centralized state object that holds the current progress of the research manuscript.
    """
    session_id: str
    target_journal: Optional[str] = None  # Added for journal-specific scope
    topic: Optional[str] = None
    problem_statement: Optional[str] = None
    research_questions: List[str] = Field(default_factory=list)
    objectives: List[str] = Field(default_factory=list)
    hypotheses: List[str] = Field(default_factory=list)
    sources: List[ResearchSource] = Field(default_factory=list)
    methodology: Dict[str, Any] = Field(default_factory=dict)
    manuscript_draft: Dict[str, str] = Field(default_factory=dict) 
    formatting_requirements: Dict[str, Any] = Field(default_factory=dict)
    
    topic_approved: bool = False
    methodology_approved: bool = False
    draft_approved: bool = False
