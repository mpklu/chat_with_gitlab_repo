from crewai import Agent
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from gitlab_helper import GitLabToolsHelper

load_dotenv()
llm = ChatOpenAI(model="gpt-3.5-turbo")


class GitLabAgents:
    def developer(self):
        toolkit = GitLabToolsHelper()
        tools = [toolkit.read_file(), toolkit.search_file()]
        return Agent(
            role="Software Engineer",
            goal="Search and fetch source code from gitlab repositories.",
            backstory="A software engineer with experience in gitlab repositories.",
            verbose=False,
            tools=tools,
            llm=llm,
        )
