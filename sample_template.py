from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field


class Recipe(BaseModel):
    ingredients: list[str] = Field(description="ingredients of the dish")
    steps: list[str] = Field(description="steps to make the dish")


def sample_prompt():
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Please tell me the recipe from user input."
            ),
            ("human", "{dish}")
        ]
    )

    # output_parser = PydanticOutputParser(pydantic_object=Recipe)
    # prompt_with_format_instructions = prompt.partial(format_instructions=output_parser.get_format_instructions())

    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    chain = prompt | model.with_structured_output(Recipe)

    recipe = chain.invoke({"dish": "curry"})
    print(type(recipe))
    print(recipe)


if __name__ == "__main__":
    sample_prompt()
