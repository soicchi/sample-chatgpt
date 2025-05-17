from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import PydanticOutputParser
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
                "Please tell me the recipe from user input.\n\n"
                "{format_instructions}",
            ),
            ("human", "{dish}")
        ]
    )

    output_parser = PydanticOutputParser(pydantic_object=Recipe)
    format_instructions = output_parser.get_format_instructions()
    prompt_with_format_instructions = prompt.partial(
        format_instructions=format_instructions,
    )

    prompt_value = prompt_with_format_instructions.invoke({"dish": "curry"})

    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    ai_message = model.invoke(prompt_value)
    # print(ai_message.content)

    recipe = output_parser.invoke(ai_message)
    print(recipe)


if __name__ == "__main__":
    sample_prompt()
