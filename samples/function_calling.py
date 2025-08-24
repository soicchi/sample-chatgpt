import json
from pyexpat import model

from openai import OpenAI


def get_current_weather(location: str, unit: str = "fahrenheit") -> str:
    if "tokyo" == location.lower():
        return json.dumps({"location": "Tokyo", "temperature": "10", "unit": unit})
    elif "san francisco" == location.lower():
        return json.dumps({"location": "San Francisco", "temperature": "72", "unit": unit})
    elif "paris" == location.lower():
        return json.dumps({"location": "Paris", "temperature": "22", "unit": unit})
    else:
        return json.dumps({"location": location, "temperature": "unknown"})


tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"]
                    },
                },
                "required": ["location"],
            },
        },
    }
]


available_functions = {
    "get_current_weather": get_current_weather,
}


def sample_function_calling():
    client = OpenAI()
    messages = [
        {"role": "user", "content": "Tokyoの天気はどうですか？"},
    ]

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=tools,
    )

    response_message = response.choices[0].message
    messages.append(response_message.to_dict())

    for tool_call in response_message.tool_calls:
        function_name = tool_call.function.name
        function_to_call = available_functions[function_name]
        function_args = json.loads(tool_call.function.arguments)
        function_response = function_to_call(
            location=function_args.get("location"),
            unit=function_args.get("unit"),
        )

        messages.append({
            "tool_call_id": tool_call.id,
            "role": "tool",
            "name": function_name,
            "content": function_response,
        })

    # print(json.dumps(messages, ensure_ascii=False, indent=2))

    second_response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
    )

    print(second_response.to_json(indent=2))


if __name__ == "__main__":
    sample_function_calling()
