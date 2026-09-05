import requests
import uuid
from typing import Dict, Any
from core.state import ResearchState, ResearchSource
from agents.base_agent import BaseAgent

class SearchStrategyAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Search Strategy Agent",
            description="Searches for highly cited, relevant literature using the Semantic Scholar API."
        )

    def process(self, state: ResearchState, user_input: str = None) -> ResearchState:
        # Build query
        query_parts = [state.topic]
        if state.objectives:
            query_parts.append(state.objectives[0])
            
        query = " ".join(query_parts)[:100] # API limit query length safely
        
        try:
            # Call Semantic Scholar Graph API
            url = f"https://api.semanticscholar.org/graph/v1/paper/search"
            params = {
                "query": query,
                "limit": 10,
                "fields": "title,authors,year,journal,url,abstract,citationCount"
            }
            resp = requests.get(url, params=params, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                papers = data.get("data", [])
                
                for p in papers:
                    authors = [a.get("name", "Unknown") for a in p.get("authors", [])]
                    journal_name = p.get("journal", {}).get("name") if p.get("journal") else "Unknown Journal"
                    
                    src = ResearchSource(
                        id=str(uuid.uuid4()),
                        title=p.get("title", "Untitled"),
                        authors=authors,
                        year=p.get("year") or 2024,
                        journal=journal_name,
                        url=p.get("url"),
                        status="PENDING", # Let verification agent check it
                        quartile="UNRANKED" # Let verification agent rank it
                    )
                    src.metadata["abstract"] = p.get("abstract", "")
                    src.metadata["citationCount"] = p.get("citationCount", 0)
                    
                    state.sources.append(src)
                    
                self._last_message = f"Found {len(papers)} relevant papers on Semantic Scholar."
            else:
                self._last_message = f"Semantic Scholar API returned {resp.status_code}"
                
        except Exception as e:
            self._last_message = f"Failed to search literature: {str(e)}"
            
        return state
