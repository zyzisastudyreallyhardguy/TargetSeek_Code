import os

import time
import logging
from Report_Generation_AgentAnalyst.tools import remove_references, clean_up_blank_lines, get_gene_info, get_drug_info_for_target, load_md_report
import time

from langchain_openai import ChatOpenAI
from langchain import ConversationChain
from langchain.agents import AgentExecutor
from Report_Generation_AgentAnalyst.tools import google_search, markdown_report, markdown_report_section

from Report_Generation_AgentAnalyst.agent_instructions import prompt_note, genetic_evidence_finder_profile, mechanism_of_action_finder_profile, experiment_data_finder_profile, invitro_invivo_experiment_designer_profile, target_gene_safety_evaluation_expert_profile,competitive_edge_expert_profile, druggability_evaluation_expert_profile, gene_comparison_agent,human_tissue_distribution_finder_profile, genetic_evidence_conclusion_analyser

from Report_Generation_AgentAnalyst.agent_usage import set_up_agent
from Report_Generation_AgentAnalyst.prompt_library import moa_promot, in_vitro_vivo_promot, assay_prompt, competitive_prompt, safety_prompt

# change directory to the current directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

#initialize LLM
def testChat(model_name = 'gpt-4o-2024-05-13'):
    # Verify OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OpenAI API key not configured. Please run setup_api_keys() first.")
        
    if 'o1-mini' in model_name:
        model = ChatOpenAI(
            model_name=model_name,
            temperature = 1
        )
    else:
        model = ChatOpenAI(
            max_tokens=4096,
            model_name='gpt-4o-2024-05-13'
        )
    return model

def directory_set_up():
    # Get the absolute path of the current working directory
    current_dir = os.getcwd()

    # Navigate up until finding TargetSeek_Code directory
    base_dir = current_dir
    while os.path.basename(base_dir) != "TargetSeek_Code" and base_dir != os.path.dirname(base_dir):
        base_dir = os.path.dirname(base_dir)

    # Check if we found TargetSeek_Code
    if os.path.basename(base_dir) == "TargetSeek_Code":
        working_dir = base_dir
    else:
        # Fallback if TargetSeek_Code not found in path
        raise ValueError("TargetSeek_Code directory not found in the path hierarchy")
    return working_dir

def conversation(llm, user_input):
    conversation = ConversationChain(llm=llm)
    response = conversation(user_input)
    return response['response']

# Genetic Evidence
def genetic_evidence(gene_name, disease_name, model='gpt4'):

    llm = testChat(model_name=model)

    google_tool = google_search()
    tool_name = [google_tool]

    '''create genetic_evidence_finder'''
    genetic_evidence_finder = set_up_agent(llm, tool_name, genetic_evidence_finder_profile(), model)
    genetic_evidence_agent_executor = AgentExecutor(agent=genetic_evidence_finder, tools=tool_name, verbose=True)

    user_input = '''{gene_name} gain of function mutation for {disease_name}''' + prompt_note()
    user_input = user_input.format(gene_name=gene_name, disease_name=disease_name)
    chat_history = []
    output = list(genetic_evidence_agent_executor.stream({"input": user_input, "chat_history":chat_history}))

    gof_content = output[-1]['output']

    markdown_report_section(gene_name, disease_name, 'gof', gof_content)

    user_input = '''{gene_name} loss of function mutation for {disease_name}''' + prompt_note()
    user_input = user_input.format(gene_name=gene_name, disease_name=disease_name)
    chat_history = []
    output = list(genetic_evidence_agent_executor.stream({"input": user_input, "chat_history":chat_history}))

    lof_content = output[-1]['output']

    markdown_report_section(gene_name, disease_name, 'lof', lof_content)

    genetic_evidence_analyser = set_up_agent(llm, tool_name, genetic_evidence_conclusion_analyser(), model)
    genetic_evidence_analyser_agent_executor = AgentExecutor(agent=genetic_evidence_analyser, tools=tool_name, verbose=True)

    user_input = '''The gathered genetic evidence information of {gene_name} for {disease_name} is as follows:'''
    user_input += gof_content + '\n' + '\n' + lof_content
    user_input += '''Please analyze the genetic evidence of {gene_name} for {disease_name}''' + prompt_note()
    user_input = user_input.format(gene_name=gene_name, disease_name=disease_name)
    chat_history = []
    output = list(genetic_evidence_analyser_agent_executor.stream({"input": user_input, "chat_history":chat_history}))

    analysis = output[-1]['output']

    markdown_report_section(gene_name, disease_name, 'analysis', analysis)

    return_content = gof_content + '\n' + '\n' + lof_content + '\n' + analysis

    return return_content, gof_content, lof_content, analysis

