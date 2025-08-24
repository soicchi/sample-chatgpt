from openai import OpenAI

def call_completions_api():
    client = OpenAI()

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "人物一覧を次のJSON形式で出力してください。\n{'people': ['aaa', 'bbb']}"},
            {"role": "user", "content": "昔々あるところにお祖父さんとお婆さんがいました"}
        ],
    )

    print(response)
    print()
    print(response.choices[0].message.content)

if __name__ == "__main__":
    call_completions_api()
