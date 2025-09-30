from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_ollama import ChatOllama
import asyncio
import os

async def main():
    client = MultiServerMCPClient(
        {
            "calculator": {
                "command": "python",
                "args": ["calculator.py"],
                "transport": "stdio"
            },
            "weather": {
                "url": "http://localhost:8000/mcp",
                "transport": "streamable_http"
            }
        }
    )
    tools = await client.get_tools()

    model = ChatOllama(model="llama3.2:3b")

    agent = create_react_agent(model, tools)

    response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "what's 10 + 20?"}]}
    )

    print(response["messages"][-1].content)


asyncio.run(main())