# Human Tissue Distribution
def human_tissue_distribution(gene_name, disease_name, model='gpt4'):

    llm = testChat()

    google_tool = google_search()
    tool_name = [google_tool]

    '''create human_tissue_distribution_finder'''
    human_tissue_distribution_finder = set_up_agent(llm, tool_name, human_tissue_distribution_finder_profile(), model)

    human_tissue_distribution_agent_executor = AgentExecutor(agent=human_tissue_distribution_finder, tools=tool_name, verbose=True)

    user_input = '''{gene_name} tissue specificity for {disease_name}''' + prompt_note()
    user_input = user_input.format(gene_name=gene_name, disease_name=disease_name)
    # split gene_name by '_' get the first element
    gene_name_search = gene_name.split('_')[0]
    tissue_info = get_gene_info(gene_name_search)
    user_input += tissue_info
    user_input += '''please analysis {gene_name} tissue specificity for {disease_name}''' + prompt_note()
    user_input = user_input.format(gene_name=gene_name, disease_name=disease_name)
    chat_history = []
    output = list(human_tissue_distribution_agent_executor.stream({"input": user_input, "chat_history":chat_history}))

    return tissue_info + '\n' + output[-1]['output']

# Mechanism of Action
def mechanism_of_action(gene_name, disease_name, model='gpt4'):

    llm = testChat()

    google_tool = google_search()
    tool_name = [google_tool]

    '''create mechanism_of_action_finder'''
    mechanism_of_action_finder = set_up_agent(llm, tool_name, mechanism_of_action_finder_profile(), model)

    mechanism_of_action_agent_executor = AgentExecutor(agent=mechanism_of_action_finder, tools=tool_name, verbose=True)

    # user_input = '''{gene_name}'s mechanism of action for {disease_name}''' + prompt_note()
    user_input = moa_promot(gene_name, disease_name) + prompt_note()
    user_input = user_input.format(gene_name=gene_name, disease_name=disease_name)
    chat_history = []
    output = list(mechanism_of_action_agent_executor.stream({"input": user_input, "chat_history":chat_history}))

    return output[-1]['output']

# In vitro/In vivo Experimental Evidence
def invitro_vivo(gene_name, disease_name, model='gpt4'):

    llm = testChat()

    google_tool = google_search()
    tool_name = [google_tool]

    '''create experiment_data_finder'''
    experiment_data_finder = set_up_agent(llm, tool_name, experiment_data_finder_profile(), model)

    experiment_data_agent_executor = AgentExecutor(agent=experiment_data_finder, tools=tool_name, verbose=True)

    # user_input = '''**Gene name:{gene_name}** in vitro and in vivo data for {disease_name}''' + prompt_note()
    user_input = in_vitro_vivo_promot(gene_name, disease_name) + prompt_note()
    user_input = user_input.format(gene_name=gene_name, disease_name=disease_name)
    chat_history = []
    output = list(experiment_data_agent_executor.stream({"input": user_input, "chat_history":chat_history}))

    return output[-1]['output']

