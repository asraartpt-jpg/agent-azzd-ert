from core.state import ResearchState
from agents.base_agent import BaseAgent
from core.config import settings

try:
    from langchain_mistralai.chat_models import ChatMistralAI
    from langchain_core.messages import HumanMessage, SystemMessage
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False

class ResearchPlanningAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Research Planning Agent",
            description="Interactively helps the researcher define topic, gap, and objectives using Mistral AI."
        )

    def process(self, state: ResearchState, user_input: str = None) -> ResearchState:
        if not user_input:
            return state

        if LANGCHAIN_AVAILABLE and settings.MISTRAL_API_KEY:
            return self._process_with_llm(state, user_input)
        else:
            return self._process_mock(state, user_input)

    def _process_with_llm(self, state: ResearchState, user_input: str) -> ResearchState:
        # Initialize the Mistral AI client
        chat = ChatMistralAI(
            mistral_api_key=settings.MISTRAL_API_KEY,
            model=settings.DEFAULT_LLM,
            temperature=0.7
        )
        
        system_prompt = f"""
        You are the Research Planning Agent for an academic manuscript.
        The current state of the research is:
        - Topic: {state.topic or 'Not defined'}
        - Problem Statement: {state.problem_statement or 'Not defined'}
        
        Analyze the user's input. If they provide a broad topic, help them narrow it down.
        Return ONLY a JSON object updating the state fields you identified. 
        Format: {{"topic": "new topic", "problem_statement": "new problem"}}
        """
        
        try:
            response = chat([
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_input)
            ])
            
            import json
            import re
            
            match = re.search(r'\{.*\}', response.content, re.DOTALL)
            if match:
                data = json.loads(match.group(0))
                if "topic" in data and data["topic"]:
                    state.topic = data["topic"]
                if "problem_statement" in data and data["problem_statement"]:
                    state.problem_statement = data["problem_statement"]
                    
        except Exception as e:
            print(f"LLM Error: {e}")
            self._process_mock(state, user_input)
            
        return state

    def _process_mock(self, state: ResearchState, user_input: str) -> ResearchState:
        if not state.topic:
            state.topic = user_input
        elif not state.problem_statement:
            state.problem_statement = user_input
            
        return state
