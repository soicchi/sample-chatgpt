from langchain_core.messages import AIMessage
from langchain_core.output_parsers import StrOutputParser


def sample_str_output_parser() -> None:
    output_parser = StrOutputParser()

    ai_message = AIMessage(content="こんにちは。私はAIアシスタントです。")
    output = output_parser.invoke(ai_message)
    print(type(output))
    print(output)


if __name__ == "__main__":
    sample_str_output_parser()
