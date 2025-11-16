from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.google import Gemini
from agno.os import AgentOS
from agno.tools.mcp import MCPTools
import os
from dotenv import load_dotenv
from textwrap import dedent


load_dotenv()

# ************* Create Agent *************
agno_agent = Agent(
    name="Agno Agent",
    instructions= dedent("""Você um Agente especialista sobre
      codigo python e projetos de criação de agents"""),
    model=Gemini(id='gemini-2.0-flash',
                 api_key=os.getenv('api-key')),
    db=SqliteDb(db_file="agno.db"),
    tools=[MCPTools(transport="streamable-http", url="https://docs.agno.com/mcp")],
    add_history_to_context=True,
    markdown=True,
    stream=True
)

# agno_agent.print_response("VOCÊ TEM ACESSO ALGUM FERRAMENTA PARA AJUDA EXPLICAR CODIGO PYTHON?")



# # ************* Create AgentOS *************
agent_os = AgentOS(agents=[agno_agent])
app = agent_os.get_app()

# # # ************* Run AgentOS *************
if __name__ == "__main__":
    agent_os.serve(app="app:app", reload=True)