# Assayability
def invitro_invivo_exp_design(gene_name, disease_name, model='gpt4'):

    llm = testChat()

    google_tool = google_search()
    tool_name = [google_tool]

    '''create invitro_invivo_experiment_designer'''
    invitro_invivo_experiment_designer = set_up_agent(llm, tool_name, invitro_invivo_experiment_designer_profile(), model)

    invitro_invivo_experiment_designer_agent_executor = AgentExecutor(agent=invitro_invivo_experiment_designer, tools=tool_name, verbose=True)

    # user_input = '''{gene_name} in vitro and in vivo experiment design for {disease_name}''' + prompt_note()
    user_input = assay_prompt(gene_name, disease_name) + prompt_note()
    user_input = user_input.format(gene_name=gene_name, disease_name=disease_name)
    chat_history = []
    output = list(invitro_invivo_experiment_designer_agent_executor.stream({"input": user_input, "chat_history":chat_history}))

    return output[-1]['output']

def safety_evaluation(gene_name, disease_name, model='gpt4'):

    llm = testChat()

    google_tool = google_search()
    tool_name = [google_tool]


    if gene_name.lower().split('_')[0] != 'itga4'.lower():
        gene_name = gene_name.lower().split('_')[0]
    elif gene_name.lower().split('_')[0] == 'itga4'.lower():
        gene_name = 'itga4_itgb7'
    
    cwd_path = directory_set_up() + '/Report_Generation_AgentAnalyst/'
    directory = cwd_path + 'reports/' + disease_name.lower() + '/' + gene_name.lower() + '/'

    #load genetic_evidence_report
    file_section_name = 'report_' + gene_name.lower() + '_' + 'in_vitro_or_vivo_data' + '.md'

    with open(directory + file_section_name, 'r') as f:
        invitro_invivo = f.read()

    '''create target_gene_safety_evaluation_expert'''
    target_gene_safety_evaluation_expert = set_up_agent(llm, tool_name, target_gene_safety_evaluation_expert_profile(), model)

    target_gene_safety_evaluation_expert_agent_executor = AgentExecutor(agent=target_gene_safety_evaluation_expert, tools=tool_name, verbose=True)

    # user_input='''
    # Please find out if there is any safety issues associated with the gene {gene_name}. 
    # Based on this information, we can conclude if {gene_name} is a good target for {disease_name} treatment.
    # If there is any safety issues, it would not be a good target.
    # You need to search and then based on the search results, analyze the safety of {gene_name}.
    # ''' + prompt_note()
    gene_name_to_search = gene_name.split('_')[0]
    if '-' in gene_name_to_search:
        pipeline_info = None
    else:
        pipeline_info = get_drug_info_for_target(gene_name_to_search)
    print(pipeline_info)
    if pipeline_info is not None:
        # user_input = '''Here are some retrieved information about the clinical pipelines for {gene_name}:'''
        # user_input += pipeline_info + '----------------\n'
        user_input = '''Here are some retrieved information about the clinical pipelines. Be careful about if the pipelines are corresponding to the target gene {gene_name} Ignore those not related:'''.format(gene_name=gene_name)
        user_input += pipeline_info + '----------------\n'
        user_input = '''Check this information one by one using search engine to find out the following information:
        1. if these pipelines are related to the target gene {gene_name} and the disease. {disease_name}. 
        2. You can think and validate their actual clinical phases based on your knowledge or search.
        Excludes those pipelines not for {disease_name}
        \n'''.format(gene_name=gene_name, disease_name=disease_name)
        print(user_input)
    else:
        user_input = ''
    # add in vitro and in vivo data
    user_input += '***In vitro and in vivo data***\n'
    user_input += invitro_invivo + '\n'
    user_input += safety_prompt(gene_name, disease_name) + prompt_note()

    user_input = user_input.format(gene_name=gene_name, disease_name=disease_name)
    chat_history = []
    output = list(target_gene_safety_evaluation_expert_agent_executor.stream({"input": user_input, "chat_history":chat_history}))

    return output[-1]['output']

# def safety_evaluation(gene_name, disease_name, model='gpt4'):

#     llm = testChat()

#     google_tool = google_search()
#     tool_name = [google_tool]

#     '''create target_gene_safety_evaluation_expert'''
#     target_gene_safety_evaluation_expert = set_up_agent(llm, tool_name, target_gene_safety_evaluation_expert_profile(), model)

