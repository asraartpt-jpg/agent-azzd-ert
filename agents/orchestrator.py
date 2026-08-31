from typing import Dict, Any
from core.state import ResearchState
from agents.base_agent import BaseAgent

class Orchestrator:
    """
    Manages the overall workflow and delegates tasks to specialized agents based on the current state.
    """
    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {}
        # We will register agents here later
        
    def register_agent(self, agent_name: str, agent: BaseAgent):
        self.agents[agent_name] = agent

    def route_request(self, state: ResearchState, current_phase: str, user_input: str = None) -> ResearchState:
        """
        Routes the request to the appropriate agent based on the phase.
        """
        if current_phase not in self.agents:
            raise ValueError(f"No agent registered for phase: {current_phase}")
            
        agent = self.agents[current_phase]
        updated_state = agent.process(state, user_input)
        return updated_state
