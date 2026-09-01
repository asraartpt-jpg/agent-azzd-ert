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

class StyleProfile(BaseModel):
    publisher: str = ""
    journal: str = ""
    article_type: str = ""
    abstract_style: str = "Unstructured"
    abstract_sections: List[str] = Field(default_factory=list)
    keyword_label: str = "Keywords"
    keyword_count: str = "4-6"
    main_sections: List[str] = Field(default_factory=list)
    subsection_rules: Dict[str, Any] = Field(default_factory=dict)
    citation_style: str = "Standard APA"
    reference_style: str = "Standard APA"
    table_rules: str = ""
    figure_rules: str = ""
    declaration_requirements: List[str] = Field(default_factory=list)
    formatting_notes: List[str] = Field(default_factory=list)
    source: str = "Generic Publisher Profile"
    verification_status: str = "Unverified"

class ResearchState(BaseModel):
    """
    Centralized state object that holds the current progress of the research manuscript.
    """
    session_id: str
    target_publisher: Optional[str] = None
    target_journal: Optional[str] = None  
    article_type: Optional[str] = "Original Research Article"
    topic: Optional[str] = None
    
    # New Phase 1 inputs
    preferred_methodology: str = "Auto Recommend"
    publication_year_preference: str = "Last 5 years"
    journal_quality_filter: List[str] = Field(default_factory=lambda: ["Q1", "Q2", "Q3"])
    
    problem_statement: Optional[str] = None
    research_questions: List[str] = Field(default_factory=list)
    objectives: List[str] = Field(default_factory=list)
    hypotheses: List[str] = Field(default_factory=list)
    sources: List[ResearchSource] = Field(default_factory=list)
    methodology: Dict[str, Any] = Field(default_factory=dict)
    
    # New Pipeline outputs
    research_intelligence: Dict[str, Any] = Field(default_factory=dict)
    search_strategy: Dict[str, Any] = Field(default_factory=dict)
    evidence_matrix: List[Dict[str, Any]] = Field(default_factory=list)
    research_gaps: List[Dict[str, Any]] = Field(default_factory=list)
    theoretical_background: Dict[str, Any] = Field(default_factory=dict)
    originality_report: Dict[str, Any] = Field(default_factory=dict)
    quality_dashboard: Dict[str, Any] = Field(default_factory=dict)
    
    # Publisher Style Engine fields
    style_profile: Optional[StyleProfile] = None
    manuscript_blueprint: Dict[str, Any] = Field(default_factory=dict)
    compliance_report: Dict[str, Any] = Field(default_factory=dict)
    
    manuscript_draft: Dict[str, str] = Field(default_factory=dict) 
    formatting_requirements: Dict[str, Any] = Field(default_factory=dict)
    
    topic_approved: bool = False
    blueprint_approved: bool = False
    methodology_approved: bool = False
    draft_approved: bool = False
