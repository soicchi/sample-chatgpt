import operator
from pprint import pprint
from typing import Annotated, Any
from uuid import uuid4

from langchain_core.messages import SystemMessage, HumanMessage, BaseMessage
from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from pydantic import BaseModel, Field


# graph state
class State(BaseModel):
    query: str
    messages: Annotated[list[BaseMessage], operator.add] = Field(default_factory=list)


def add_message(state: State) -> dict[str, Any]:
    additional_messages = []
    if not state.messages:
        additional_messages.append(
            SystemMessage(content="あなたは最小限の応答をする対話エージェントです。")
        )

    additional_messages.append(HumanMessage(content=state.query))
    return {"messages": additional_messages}


def llm_response(state: State) -> dict[str, Any]:
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.0)
    ai_message = llm.invoke(state.messages)
    return {"messages": [ai_message]}


def print_checkpoint_dump(checkpointer: BaseCheckpointSaver, config: RunnableConfig):
    checkpoint_tuple = checkpointer.get_tuple(config)

    print("check point data:")
    pprint(checkpoint_tuple.checkpoint)
    print("\nmetadata:")
    pprint(checkpoint_tuple.metadata)


def setup_graph(checkpointer: BaseCheckpointSaver) -> StateGraph:
    graph = StateGraph(State)
    graph.add_node("add_message", add_message)
    graph.add_node("llm_response", llm_response)

    graph.set_entry_point("add_message")
    graph.add_edge("add_message", "llm_response")
    graph.add_edge("llm_response", END)

    return graph.compile(checkpointer=checkpointer)


def main():
    checkpointer = MemorySaver()
    state_graph = setup_graph(checkpointer)

    config = {"configurable": {"thread_id": uuid4()}}

    user_query = State(query="私の好きなものはずんだ餅です。覚えておいてね。")
    first_response = state_graph.invoke(user_query, config)
    print(first_response)

    user_second_query = State(query="私の好物は何か覚えている？")
    second_response = state_graph.invoke(user_second_query, config)
    print(second_response)


if __name__ == "__main__":
    main()
