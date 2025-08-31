from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI


def sample_chat_model():
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    messages = [
        SystemMessage(content="You are a helpful assistant."),
        HumanMessage("こんにちは！私はジョンといいます！"),
        AIMessage(content="こんにちは、ジョンさん！お会いできて嬉しいです。今日はどのようにお手伝いできますか？"),
        HumanMessage(content="私の名前は分かりますか？"),
    ]

    ai_message = model.invoke(messages)
    print(ai_message.content)


if __name__ == "__main__":
    sample_chat_model()
