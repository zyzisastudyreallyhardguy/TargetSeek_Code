import sys
import os

from langchain.agents import AgentExecutor
from langchain.chains import LLMChain

from Report_Reviewing_AgentReviewer.prompt import editor_self_developed_prompt, editor_feedback_prompt, editor_summary_prompt,editor_summary_prompt_with_mp,mistake_pool_prompt
from Report_Reviewing_AgentReviewer.instructions_1101 import editor_instruction, rebuttal_instruction, rebuttal_summary_instructions, mistake_pool_instructions
from Report_Reviewing_AgentReviewer.report_sec_output_format import genetic_evidence
from Report_Generation_AgentAnalyst import tools, run_section, agent_usage, agent_instructions

import concurrent.futures
import json
import ast

def create_agent(llm, google_search, set_up_agent, profile):
    google_tool = google_search()
    tool_name = [google_tool]

    agent = set_up_agent(llm, tool_name, profile)

    return agent, tool_name

def agent_response(agent, tool_name, prompt):
    genetic_evidence_agent_executor = AgentExecutor(agent=agent, tools=tool_name, verbose=False)

    user_input = prompt
    chat_history = []
    output = list(genetic_evidence_agent_executor.stream({"input": user_input, "chat_history":chat_history}))
    return output[-1]['output']

def load_report(directory):
    with open(directory, 'r') as f:
        report = f.read()
    return report

def split_questions(questions):
    result = []
    for i in range(0, len(questions), 2):
        result.append('\n'.join(questions[i:i+2]))
    return result

#for all questions in the question_list, each process_num will be used to create the feedback prompt
def feedback_question_list(question_list, process_num = 2):
    feedback_question_list = []
    for i in range(0, len(question_list), process_num):
        # combine each num questions to a string
        feedback_question_list.append('\n'.join(question_list[i:i+process_num]))
    return feedback_question_list

def get_feedback(feedback_agent, tool_name, feedback_prompt):
    return agent_response(feedback_agent, tool_name, feedback_prompt)

def generate_responses_in_parallel(prompt_question_list, report_sec, llm, google_search, agent_usage, editor_feedback_instruction):
    response_list = [None] * len(prompt_question_list)  # 初始化结果列表

    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Create a dictionary to keep track of futures and their order
        future_to_index = {}
        for index, questions in enumerate(prompt_question_list):
            feedback_prompt = editor_feedback_prompt(submitted_report=report_sec, questions=questions)
            feedback_agent, tool_name = create_agent(llm, google_search, agent_usage.set_up_agent, profile=editor_feedback_instruction)
            future = executor.submit(get_feedback, feedback_agent, tool_name, feedback_prompt)
            future_to_index[future] = index
        
        # Collect the results in order
        for future in concurrent.futures.as_completed(future_to_index):
            index = future_to_index[future]
            response_list[index] = future.result()
    
    return response_list

def generate_responses_together(prompt_question_list, report_sec, llm, google_search, agent_usage, editor_feedback_instruction):
    for i, questions in enumerate(prompt_question_list):
        feedback_prompt = editor_feedback_prompt(submitted_report=report_sec, questions=questions)
        feedback_agent, tool_name = create_agent(llm, google_search, agent_usage.set_up_agent, profile=editor_feedback_instruction)
        response_list = get_feedback(feedback_agent, tool_name, feedback_prompt)

    return response_list

def obtain_questions(report,section_name):
    # load the report tern_deployment/reports/gpam/report_gpam_genetic_evidence.md
    # report = load_report(report_directory)

    #set up instruction
    self_developed_output_format = '''
    1. Are you sure ........?
    2. Are you sure ........?
    .......

    **You have to output 10 questions in total.**
    '''
    editor_self_instruction = editor_instruction(section_name, output_format = self_developed_output_format)

    #set up llm
    llm = run_section.testChat()
    google_search = tools.google_search

    # set up agent
    agent, tool_name = create_agent(llm, google_search, agent_usage.set_up_agent, profile = editor_self_instruction)
        #set up prompt
    self_developed_prompt = editor_self_developed_prompt(report)

    response =  agent_response(agent, tool_name, self_developed_prompt)

    return response

