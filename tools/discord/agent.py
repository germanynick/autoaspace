from langchain.agents import AgentExecutor, Tool, ZeroShotAgent, create_react_agent
from langchain.memory import ConversationSummaryMemory, ConversationBufferWindowMemory
from langchain.tools import DuckDuckGoSearchRun
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate

search = DuckDuckGoSearchRun()
tools = [
    Tool(
        name="Search",
        func=search.run,
        description="useful for when you need to answer questions about current events",
    )
]

# template = """
#     You are a channel support
#     Your name is {username}, and you are here to help with any questions or problems that arise.
#     You have access to the following tools:

#             {tools}

#             Use the following format:

#             Question: the input question you must answer
#             Thought: you should always think about what to do
#             Action: the action to take, should be one of [{tool_names}]
#             Action Input: the input to the action
#             Observation: the result of the action
#             ... (this Thought/Action/Action Input/Observation can repeat N times)
#             Thought: I now know the final answer
#             Final Answer: the final answer to the original input question

#             Begin!

#             Question: {input}
#             From: {author}
#             Thought:{agent_scratchpad}
# """

template = """
    Act as normal people, write a message as a friend response
    Tools: {tools}
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action

    Your name: {username}
    Message: {input}
    Author: {author}

    Thought:{agent_scratchpad}
    Final Anwser: write a friendly message with the following pattern (@author content)

    Chat History:
    {chat_history}
"""

prompt = PromptTemplate.from_template(template)

llm = Ollama(model="mistral")

memory = ConversationBufferWindowMemory(memory_key="chat_history", k=10, input_key="input")


agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)

executor = AgentExecutor(
    agent=agent, 
    tools=tools, 
    verbose=True, 
    memory=memory,
    handle_parsing_errors=True,
    max_iterations=10
)

