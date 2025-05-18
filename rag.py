from langchain_community.document_loaders import GitLoader


def file_filter(file_path: str) -> bool:
    return file_path.endswith(".mdx")


def sample_rag():
    loader = GitLoader(
        clone_url="https:/github.com/langhcain-ai/langchain",
        repo_path="./langchain",
        branch="master",
        file_filter=file_filter,
    )

    row_docs = loader.load()
    print(row_docs)


if __name__ == "__main__":
    sample_rag()
