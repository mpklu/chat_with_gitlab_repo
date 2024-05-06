from langchain_community.tools import BaseTool
from langchain_community.tools.gitlab.tool import GitLabAction
from langchain_community.utilities.gitlab import GitLabAPIWrapper
from langchain_community.agent_toolkits.gitlab.toolkit import GitLabToolkit
from prompts import SEARCH_FILE_PROMPT, GET_MERGE_REQUEST_DIFFS_PROMPT


class ExtendedGitLabAPIWrapper(GitLabAPIWrapper):
    def get_mr_diffs(self, mr_id: int) -> str | None:
        """
        Get the diffs of a merge request.

        Parameters:
            mr_id (int): The ID of the merge request.

        Returns:
            str: The diffs of the merge request.
        """
        mr = self.gitlab_repo_instance.mergerequests.get(mr_id)
        # print(mr)
        # diffs = mr.diffs.list()
        # for i, diff in enumerate(diffs):
        #     d = mr.diffs.get(diffs[i].id)
        #     print(
        #         "Diff version index: %d, id: %d, len(d.attributes['diffs']): %d"
        #         % (i, diffs[i].id, len(d.attributes["diffs"]))
        #     )
        changes = mr.changes()["changes"]
        # print(f"class: {changes.__class__}, \n\nchanges: {changes}")
        for change in changes:
            print(f"class: {change.__class__}, \n\nchanges: {change}")
            print()

        return changes

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
        elif mode == "get_mr_diffs":
            return self.get_mr_diffs(int(query))
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

    def get_mr_diffs(self) -> BaseTool:
        return GitLabAction(
            name="Get Merge Request Changes",
            description=GET_MERGE_REQUEST_DIFFS_PROMPT,
            mode="get_mr_diffs",
            api_wrapper=self.gitlab,
        )
