from crewai import Task
from textwrap import dedent


class GitLabTasks:
    def fetch_source_code(self, agent):
        return Task(
            description=dedent(
                """
                Fetch source code from gitlab repositories.
                Search for relevant repositories based on the user's query.
                It could be a file name or a class name.

                1. Search for src code files based on the user's query.
                2. Fetch the source code from the selected repository.
                3. Display the source code to the user.
                4. Provide an option to download the source code.
                5. Ask the user if additional information is needed.

                {query}
                """
            ),
            agent=agent,
            expected_output="A detailed report on the fetched repository, including its code and relevant metadata.",
        )
