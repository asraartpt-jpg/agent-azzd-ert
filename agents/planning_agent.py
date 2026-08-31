from core.state import ResearchState
from agents.base_agent import BaseAgent
from core.config import settings

# Attempt to import langchain, fallback to mock if API key missing
try:
    from langchain.chat_models import ChatOpenAI
    from langchain.schema import HumanMessage, SystemMessage
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False

class ResearchPlanningAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Research Planning Agent",
            description="Interactively helps the researcher define topic, gap, and objectives using an LLM."
        )

    def process(self, state: ResearchState, user_input: str = None) -> ResearchState:
        """
        Invokes an LLM to chat with the user, extract the topic, problem statement, and objectives, 
        and updates the state.
        """
        if not user_input:
            return state

        # If we have an API key and LangChain installed, do a real LLM call
        if LANGCHAIN_AVAILABLE and settings.OPENAI_API_KEY and settings.OPENAI_API_KEY != "your_openai_api_key_here":
            return self._process_with_llm(state, user_input)
        else:
            # Fallback to the mock behavior for testing without keys
            return self._process_mock(state, user_input)

    def _process_with_llm(self, state: ResearchState, user_input: str) -> ResearchState:
        chat = ChatOpenAI(temperature=0.7, model_name=settings.DEFAULT_LLM, openai_api_key=settings.OPENAI_API_KEY)
        
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
            
            # Very basic JSON parsing for the sake of the prototype
            import json
            import re
            
            # Extract JSON from response
            match = re.search(r'\{.*\}', response.content, re.DOTALL)
            if match:
                data = json.loads(match.group(0))
                if "topic" in data and data["topic"]:
                    state.topic = data["topic"]
                if "problem_statement" in data and data["problem_statement"]:
                    state.problem_statement = data["problem_statement"]
                    
        except Exception as e:
            print(f"LLM Error: {e}")
            # Graceful fallback
            self._process_mock(state, user_input)
            
        return state

    def _process_mock(self, state: ResearchState, user_input: str) -> ResearchState:
        """Mock extraction for when API keys aren't set"""
        if not state.topic:
            state.topic = user_input
        elif not state.problem_statement:
            state.problem_statement = user_input
            
        return state
