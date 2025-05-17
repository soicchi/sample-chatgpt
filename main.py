from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI


model = ChatOpenAI(model="gpt-4o-mini", temperature=0)


def main():
    messages = [
        SystemMessage("You are a helpful assistant."),
        HumanMessage("こんにちは！"),
    ]

    for chunk in model.stream(messages):
        print(chunk.content,end="", flush=True)


if __name__ == "__main__":
    main()
