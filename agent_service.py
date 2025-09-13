import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from agent_tools import agent_tools


# Initialize Gemini LLM
def get_llm():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable is not set")

    return ChatGoogleGenerativeAI(
        model="gemini-1.5-flash", temperature=0, google_api_key=api_key
    )


# Create agent prompt
agent_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a helpful assistant that manages student records. 
    You have access to tools to add, update, delete, get, and list students.
    
    Important rules:
    - Gender must be 'male', 'female', or 'other'
    - Email addresses must be unique
    - Always use the appropriate tool for the user's request
    - Keep responses short and clean
    - For get_user and list_users, return the actual JSON data
    - When updating users, you can update multiple fields at once
    
    When parsing user requests:
    - Extract all relevant information (name, age, gender, email, id)
    - Use the most appropriate tool based on the request
    - Handle partial updates correctly
    - For get and list operations, return the data as JSON
    
    Examples:
    - "Add user Sara Ali, 27, female, saraali@gmail.com" -> use add_user tool
    - "Update user 1 email to sara.ali@uni.edu" -> use update_user tool with id=1, email="sara.ali@uni.edu"
    - "Update user 1 age to 28 and name to Sara A." -> use update_user tool with id=1, age=28, name="Sara A."
    - "Delete user 2" -> use delete_user tool with id=2
    - "Get user 1" -> use get_user tool with id=1
    - "List users" -> use list_users tool""",
        ),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)

# Initialize agent
_agent_executor = None


def get_agent():
    global _agent_executor
    if _agent_executor is None:
        llm = get_llm()
        agent = create_tool_calling_agent(llm, agent_tools, agent_prompt)
        _agent_executor = AgentExecutor(agent=agent, tools=agent_tools, verbose=False)
    return _agent_executor


def process_agent_command(prompt: str) -> str:
    """Process a natural language command through the agent"""
    try:
        agent_executor = get_agent()
        result = agent_executor.invoke({"input": prompt})
        return result["output"]
    except Exception as e:
        return f"Error processing command: {str(e)}"
