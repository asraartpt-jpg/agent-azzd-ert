from typing import Dict, Any, List
from core.state import ResearchState
from agents.base_agent import BaseAgent

class GapSynthesisAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Research Gap Synthesis Agent",
            description="Identifies and structures critical conceptual, empirical, and methodological gaps in the literature based on top-tier peer-reviewed research standards."
        )

    def process(self, state: ResearchState, user_input: str = None) -> ResearchState:
        topic = state.topic or "Agentic AI Adoption"
        
        state.research_gaps = [
            {
                "gap_id": "GAP-01",
                "title": "The Capability-Deployment Verification Gap",
                "description": f"While agentic AI demonstrates high-level problem-solving capabilities, organizations face severe deployment barriers due to non-determinism, context window limitations, and the absence of automated qualification mechanisms.",
                "extant_literature": "Hughes et al. (2025); Apostolou et al. (2026); Dwivedi et al. (2025a)",
                "how_addressed": f"This study develops a multi-layered governance and verification framework that establishes clear accountability guardrails for {topic}."
            },
            {
                "gap_id": "GAP-02",
                "title": "Cognitive vs Relational Sensemaking Disconnect",
                "description": f"Existing technology adoption research often treats intention as an individual cognitive consequence (TAM), neglecting how organizational knowledge-sharing culture (KSC) translates AI explainability and autonomy into collective adoption norms.",
                "extant_literature": "Islam et al. (2026); Alqurni (2026); Hu et al. (2025)",
                "how_addressed": f"Integrates Social Cognitive Theory (SCT) and Social Exchange Theory (SET) to examine how KSC and technical self-efficacy mediate the adoption pathway for {topic}."
            },
            {
                "gap_id": "GAP-03",
                "title": "The Three-Tension Reality Gap in Organizational Adoption",
                "description": f"Adoption decisions are constrained by three competing tensions: Implementation Feasibility, Adaptation Speed, and Mission Alignment, causing many AI initiatives to stall between pilot and enterprise scale.",
                "extant_literature": "Fournier & Łodzikowski (2025); Hosseini & Seilani (2025)",
                "how_addressed": f"Formulates an Antecedent–Mechanism–Outcome (AMO) diagnostic framework providing actionable strategic roadmaps to navigate adoption tensions."
            },
            {
                "gap_id": "GAP-04",
                "title": "Empirical and Methodological Scarcity",
                "description": f"Prior research predominantly relies on conceptual reviews, narrow single-step experiments, or localized pilot studies, lacking comprehensive structural equation modeling (SEM-PLS) combined with Necessary Condition Analysis (NCA).",
                "extant_literature": "Hasselwander & Lah (2026); Sarstedt et al. (2021); Hair et al. (2021)",
                "how_addressed": f"Conducts full psychometric validation, CFA, and bootstrapping structural path analysis to empirically test the hypothesized determinants of {topic}."
            }
        ]
        
        self._last_message = f"Synthesized {len(state.research_gaps)} core research gaps for {topic}."
        return state