#     target_gene_safety_evaluation_expert_agent_executor = AgentExecutor(agent=target_gene_safety_evaluation_expert, tools=tool_name, verbose=True)

#     # user_input='''
#     # Please find out if there is any safety issues associated with the gene {gene_name}. 
#     # Based on this information, we can conclude if {gene_name} is a good target for {disease_name} treatment.
#     # If there is any safety issues, it would not be a good target.
#     # You need to search and then based on the search results, analyze the safety of {gene_name}.
#     # ''' + prompt_note()
#     gene_name_to_search = gene_name.split('_')[0]
#     if '-' in gene_name_to_search:
#         pipeline_info = None
#     else:
#         pipeline_info = get_drug_info_for_target(gene_name_to_search)
#     print(pipeline_info)
#     if pipeline_info is not None:
#         # user_input = '''Here are some retrieved information about the clinical pipelines for {gene_name}:'''
#         # user_input += pipeline_info + '----------------\n'
#         user_input = '''Here are some retrieved information about the clinical pipelines. Be careful about if the pipelines are corresponding to the target gene {gene_name} Ignore those not related:'''.format(gene_name=gene_name)
#         user_input += pipeline_info + '----------------\n'
#         user_input = '''Check this information one by one using search engine to find out the following information:
#         1. if these pipelines are related to the target gene {gene_name} and the disease. {disease_name}. 
#         2. You can think and validate their actual clinical phases based on your knowledge or search.
#         Excludes those pipelines not for {disease_name}
#         \n'''.format(gene_name=gene_name, disease_name=disease_name)
#         print(user_input)
#     else:
#         user_input = ''
#     user_input += safety_prompt(gene_name, disease_name) + prompt_note()
#     user_input.format(gene_name=gene_name, disease_name=disease_name)

#     user_input = user_input.format(gene_name=gene_name, disease_name=disease_name)
#     chat_history = []
#     output = list(target_gene_safety_evaluation_expert_agent_executor.stream({"input": user_input, "chat_history":chat_history}))

#     return output[-1]['output']

def competitive_edge(gene_name, disease_name, model='gpt4'):

    llm = testChat()

    google_tool = google_search()
    tool_name = [google_tool]
    

    '''create competitive_edge_expert'''
    competitive_edge_expert = set_up_agent(llm, tool_name, competitive_edge_expert_profile(), model)

    competitive_edge_expert_agent_executor = AgentExecutor(agent=competitive_edge_expert, tools=tool_name, verbose=False)

    # user_input = '''Please analyze the competitive edge of {gene_name} in {disease_name} treatment and list all the clinical/pre-clinical pipelines around the queried gene. 
    # If there is no pipeline, then conclude this is a first-in-class target.''' + prompt_note()
    gene_name_to_search = gene_name.split('_')[0]
    if '-' in gene_name_to_search:
        pipeline_info = None
    else:
        pipeline_info = get_drug_info_for_target(gene_name_to_search)

    '''
    Please be aware that this information may not be accurate and can be out of date! 
    '''
    
    if pipeline_info is not None:
        user_input = '''Here are some retrieved information about the clinical pipelines. Be careful about if the pipelines are corresponding to the target gene {gene_name} Ignore those not related:'''.format(gene_name=gene_name)
        user_input += pipeline_info + '----------------\n'
        user_input = '''Check this information one by one using search engine to find out the following information:
        1. if these pipelines are related to the target gene {gene_name} and the disease. {disease_name}. 
        2. You can think and validate their actual clinical phases based on your knowledge or search.
        Excludes those pipelines not for {disease_name}
        \n'''.format(gene_name=gene_name, disease_name=disease_name)
        print(user_input)
    else:
        user_input = ''
    user_input += competitive_prompt(gene_name, disease_name) + prompt_note()
    user_input = user_input.format(gene_name=gene_name, disease_name=disease_name)

    chat_history = []
    output = list(competitive_edge_expert_agent_executor.stream({"input": user_input, "chat_history":chat_history}))

    return output[-1]['output']

