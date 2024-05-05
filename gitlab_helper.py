from langchain_community.tools import BaseTool
from langchain_community.tools.gitlab.tool import GitLabAction
from langchain_community.utilities.gitlab import GitLabAPIWrapper
from langchain_community.agent_toolkits.gitlab.toolkit import GitLabToolkit
from prompts import SEARCH_FILE_PROMPT


class ExtendedGitLabAPIWrapper(GitLabAPIWrapper):
    # def __init__(self):
    #     super().__init__()

    def search_file(self, file_name: str) -> str | None:
        """
        Search for a file in the repository.

        Parameters:
            file_name (str): The name of the file to search for.

        Returns:
            str: The path of the file.
        """
        search_result = self.gitlab_repo_instance.search(
            scope="blobs",
            # search=f"filename:{file_name}"
            search=file_name,
        )

        for result in search_result:
            return result["path"]

        return None

    def run(self, mode: str, query: str) -> str:
        if mode == "search_file":
            return self.search_file(query)
        else:
            return super.run(mode, query)


class GitLabToolsHelper:

    toolkit = GitLabToolkit.from_gitlab_api_wrapper(GitLabAPIWrapper())

    gitlab = ExtendedGitLabAPIWrapper()

    def all_tools(self):
        return self.toolkit.get_tools()

    def read_file(self) -> BaseTool:
        tools = self.all_tools()
        return next((tool for tool in tools if tool.name == "Read File"), None)

    def search_file(self) -> BaseTool:
        return GitLabAction(
            name="Search File",
            description=SEARCH_FILE_PROMPT,
            mode="search_file",
            api_wrapper=self.gitlab,
        )
