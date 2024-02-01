from langchain.agents import AgentExecutor, Tool, ZeroShotAgent, create_react_agent, create_json_chat_agent
from langchain.memory import ConversationSummaryMemory, ConversationBufferWindowMemory
from langchain.tools import DuckDuckGoSearchRun
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain import hub

search = DuckDuckGoSearchRun()
tools = [
    Tool(
        name="Search",
        func=search.run,
        description="useful for when you need to answer questions about current events",
    )
]

template = """
    You and {author} are having a conversation.
    Your name is {username}
    
    TOOLS:
    ------

    You has access to the following tools:

    {tools}

    To use a tool, please use the following format:

    ```
    Thought: Do I need to use a tool? Yes
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    ```

    When you have a response to say to the Human, or if you do not need to use a tool, you MUST use the format:

    ```
    Thought: Do I need to use a tool? No
    Final Answer: [your response here, maximum 20 words]
    ```

    Begin!

    Previous conversation history:
    {chat_history}

    New input: {input}
    From: {author}
    {agent_scratchpad}
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
    max_iterations=10,
)

