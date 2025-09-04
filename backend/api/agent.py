import sys
import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# Fix Python path to project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.pipelines.extract import Agent  # Import your Agent class

router = APIRouter()

# Initialize agent once at startup
agent_instance = Agent()
team_agent = agent_instance.team_agent()

# Request schema
class QueryRequest(BaseModel):
    query: str

# Response schema
class QueryResponse(BaseModel):
    answer: str

@router.post("/ask", response_model=QueryResponse)
def ask_agent(request: QueryRequest):
    """Ask the academic agent a question"""
    try:
        response = team_agent.run(request.query)
        return QueryResponse(answer=response)
    except Exception as e:
        return QueryResponse(answer=f"Error: {str(e)}")


