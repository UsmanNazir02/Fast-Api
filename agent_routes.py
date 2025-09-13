from fastapi import APIRouter, HTTPException
from type import AgentCommand
from agent_service import process_agent_command
import json

router = APIRouter()

@router.post("/command")
async def agent_command(command: AgentCommand):
    """
    Process natural language commands through the agent
    
    Example prompts:
    - "Add user Sara Ali, 27, female, saraali@gmail.com"
    - "Update user 1 email to sara.ali@uni.edu"
    - "Delete user 2"
    - "Get user 1"
    - "List users"
    """
    try:
        result = process_agent_command(command.prompt)
        
        # Try to parse JSON responses for get/list operations
        if isinstance(result, str):
            # Check if the result looks like JSON
            if result.strip().startswith(('[', '{')):
                try:
                    parsed_result = json.loads(result)
                    return {"result": parsed_result}
                except json.JSONDecodeError:
                    pass
        
        return {"result": result}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent error: {str(e)}")