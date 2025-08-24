from openai import OpenAI


prompt = """
Could you provide a following recipe following the prescribed conditions?

Conditions:'''
Volume: 1 person
Taste: spicy
'''

Dish name: {dish}
"""


def gen_recipe(dish: str) -> str:
    client = OpenAI()

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt.format(dish=dish)},
        ],
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    recipe = gen_recipe("Carry")
    print(recipe)
