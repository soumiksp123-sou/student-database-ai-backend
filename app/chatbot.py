
import os

from typing import Annotated
from typing_extensions import TypedDict

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

from .tools import student_tools


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]


# ---------------------------------------------------------
# Gemini model
# ---------------------------------------------------------

llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    google_api_key=os.environ["GEMINI_API_KEY"]
)


# Bind database tools
llm_with_tools = llm.bind_tools(student_tools)


# ---------------------------------------------------------
# Agent node
# ---------------------------------------------------------

def agent_node(state: AgentState):

    print("\n[Agent] Processing request...")

    response = llm_with_tools.invoke(
        state["messages"]
    )

    if getattr(response, "tool_calls", None):
        print(
            "[Agent] Tool requested:",
            [
                {
                    "name": call["name"],
                    "args": call["args"]
                }
                for call in response.tool_calls
            ]
        )
    else:
        print("[Agent] No tool required.")

    return {
        "messages": [response]
    }


# ---------------------------------------------------------
# Tool node
# ---------------------------------------------------------

tool_node = ToolNode(student_tools)


# ---------------------------------------------------------
# Routing logic
# ---------------------------------------------------------

def should_continue(state: AgentState):

    last_message = state["messages"][-1]

    if getattr(last_message, "tool_calls", None):
        return "tools"

    return END


# ---------------------------------------------------------
# Build graph
# ---------------------------------------------------------

builder = StateGraph(AgentState)

builder.add_node(
    "agent",
    agent_node
)

builder.add_node(
    "tools",
    tool_node
)

builder.add_edge(
    START,
    "agent"
)

builder.add_conditional_edges(
    "agent",
    should_continue,
    {
        "tools": "tools",
        END: END
    }
)

builder.add_edge(
    "tools",
    "agent"
)


# ---------------------------------------------------------
# Compile graph
# ---------------------------------------------------------

graph = builder.compile()


# ---------------------------------------------------------
# Public chatbot function
# ---------------------------------------------------------

def ask_student_database(question: str) -> str:
    result = graph.invoke(
        {
            "messages": [
                HumanMessage(content=question)
            ]
        },
        config={
            "recursion_limit": 4
        }
    )

    final_message = result["messages"][-1]
    content = final_message.content

    if isinstance(content, str):
        return content

    if isinstance(content, list):
        text_parts = []

        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                text_parts.append(block.get("text", ""))
            elif isinstance(block, str):
                text_parts.append(block)

        return "\n".join(text_parts).strip()

    return str(content)
