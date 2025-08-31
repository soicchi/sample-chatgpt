from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


class Recipe(BaseModel):
    ingredients: list[str] = Field(description="ingredients of the dish")
    steps: list[str] = Field(description="steps to make the dish")


def sample_output_parser() -> PydanticOutputParser[Recipe]:
    output_parser = PydanticOutputParser(pydantic_object=Recipe)
    format_instructions = output_parser.get_format_instructions()

    print(f"Format Instructions: {format_instructions}")

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "ユーザーが入力した料理のレシピを教えてください。\n\n{format_instructions}"),
            ("human", "{dish}"),
        ],
    )

    prompt_with_format_instructions = prompt.partial(
        format_instructions=format_instructions,
    )

    prompt_value = prompt_with_format_instructions.invoke({"dish": "カレーライス"})

    print("=== role: system ===")
    print(f"Prompt Value: {prompt_value.messages[0].content}")

    print("=== role: user ===")
    print(f"Prompt Value: {prompt_value.messages[1].content}")

    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    ai_message = model.invoke(prompt_value)
    print(ai_message.content)

    recipe = output_parser.invoke(ai_message.content)
    print(type(recipe))
    print(recipe)

    print(f"Ingredients: {recipe.ingredients}")
    print(f"Steps: {recipe.steps}")


if __name__ == "__main__":
    sample_output_parser()
