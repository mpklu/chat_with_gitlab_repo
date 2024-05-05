import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from agents import GitLabAgents
from tasks import GitLabTasks
import os
from crewai import Agent, Task, Crew, Process

load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo")

# Define a Chat Agent
chat_agent = Agent(
    role="Chat Agent",
    goal="Engage in meaningful conversation with users.",
    verbose=True,
    memory=True,
    backstory=(
        "A friendly assistant designed to provide informative and engaging conversations."
    ),
    llm=llm,
)


# Define a Chat Task
chat_task = Task(
    description="Respond to user inputs with informative or engaging responses for {query}",
    expected_output="An appropriate response to the user's query.",
    agents=[chat_agent],
)

agents = GitLabAgents()
tasks = GitLabTasks()

developer_agent = agents.developer()
fetch_code_task = tasks.fetch_source_code(developer_agent)
# Create a Crew with the Chat Agent and Task
chat_crew = Crew(
    agents=[developer_agent],
    tasks=[fetch_code_task],
    process=Process.sequential,  # Sequential task execution
)


# CLI Interface to interact with the Crew
def chat_cli():
    print("Welcome to the GitLab Chat!")

    while True:
        user_input = input("You: ")

        # Exit condition
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        # Run the task with the user's input
        response = chat_crew.kickoff(
            inputs={
                "query": user_input,
                "instructions": "",
            }
        )

        # Display the response
        print(f"Chat Agent: {response}")


# Running the CLI
if __name__ == "__main__":
    chat_cli()
