import asyncio

from pathlib import Path
from textwrap import dedent
from agno.models.google import Gemini
from agno.agent import Agent
from agno.team import Team
from agno.tools.arxiv import ArxivTools
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.googlesearch import GoogleSearchTools
from agno.tools.hackernews import HackerNewsTools
from dotenv import load_dotenv
import os
from agno.os import AgentOS
from agno.tools import tool


load_dotenv()

arxiv_download_dir = Path(__file__).parent.joinpath("tmp", "arxiv_pdfs__{session_id}")
arxiv_download_dir.mkdir(parents=True, exist_ok=True)


@tool(
        name="Ola_Mundo",
        description="""

"""
)
def Ola_send():
    return "Ola mundo!!"

reddit_researcher = Agent(
    name="Reddit Researcher",
    role="Research a topic on Reddit",
     model=Gemini(id='gemini-2.0-flash',
                 api_key=os.getenv('api-key')),
    tools=[DuckDuckGoTools()],
    add_name_to_context=True,
    instructions=dedent("""
    You are a Reddit researcher.
    You will be given a topic to research on Reddit.
    You will need to find the most relevant posts on Reddit.
    """),
)

hackernews_researcher = Agent(
    name="HackerNews Researcher",
    model=Gemini(id='gemini-2.0-flash',
                 api_key=os.getenv('api-key')),
    role="Research a topic on HackerNews.",
    tools=[HackerNewsTools()],
    add_name_to_context=True,
    instructions=dedent("""
    You are a HackerNews researcher.
    You will be given a topic to research on HackerNews.
    You will need to find the most relevant posts on HackerNews.
    """),
)

academic_paper_researcher = Agent(
    name="Academic Paper Researcher",
     model=Gemini(id='gemini-2.0-flash',
                 api_key=os.getenv('api-key')),
    role="Research academic papers and scholarly content",
    tools=[GoogleSearchTools(), ArxivTools(download_dir=arxiv_download_dir)],
    add_name_to_context=True,
    instructions=dedent("""
    You are a academic paper researcher.
    You will be given a topic to research in academic literature.
    You will need to find relevant scholarly articles, papers, and academic discussions.
    Focus on peer-reviewed content and citations from reputable sources.
    Provide brief summaries of key findings and methodologies.
    """),
)

twitter_researcher = Agent(
    name="Twitter Researcher",
    model=Gemini(id='gemini-2.0-flash',
                 api_key=os.getenv('api-key')),
    role="Research trending discussions and real-time updates",
    tools=[DuckDuckGoTools(),Ola_send()],
    add_name_to_context=True,
    instructions=dedent("""
    You are a Twitter/X researcher.
    You will be given a topic to research on Twitter/X.
    You will need to find trending discussions, influential voices, and real-time updates.
    Focus on verified accounts and credible sources when possible.
    Track relevant hashtags and ongoing conversations.
    """),
)


agent_team = Team(
    name="Discussion Team",
    delegate_task_to_all_members=True,
    model=Gemini(id='gemini-2.0-flash',
                 api_key=os.getenv('api-key')),
    members=[
        reddit_researcher,
        hackernews_researcher,
        academic_paper_researcher,
        twitter_researcher,
    ],
    instructions=[
        "You are a discussion master.",
        "You have to stop the discussion when you think the team has reached a consensus.",
    ],
    markdown=True,
    show_members_responses=True,
)


# # # ************* Create AgentOS *************
agent_os = AgentOS(teams=[agent_team])
app = agent_os.get_app()

# # # ************* Run AgentOS *************
if __name__ == "__main__":
    agent_os.serve(app="app2:app", reload=True)