def druggability(gene_name, disease_name, directory = '', model='gpt4'):
    if gene_name.lower().split('_')[0] != 'itga4'.lower():
        gene_name = gene_name.lower().split('_')[0]
    elif gene_name.lower().split('_')[0] == 'itga4'.lower():
        gene_name = 'itga4_itgb7'
        directory = 'reports/' + disease_name.lower() + '/' + gene_name.lower() + '/'

    print(os.getcwd())

    llm = testChat()

    google_tool = google_search()
    tool_name = [google_tool]

    druggability_evaluation_expert = set_up_agent(llm,tool_name, druggability_evaluation_expert_profile(), model)
    druggability_evaluation_expert_agent_executor = AgentExecutor(agent=druggability_evaluation_expert, tools=tool_name, verbose=True)

    # load genetic_evidence_report
    file_section_name = 'report_' + gene_name.lower() + '_' + 'genetic_evidence' + '.md'

    with open(directory + file_section_name, 'r') as f:
        genetic_evidence = f.read()
    
    # load mechanism_of_action_report
    file_section_name = 'report_' + gene_name.lower() + '_' + 'mechanism_of_action' + '.md'

    with open(directory + file_section_name, 'r') as f:
        mechanism_of_action = f.read()

    # load invitro_invivo_report
    file_section_name = 'report_' + gene_name.lower() + '_' + 'in_vitro_or_vivo_data' + '.md'

    with open(directory + file_section_name, 'r') as f:
        invitro_invivo = f.read()
    
    # # load competitive edge report
    # file_section_name = 'report_' + gene_name.lower() + '_' + 'competitive_edge' + '.md'

    # with open(directory + file_section_name, 'r') as f:
    #     competitive_edge = f.read()

    # load human tissue distribution report
    file_section_name = 'report_' + gene_name.lower() + '_' + 'human_tissue_distribution' + '.md'

    with open(directory + file_section_name, 'r') as f:
        human_tissue_distribution = f.read()

    user_input = '***Genetic Evidence***\n' + genetic_evidence + '\n'  + '***Mechanism of Action***\n'  + mechanism_of_action + '\n' +  '***In vitro/In vivo Experiment***\n' + invitro_invivo + '\n' + '***Human Tissue Distribution***\n' + human_tissue_distribution + '\n'

    clean_user_input = remove_references(user_input)
    clean_user_input = clean_up_blank_lines(clean_user_input)

    query = '''
    ----------------------------------
    Based on the information above, please find out the suitable modality to target {gene_name} for {disease} treatment.
    You need to list out all modality options and provide the rationale for each option.
    Then conclude what modality of drug you think are appropriate to choose for targeting this gene.
    '''
    query = query.format(gene_name=gene_name, disease=disease_name)

    user_input = clean_user_input + query
    chat_history = []
    output = list(druggability_evaluation_expert_agent_executor.stream({"input": user_input, "chat_history":chat_history}))

    return output[-1]['output']

