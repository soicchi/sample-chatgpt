from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field


def sample_lcel_chain_with_str_output_parser() -> None:
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "ユーザーが入力した料理のレシピを考えてください。"),
            ("human", "{dish}"),
        ],
    )

    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    chain = prompt | model | StrOutputParser()

    output = chain.invoke({"dish": "カレーライス"})
    print(output)


class Recipe(BaseModel):
    ingredients: list[str] = Field(description="ingredients of the dish")
    steps: list[str] = Field(description="steps to make the dish")


def sample_lcel_chain_with_pydantic_output_parser() -> None:
    output_parser = PydanticOutputParser(pydantic_object=Recipe)

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "ユーザーが入力した料理のレシピを教えてください。\n\n{format_instructions}"),
            ("human", "{dish}"),
        ]
    )

    prompt_with_format_instructions = prompt.partial(
        format_instructions=output_parser.get_format_instructions(),
    )
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0).bind(response_format={"type": "json_object"})
    # pattern 1 PydanticOutputParserを使用するパターン
    # chain = prompt_with_format_instructions | model | output_parser

    # pattern 2: with_structured_outputを使用するパターン
    # 利用できるChatModel一覧: https://python.langchain.com/docs/integrations/chat/
    chain = prompt_with_format_instructions | model.with_structured_output(Recipe)

    recipe = chain.invoke({"dish": "カレーライス"})
    print(type(recipe))
    print(recipe)


if __name__ == "__main__":
    # sample_lcel_chain_with_str_output_parser()
    sample_lcel_chain_with_pydantic_output_parser()
