from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI


def sample_chat_model_stream():
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    messages = [
        SystemMessage(content="You are a helpful assistant."),
        HumanMessage("こんにちは！"),
    ]

    for chunk in model.stream(messages):
        print(chunk.content, end="", flush=True)


if __name__ == "__main__":
    sample_chat_model_stream()