def generate_all(gene_name, disease_name, directory = '', model_name = 'chatgpt-4o-latest'):
    generate_all = False
    if gene_name.lower().split('_')[0] != 'itga4'.lower():
        gene_name = gene_name.lower().split('_')[0]
    elif gene_name.lower().split('_')[0] == 'itga4'.lower():
        gene_name = 'itga4_itgb7'
    disease_name = disease_name.lower()
    cwd_path = directory_set_up() + '/Report_Generation_AgentAnalyst/'
    directory = cwd_path + 'reports/' + disease_name + '/' + gene_name + '/'
    # if the document exists, skip the generation
    if not os.path.exists(directory + 'report_' + gene_name + '_genetic_evidence.md'):
        #generate genetic evidence
        genetic_evidence_report, gof, lof, analysis = genetic_evidence(gene_name, disease_name, model_name)
        markdown_report_section(gene_name, disease_name, 'genetic evidence', genetic_evidence_report)
    else:
        gof = load_md_report(directory + 'report_' + gene_name + '_gof.md')
        lof = load_md_report(directory + 'report_' + gene_name + '_lof.md')
        analysis = load_md_report(directory + 'report_' + gene_name + '_analysis.md')
    if not os.path.exists(directory + 'report_' + gene_name + '_human_tissue_distribution.md'):
        #generate human tissue distribution
        human_tissue_distribution_report = human_tissue_distribution(gene_name, disease_name, model_name)
        markdown_report_section(gene_name, disease_name, 'human tissue distribution', human_tissue_distribution_report)
    else:
        human_tissue_distribution_report = load_md_report(directory + 'report_' + gene_name + '_human_tissue_distribution.md')
    if not os.path.exists(directory + 'report_' + gene_name + '_mechanism_of_action.md'):
        #generate mechanism of action
        mechanism_of_action_report = mechanism_of_action(gene_name, disease_name, model_name)
        markdown_report_section(gene_name, disease_name, 'mechanism of action', mechanism_of_action_report)
    else:
        mechanism_of_action_report = load_md_report(directory + 'report_' + gene_name + '_mechanism_of_action.md')
    if not os.path.exists(directory + 'report_' + gene_name + '_in_vitro_or_vivo_data.md'):
        #generate invitro_invivo
        invitro_invivo_report = invitro_vivo(gene_name, disease_name, model_name)
        markdown_report_section(gene_name, disease_name, 'in vitro or vivo data', invitro_invivo_report)
    else:
        invitro_invivo_report = load_md_report(directory + 'report_' + gene_name + '_in_vitro_or_vivo_data.md')
    if not os.path.exists(directory + 'report_' + gene_name + '_assays.md'):
        #generate invitro_invivo_exp_design
        invitro_invivo_exp_design_report = invitro_invivo_exp_design(gene_name, disease_name, model_name)
        markdown_report_section(gene_name, disease_name, 'assays', invitro_invivo_exp_design_report)
    else:
        invitro_invivo_exp_design_report = load_md_report(directory + 'report_' + gene_name + '_assays.md')
    if not os.path.exists(directory + 'report_' + gene_name + '_competitive_edge.md'):
        #generate competitive edge
        competitive_edge_report = competitive_edge(gene_name, disease_name, model_name)
        markdown_report_section(gene_name, disease_name, 'competitive edge', competitive_edge_report)
    else:
        competitive_edge_report = load_md_report(directory + 'report_' + gene_name + '_competitive_edge.md')
    if not os.path.exists(directory + 'report_' + gene_name + '_safety.md'):
        #generate safety evaluation
        safety_evaluation_report = safety_evaluation(gene_name, disease_name, model_name)
        markdown_report_section(gene_name, disease_name, 'safety', safety_evaluation_report)
    else:
        safety_evaluation_report = load_md_report(directory + 'report_' + gene_name + '_safety.md')
    if not os.path.exists(directory + 'report_' + gene_name + '_druggability.md'):
        #generate druggability
        druggability_report = druggability(gene_name, disease_name, directory, model_name)
        markdown_report_section(gene_name, disease_name, 'druggability', druggability_report)
    else:
        druggability_report = load_md_report(directory + 'report_' + gene_name + '_druggability.md')
    if not os.path.exists(directory + 'report_' + gene_name + '_all.md'):
        #markdown report
        markdown_report(gene_name, disease_name, gof, lof, analysis, mechanism_of_action_report, invitro_invivo_report, druggability_report, competitive_edge_report, invitro_invivo_exp_design_report, safety_evaluation_report, human_tissue_distribution_report)
    
    print(gene_name + ' is processed.')

    generate_all = True
    return generate_all

