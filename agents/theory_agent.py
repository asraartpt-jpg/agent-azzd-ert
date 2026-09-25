from typing import Dict, Any, List
from core.state import ResearchState
from agents.base_agent import BaseAgent

class TheoryAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Theoretical Framework Agent",
            description="Constructs robust multi-theoretical grounding integrating TAM/UTAUT, Social Cognitive Theory (SCT), Self-Determination Theory (SDT), Social Exchange Theory (SET), Agency Theory, Dynamic Capabilities, and the Antecedent-Mechanism-Outcome (AMO) model."
        )

    def process(self, state: ResearchState, user_input: str = None) -> ResearchState:
        topic = state.topic or "Agentic AI Adoption"
        
        state.theoretical_background = {
            "core_theories": [
                {
                    "theory": "Technology Acceptance Model (TAM) & Meta-UTAUT",
                    "seminal_authors": "Davis (1989); Venkatesh et al. (2022)",
                    "core_constructs": ["Perceived Usefulness (PU)", "Perceived Ease of Use (PEU)", "Behavioral Intention (BI)"],
                    "application_to_topic": f"Explains how cognitive evaluations of {topic}'s autonomous utility and interface usability drive user acceptance and reduce adoption friction."
                },
                {
                    "theory": "Social Cognitive Theory (SCT)",
                    "seminal_authors": "Bandura (1986); Compeau & Higgins (1995)",
                    "core_constructs": ["AI-Supported Self-Efficacy (AISS)", "Triadic Reciprocal Causation", "Mastery Experience"],
                    "application_to_topic": f"Frames how confidence in operating autonomous agentic systems directly translates cognitive utility into sustained task persistence and performance."
                },
                {
                    "theory": "Self-Determination Theory (SDT)",
                    "seminal_authors": "Deci & Ryan (2000); Ryan & Deci (2020)",
                    "core_constructs": ["Autonomy Support", "Competence", "Intrinsic Motivation"],
                    "application_to_topic": f"Demonstrates that when {topic} acts as a collaborative co-agent rather than a rigid controller, psychological autonomy needs are satisfied, fostering proactive engagement."
                },
                {
                    "theory": "Social Exchange Theory (SET) & Knowledge Management",
                    "seminal_authors": "Blau (1964); Cropanzano & Mitchell (2005); Alavi & Leidner (2001)",
                    "core_constructs": ["Knowledge-Sharing Culture (KSC)", "Reciprocal Learning", "Shared Sensemaking"],
                    "application_to_topic": f"Illustrates how an open, collaborative organizational culture mediates the translation of AI explainability and autonomy into collective adoption norms."
                },
                {
                    "theory": "Agency Theory & Co-Agency",
                    "seminal_authors": "Jensen & Meckling (1976); Hughes et al. (2025)",
                    "core_constructs": ["Principal-Agent Dynamics", "Delegated Decision Rights", "Shared Accountability"],
                    "application_to_topic": f"Reframes governance when AI systems assume autonomous decision rights, establishing verification guardrails to align agent behavior with organizational objectives."
                },
                {
                    "theory": "Dynamic Capabilities & Institutional Theory",
                    "seminal_authors": "Teece (2018); North (1990); DiMaggio & Powell (1983)",
                    "core_constructs": ["Sensing, Seizing, Reconfiguring", "Coercive, Normative, Mimetic Isomorphism", "Institutional Voids"],
                    "application_to_topic": f"Analyzes how enterprises adapt infrastructure, overcome regulatory uncertainty, and build resilience to assimilate {topic} in turbulent environments."
                }
            ],
            "framework_type": "Antecedent–Mechanism–Outcome (AMO) Multilevel Model",
            "framework_summary": (
                f"The integration of TAM, SCT, SDT, and Dynamic Capabilities establishes a holistic framework for {topic}. "
                f"Technological, organizational, and institutional antecedents enable core agentic mechanisms (autonomy, adaptivity, proactiveness, and co-agency), "
                f"which drive strategic outcomes (business performance, cognitive empowerment, and sustainable organizational excellence)."
            )
        }
        
        self._last_message = f"Constructed multi-theoretical grounding (TAM, SCT, SDT, SET, Agency, Dynamic Capabilities) for {topic}."
        return state
