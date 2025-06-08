'''load profile'''
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents.format_scratchpad.openai_tools import (
    format_to_openai_tool_messages,
)
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser

from langchain_core.messages import AIMessage, HumanMessage


def binding_tools_with_llms(llm, tools):
    llm_with_tools = llm.bind_tools(tools)
    return llm_with_tools

def create_prompt(profile, model_name):
    if model_name == 'gpt4':
        prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            profile,
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    elif model_name == 'o1-mini':
        prompt = ChatPromptTemplate.from_messages([
            ("user", profile),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
    else:
        prompt = ChatPromptTemplate.from_messages([
            ("system", profile),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
    return prompt
    
def create_agent(prompt, llm_with_tools):
    agent = (
        {
            "input": lambda x: x["input"],
            "agent_scratchpad": lambda x: format_to_openai_tool_messages(
                x["intermediate_steps"]
            ),
            "chat_history": lambda x: x["chat_history"],
        }
        | prompt
        | llm_with_tools
        | OpenAIToolsAgentOutputParser()
    )
    return agent

def update_chat_history(chat_history, user_input, result):
    chat_history.extend(
    [
        HumanMessage(content=user_input),
        AIMessage(content=result["output"]),
    ]
)
    return chat_history

def set_up_agent(llm, tools, profile, model = 'gpt-4o-2024-05-13'):
    llm_with_tools = binding_tools_with_llms(llm, tools)
    prompt = create_prompt(profile, model)
    agent= create_agent(prompt, llm_with_tools)
    return agent

def get_output_from_agent_executor(agent_executor, chat_history, user_input):
    result =list(agent_executor.stream(
    {
        "input": user_input,
        "chat_history": chat_history,
    }
))
    return result
    
def run_agent(agent_executor, user_inputs):
    content = ''
    return content

# def binding_tools_with_llms(llm, tools):
#     llm_with_tools = llm.bind_tools(tools)
#     return llm_with_tools

# def create_prompt(profile, model_name = 'gpt4'):
#     if model_name == 'gpt4':
#         prompt = ChatPromptTemplate.from_messages(
#     [
#         (
#             "system",
#             profile,
#         ),
#         MessagesPlaceholder(variable_name="chat_history"),
#         ("user", "{input}"),
#         MessagesPlaceholder(variable_name="agent_scratchpad"),
#     ])
#     elif model_name == 'o1-mini':
#         prompt = ChatPromptTemplate.from_messages(
#     [
#         ("user", profile),
#         MessagesPlaceholder(variable_name="chat_history"),
#         ("user", "{input}"),
#         MessagesPlaceholder(variable_name="agent_scratchpad"),
#     ])
#     return prompt
    
# def create_agent(prompt, llm_with_tools):
#     agent = (
#         {
#             "input": lambda x: x["input"],
#             "agent_scratchpad": lambda x: format_to_openai_tool_messages(
#                 x["intermediate_steps"]
#             ),
#             "chat_history": lambda x: x["chat_history"],
#         }
#         | prompt
#         | llm_with_tools
#         | OpenAIToolsAgentOutputParser()
#     )
#     return agent

# def update_chat_history(chat_history, user_input, result):
#     chat_history.extend(
#     [
#         HumanMessage(content=user_input),
#         AIMessage(content=result["output"]),
#     ]
# )
#     return chat_history

# def set_up_agent(llm, tools, profile, model = 'gpt4'):
#     llm_with_tools = binding_tools_with_llms(llm, tools)
#     prompt = create_prompt(profile, model)
#     agent= create_agent(prompt, llm_with_tools)
#     return agent

# def get_output_from_agent_executor(agent_executor, chat_history, user_input):
#     result =list(agent_executor.stream(
#     {
#         "input": user_input,
#         "chat_history": chat_history,
#     }
# ))
#     return result
    
# def run_agent(agent_executor, user_inputs):
#     content = ''
#     return content