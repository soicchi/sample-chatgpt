from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI


def sample_chat_prompt_template():
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful assistant."),
            MessagesPlaceholder("chat_history", optional=True),
            ("human", "{input}"),
        ],
    )

    prompt_value = prompt.invoke(
        {
            "chat_history": [
                HumanMessage(content="こんにちは！私はジョンといいます！"),
                AIMessage(content="こんにちは、ジョンさん！お会いできて嬉しいです。今日はどのようにお手伝いできますか？"),
            ],
            "input": "私の名前は分かりますか？",
        }
    )

    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    for chunk in model.stream(prompt_value.to_messages()):
        print(chunk.content, end="", flush=True)

if __name__ == "__main__":
    sample_chat_prompt_template()

