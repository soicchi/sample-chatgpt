from langchain_core.prompts import PromptTemplate


def sample_prompt_template():
    prompt = PromptTemplate.from_template("""以下の料理のレシピを教えて下さい。

料理名: {dish}""")

    prompt_value = prompt.invoke({"dish": "カレー"})
    print(prompt_value)


if __name__ == "__main__":
    sample_prompt_template()