def update_gene_report(gene_name, disease_name):
    if gene_name.lower().split('_')[0] != 'itga4'.lower():
        gene_name = gene_name.lower().split('_')[0]
    elif gene_name.lower().split('_')[0] == 'itga4'.lower():
        gene_name = 'itga4_itgb7'
    gene_name = gene_name.lower()
    disease_name = disease_name.lower()
    directory = 'reports/' + gene_name + '/'
    #load md files 
    gof = load_md_report(directory + 'report_' + gene_name + '_gof.md')
    lof = load_md_report(directory + 'report_' + gene_name + '_lof.md')
    analysis = load_md_report(directory + 'report_' + gene_name + '_analysis.md')

    human_tissue_distribution_report = load_md_report(directory + 'report_' + gene_name + '_human_tissue_distribution.md')
    mechanism_of_action_report = load_md_report(directory + 'report_' + gene_name + '_mechanism_of_action.md')
    invitro_invivo_report = load_md_report(directory + 'report_' + gene_name + '_in_vitro_or_vivo_data.md')
    invitro_invivo_exp_design_report = load_md_report(directory + 'report_' + gene_name + '_assays.md')
    competitive_edge_report = load_md_report(directory + 'report_' + gene_name + '_competitive_edge.md')
    safety_evaluation_report = load_md_report(directory + 'report_' + gene_name + '_safety.md')
    druggability_report = load_md_report(directory + 'report_' + gene_name + '_druggability.md')

    #markdown report
    markdown_report(gene_name, disease_name, gof, lof, analysis, mechanism_of_action_report, invitro_invivo_report, druggability_report, competitive_edge_report, invitro_invivo_exp_design_report, safety_evaluation_report, human_tissue_distribution_report)

def compare_gene(gene_1, gene_2):
    # load gene_report
    directory = 'comparison_report/'
    gene_1 = gene_1.lower()
    gene_2 = gene_2.lower()

    file_section_name = 'report_' + gene_1 + '_all.txt'
    with open(directory + file_section_name, 'r') as f:
        gene_1_report = f.read()
    
    file_section_name = 'report_' + gene_2 + '_all.txt'
    with open(directory + file_section_name, 'r') as f:
        gene_2_report = f.read()

    llm = testChat()

    google_tool = google_search()
    tool_name = [google_tool]

    gene_comparison = set_up_agent(llm, tool_name, gene_comparison_agent(gene_1, gene_2))

    gene_comparison_agent_executor = AgentExecutor(agent=gene_comparison, tools=tool_name, verbose=True)

    user_input = 'First Report \n' + gene_1_report + '\n ------ \n' + 'Second Report \n' + gene_2_report

    chat_history = []
    output = list(gene_comparison_agent_executor.stream({"input": user_input, "chat_history":chat_history}))

    # save the results in markdown
    file_section_name = 'report_' + gene_1 + '_' + gene_2 + '_comparison.txt'

    with open(directory + file_section_name, 'w') as f:
        f.write(output[-1]['output'])

    return output[-1]['output']

def generate_with_progress(gene_name, disease, model_name = 'chatgpt-4o-latest'):
    # try:
    generate_all(gene_name, disease,'', model_name)
    time.sleep(1)  # Simulating some processing time
    # except Exception as e:
    #     logging.error(f"Error processing gene {gene_name} for disease {disease}: {e}")

# direct gene_comparison with GPT4
# if __name__ == '__main__':
    # gene_list = ['GPAM', 'PSD3', 'CIDEB', 'INHBE', 'DGAT2']
    # # compare these genes in pair using compare_gene() function
    # # show progress bar using tqdm
    # from tqdm import tqdm
    # for i in tqdm(range(len(gene_list))):
    #     for j in range(i+1, len(gene_list)):
    #         compare_gene(gene_list[i], gene_list[j])
    #         time.sleep(1)

# in batch report generation
if __name__ == '__main__':
    from joblib import Parallel, delayed
    from tqdm import tqdm
    import time

    gene_list = ['HMGA1', 'PIK3R1', 'SEC16B', 'CHI3L1', 'ANGPTL4']
    # Wrapping the generate_all function to add the tqdm progress bar
    # def generate_with_progress(gene_name, disease):
    #     try:
    #         generate_all(gene_name, disease)
    #         time.sleep(1)  # Simulating some processing time
    #     except Exception as e:
    #         logging.error(f"Error processing gene {gene_name} for disease {disease}: {e}")

    # Using tqdm with joblib for parallel execution with progress bar
    Parallel(n_jobs=-1)(delayed(generate_with_progress)(gene_name, 'NASH', 'gpt4') for gene_name in tqdm(gene_list))
