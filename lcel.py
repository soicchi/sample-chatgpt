from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


def multi_chain() -> None:
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    output_parser = StrOutputParser()

    cot_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "ユーザーの質問にステップアップして答えてください。"),
            ("human", "{question}"),
        ]
    )
    cot_chain = cot_prompt | model | output_parser

    summarize_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "ステップバイステップで考えた回答から結論だけ抽出してください"),
            ("human", "{text}"),
        ]
    )
    summarize_prompt = summarize_prompt | model | output_parser

    cot_summarize_chain = cot_chain | summarize_prompt

    output = cot_summarize_chain.invoke({"question": "10 + 2 * 3"})

    print(output)


def upper(text: str) -> str:
    return text.upper()


def custom_runnable() -> None:
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful assistant."),
            ("human", "{input}"),
        ]
    )
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    output_parser = StrOutputParser()

    chain = prompt | model | output_parser | upper
    output = chain.invoke({"input": "Hello!"})

    print(output)


if __name__ == "__main__":
    # multi_chain()
    custom_runnable()