def obtain_feedbacks_together(report, questions, section_name):
    llm = run_section.testChat()
    google_search = tools.google_search

    question_list = questions.split('\n')

    feedback_output_format = '''
    Question X: Are you sure ...
    Answer: Yes or No, ...
    Action: You need to ...  to correct the mistake.

    An example output is shown below: 
    Question 1: Are you sure ...
    Answer: Yes, from reference [X], ...
    Action: You need to ...
    Question 2: Are you sure ... 
    Answer: No, from reference [X], ...
    Action: You need to remove the row xxx ...
    '''
    #set up instruction
    editor_feedback_instruction = rebuttal_instruction(section_name, output_format = feedback_output_format)
    prompt_question_list = feedback_question_list(question_list,process_num=len(question_list))

    responses = generate_responses_together(prompt_question_list, report, llm, google_search, agent_usage, editor_feedback_instruction)
    
    # responses = generate_responses_in_parallel(prompt_question_list, report, llm, google_search, agent_usage, editor_feedback_instruction)
    return [responses]

def obtain_feedbacks(report, questions,section_name):
    llm = run_section.testChat()
    google_search = tools.google_search

    question_list = questions.split('\n')

    feedback_output_format = '''
    Question X: Are you sure ...
    Answer: Yes or No, ...
    Action: You need to ...  to correct the mistake.

    An example output is shown below: 
    Question 1: Are you sure ...
    Answer: Yes, from reference [X], ...
    Action: You need to ...
    Question 2: Are you sure ... 
    Answer: No, from reference [X], ...
    Action: You need to remove the row xxx ...
    '''
    #set up instruction
    editor_feedback_instruction = rebuttal_instruction(section_name, output_format = feedback_output_format)
    prompt_question_list = feedback_question_list(question_list,process_num=2)
    responses = generate_responses_in_parallel(prompt_question_list, report, llm, google_search, agent_usage, editor_feedback_instruction)
    return responses


def summarize_feedback(feedback_input, report, gene_name, section_name, save_dir):
    llm = run_section.testChat()
    google_search = tools.google_search

    summary_prompt = editor_summary_prompt(report, gene_name, feedback_input)

    summary_instruction = rebuttal_summary_instructions(section_name)
    agent, tool_name = create_agent(llm, google_search, agent_usage.set_up_agent, profile = summary_instruction)
    summarize_feedback = agent_response(agent, tool_name, summary_prompt)

    if save_dir:
        # save the summarize_feedback to feedback_repo
        with open(os.path.join(save_dir, f"{gene_name}_{section_name}.md"), 'w') as f:
            f.write(summarize_feedback)

    return summarize_feedback

def summarize_feedback_with_mistakePool(feedback_input, report, gene_name, section_name, mistake_pool_file, save_dir):
    llm = run_section.testChat()
    google_search = tools.google_search

    with open(mistake_pool_file, 'r') as json_file:
        mistake_pool = json.load(json_file)

    summary_prompt = editor_summary_prompt_with_mp(report, gene_name, feedback_input,mistake_pool)
    summary_instruction = rebuttal_summary_instructions(section_name)
    agent, tool_name = create_agent(llm, google_search, agent_usage.set_up_agent, profile = summary_instruction)
    summarize_feedback = agent_response(agent, tool_name, summary_prompt)

    # if save_dir:
    #     # save the summarize_feedback to feedback_repo
    #     with open(os.path.join(save_dir, f"{gene_name}_{section_name}.md"), 'w') as f:
    #         f.write(summarize_feedback)
    
    mp_instructions, mp_prompts = mistake_pool_instructions(mistake_pool,report,summarize_feedback)
    mistake_pool_prompts = mistake_pool_prompt(mp_instructions, mp_prompts)
    llm = run_section.testChat()
    # Create the LLMChain
    llm_chain = LLMChain(llm=llm, prompt=mistake_pool_prompts)
    # Generate the response
    mistake_pool_response = llm_chain.run(mistake_pool=mistake_pool, report=report, summarized_feedback=summarize_feedback)

    # 提取字典部分
    try:
        dict_str = mistake_pool_response.split("=", 1)[1].strip()
        mistake_pool = ast.literal_eval(dict_str)
        with open(mistake_pool_file, 'w') as json_file:
            json.dump(mistake_pool, json_file, indent=4)
    except:
        print('error in saving mistake pools')
        print(f'mistake pool response is {mistake_pool_response}')

    return summarize_feedback

def summarize_feedback_offline(feedback_input, report, gene_name, section_name, save_dir):
    # 不使用google search
    llm = run_section.testChat()
    google_search = tools.google_search

    summary_prompt = editor_summary_prompt(report, gene_name, feedback_input)

    summary_instruction = rebuttal_summary_instructions(section_name)
    agent, tool_name = create_agent(llm, google_search, agent_usage.set_up_agent, profile = summary_instruction)
    summarize_feedback = agent_response(agent, tool_name, summary_prompt)

    if save_dir:
        # save the summarize_feedback to feedback_repo
        with open(os.path.join(save_dir, f"{gene_name}_{section_name}.md"), 'w') as f:
            f.write(summarize_feedback)

    return summarize_feedback

def get_profile_name(section_name):
    if section_name == 'genetic_evidence':
        profile = agent_instructions.genetic_evidence_finder_profile()
    return profile

def refine_report_based_on_feedback(report, summarized_feedback, section_name, gene_name, disease_name):
#     profile = f'''
# Your task is to refine the report based on the feedback. 
# **Think first based on the feedback and then refine the report.**
# **The gain of function and loss of function tables should only include the gene {gene_name} that we are concerned about.**
# **Directly return the refined report and only the refined report, without any description of your actions.**
# '''
#     llm = run_section.testChat()
#     google_search = tools.google_search
#     prompt = f'''
# PART1 Feedback:
# {summarized_feedback}
# -----------------------
# PART2 Original Report:
# {report}
# -----------------------
# Based on the first part feedback, refine the second part, which is the report you wrote. Use web search when necessary to confirm some information.
# **The gain of function and loss of function tables should only include the gene {gene_name} that we are concerned about.**
# '''

    profile = f'''
Your task is to refine the report based on the feedback. 
**Think first based on the feedback and then refine the report.**
**Directly return the refined report and only the refined report, without any description of your actions.**
'''
    llm = run_section.testChat()
    google_search = tools.google_search
    prompt = f'''
PART1 Feedback:
{summarized_feedback}
-----------------------
PART2 Original Report:
{report}
-----------------------
Based on the first part feedback, refine the second part, which is the report you wrote. Use web search when necessary to confirm some information.
'''

    agent, tool_name = create_agent(llm, google_search, agent_usage.set_up_agent, profile)
    refine_report = agent_response(agent, tool_name, prompt)

    return refine_report

def fill_in_table(report, section_name, gene_name, disease_name):
    llm = run_section.testChat()
    google_search = tools.google_search

    prompt = report
    prompt += '''
    ------------------------------------
    Please ensure the report is comprehensive. Search for more information to fill in the table. 

    This {section_name} report is about gene: {gene_name} for disease {disease_name}.  

    Please ensure the information you input is correct before you fill in the table. Don't put in the information that you are unsure if is correct.
    **Be aware that don't hallucinate and put wrong stuff.**
    '''.format(section_name = section_name, gene_name = gene_name, disease_name = disease_name)

    agent, tool_name = create_agent(llm, google_search, agent_usage.set_up_agent, profile = agent_instructions.genetic_evidence_finder_profile())
    fill_in_table = agent_response(agent, tool_name, prompt)

    return fill_in_table