import sys
import os
import json
from Report_Generation_AgentAnalyst.run_section import testChat, directory_set_up

# # Add the parent directory to the sys.path
sys.path.append(directory_set_up())

from Report_Generation_AgentAnalyst.tools import load_md_report, google_search, markdown_report_section

from Report_Reviewing_AgentReviewer.functions import fill_in_table
from Report_Reviewing_AgentReviewer import functions
from Report_Generation_AgentAnalyst.agent_usage import set_up_agent
from langchain.agents import AgentExecutor

from Report_Generation_AgentAnalyst.agent_instructions import genetic_evidence_conclusion_analyser, prompt_note

from concurrent.futures import ThreadPoolExecutor

def save_refined_report_all_sections(md_gene_name, disease_name, save_path):
    gene_name = stand_gene_name(md_gene_name)

    analysis_path = os.path.join(directory_set_up() + '/Report_Generation_AgentAnalyst','reports', disease_name, gene_name, f'report_{gene_name}_analysis.md')

    human_tissue_distribution_path = os.path.join(directory_set_up() + '/Report_Generation_AgentAnalyst','reports', disease_name, gene_name, f'report_{gene_name}_human_tissue_distribution.md')
    
    gain_of_function = load_md_report(os.path.join(save_path,'refine_reports', disease_name, gene_name,
                                                   f'report_{gene_name}_gain_of_function.md'))
    loss_of_function = load_md_report(os.path.join(save_path,'refine_reports', disease_name, gene_name,
                                                   f'report_{gene_name}_loss_of_function.md'))
    analysis = load_md_report(os.path.join(analysis_path))
    mechanism_of_action = load_md_report(os.path.join(save_path,'refine_reports', disease_name, gene_name,
                                                   f'report_{gene_name}_mechanism_of_action.md'))
    in_vitro_or_vivo_data = load_md_report(os.path.join(save_path,'refine_reports', disease_name, gene_name,
                                                   f'report_{gene_name}_in_vitro_or_vivo_data.md'))
    druggability = load_md_report(os.path.join(save_path,'refine_reports', disease_name, gene_name,
                                                   f'report_{gene_name}_druggability.md'))
    competitive_edge = load_md_report(os.path.join(save_path,'refine_reports', disease_name, gene_name,
                                                   f'report_{gene_name}_competitive_edge.md'))
    assays = load_md_report(os.path.join(save_path,'refine_reports', disease_name, gene_name,
                                                   f'report_{gene_name}_assays.md'))
    safety = load_md_report(os.path.join(save_path,'refine_reports', disease_name, gene_name,
                                                   f'report_{gene_name}_safety.md'))
    human_tissue_distribution = load_md_report(human_tissue_distribution_path)

    markdown_report_all(gene_name, disease_name, gain_of_function, loss_of_function, analysis, mechanism_of_action, in_vitro_or_vivo_data, druggability, competitive_edge, assays, safety, human_tissue_distribution, save_path)

def markdown_report_all(gene_name, disease_name, gain_of_function, loss_of_function, analysis, mechanism_of_action, in_vitro_or_vivo_data, druggability, competitive_edge, assays, safety, human_tissue_distribution, save_path):
    path = os.path.join(save_path, 'refine_reports', disease_name, gene_name)
    with open(os.path.join(path, f'report_{gene_name}_all.md'), 'w') as f:
        gene_name = gene_name.upper()
        disease_name = disease_name.upper()
        f.write('# Gene Report\n')
        f.write('## Gene Name: ' + gene_name + '\n')
        f.write('## Disease Name: ' + disease_name + '\n')
        f.write('### 1.Genetic Evidence\n')
        f.write('#### Gain of Function\n' + gain_of_function + '\n')
        f.write('#### Loss of Function\n' + loss_of_function + '\n')
        f.write(analysis + '\n' )
        f.write('### 2.Mechanism of Action\n' + mechanism_of_action + '\n')
        f.write('### 3.Human Tissue Distribution\n' + human_tissue_distribution + '\n')
        f.write('### 4.In vitro/In vivo Experiment\n' + in_vitro_or_vivo_data + '\n')
        f.write('### 5.Druggability Evaluation\n' + druggability + '\n')
        f.write('### 6.Competitive Edge\n' + competitive_edge + '\n')
        f.write('### 7.Assay Design\n' + assays + '\n')
        f.write('### 8.Safety Evaluation\n' + safety + '\n')


def load_refined_report(gene_name, disease_name, section_name, report_path=directory_set_up() + 'Report_Reviewing_AgentReviewer/feedback_repo/refine_reports'):
    with open(os.path.join(report_path, disease_name, gene_name, f'{gene_name}_{section_name}_refine_reports_{gene_name}_{section_name}' + '.md'), 'r') as f:
        report = f.read()
    return report

def stand_section_name(short_name):
    # this is for finding output format of sections
    name_dict = {
        'lof':'loss_of_function',
        'gof':'gain_of_function',
    }
    if short_name in name_dict.keys():
        return name_dict[short_name]
    else:return short_name

def stand_gene_name(gene_name):
    if gene_name.lower().split('_')[0] != 'itga4'.lower():
        gene_name = gene_name.lower().split('_')[0]
    elif gene_name.lower().split('_')[0] == 'itga4'.lower():
        gene_name = 'itga4_itgb7'
    return gene_name

def process_section(md_gene_name, disease_name, md_section_name, save_dir, md_dir, mistake_pool_file):
    """
    Process a single section by loading the report and running the inner loop.
    """
    gene_name = stand_gene_name(md_gene_name)
    md_path = os.path.join(md_dir, disease_name, md_gene_name, f'report_{gene_name}_{md_section_name}.md')
    complete_report = load_md_report(md_path)
    section_name = stand_section_name(md_section_name)
    
    return review_section_withMP(
        gene_name,
        disease_name,
        complete_report=complete_report,
        section_name=section_name,
        prefix='',
        mistake_pool_file=mistake_pool_file,
        save_dir=save_dir,
    )


def run_parallel_refinement_for_a_gene(gene_name, disease_name, sections, save_dir, md_dir, mistake_pool_file):
    """
    Run the process_section function in parallel for each section.
    """
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_section, gene_name, disease_name, section, save_dir, md_dir, mistake_pool_file) for section in sections]
        results = [future.result() for future in futures]
    return results


def check_mistake_pool(mistake_pool_file_path):
    if not os.path.exists(mistake_pool_file_path):
        print(f'mistake pool not exists, init a new mistake pool in {mistake_pool_file_path}.')
        mistake_pool = {'Included irrelevant content to the target gene': 'The row in the table is not **directly** related to the gene of interest||Action: Delete the content.',
               'Logical error': 'A mutation cannot simultaneously be both gain of function and loss of function|| Action: You should remove one of them.',
               'Redundant reference': 'Some references are not used. ||Action: Delete the references.',
               'Incorrect reference': 'The reference provided does not support the claim made in the report|| Action: Delete the relavent content and the references, unless you find the correct one that supports the claim.'}
    
        with open(mistake_pool_file_path, 'w') as json_file:
            json.dump(mistake_pool, json_file, indent=4)


def review_section_withMP(
                        gene_name,
                        disease_name,
                        complete_report,
                        questions = None,
                        section_name = 'loss_of_section',
                        prefix = 'test_bhy',
                        mistake_pool_file = directory_set_up() + '/Report_Reviewing_AgentReviewer/mistake_pool/mistake_pool_tmp.json',
                        save_dir = directory_set_up() + '/Report_Reviewing_AgentReviewer/feedback_repo/summary_feedback_tmp/'
    
                       ):
    
    cwd_path = directory_set_up()
    mistake_pool_file = cwd_path + '/Report_Reviewing_AgentReviewer/mistake_pool/mistake_pool_tmp.json'
    save_dir = cwd_path + '/Report_Reviewing_AgentReviewer/feedback_repo/summary_feedback_tmp/'
    
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
    
    if not questions:
        questions = functions.obtain_questions(complete_report, section_name)
        
    feedbacks = functions.obtain_feedbacks_together(complete_report, questions, section_name)
    feedback_input = '/n'.join(feedbacks)
    check_mistake_pool(mistake_pool_file)
    summarized_feedback = functions.summarize_feedback_with_mistakePool(feedback_input, complete_report, gene_name, section_name, mistake_pool_file, save_dir)
    refine_report = functions.refine_report_based_on_feedback(complete_report, summarized_feedback, section_name, gene_name, disease_name)
    results = [complete_report, refine_report, questions,feedback_input,summarized_feedback]
    res_types = ['complete_reports', 'refine_reports', 'questions','feedback_input','summarized_feedback']
    # save_dir + res_type, gene_name not exist create one
    for res,res_type in zip(results, res_types):
        # if the repo doesn't exist, create one
        os.makedirs(os.path.join(save_dir, res_type, disease_name, gene_name), exist_ok=True)
        if res_type == 'refine_reports':
            markdown_report_section(gene_name, disease_name, section_name, content=res, save_file_directory= os.path.join(save_dir, res_type, disease_name, gene_name))
        else:
            with open(os.path.join(save_dir, res_type, disease_name, gene_name, f"{prefix}_{res_type}_{gene_name}_{section_name}.md"), 'w') as f:
                f.write(res)
    return complete_report, refine_report, questions,feedback_input,summarized_feedback


def post_generate_genetic_evidence_and_distribution(md_gene_name, disease_name, md_dir, save_dir = './'):

    llm = testChat()

    google_tool = google_search()
    tool_name = [google_tool]

    gene_name = stand_gene_name(md_gene_name)
    gof_path = os.path.join(md_dir, disease_name, md_gene_name, f'report_{gene_name}_gof.md')
    lof_path = os.path.join(md_dir, disease_name, md_gene_name, f'report_{gene_name}_lof.md')
    gof_content = load_md_report(gof_path)
    lof_content = load_md_report(lof_path)

    genetic_evidence_analyser = set_up_agent(llm, tool_name, genetic_evidence_conclusion_analyser())
    genetic_evidence_analyser_agent_executor = AgentExecutor(agent=genetic_evidence_analyser, tools=tool_name, verbose=True)

    user_input = f'''The gathered genetic evidence information of {md_gene_name} for {disease_name} is as follows:'''
    user_input += gof_content + '\n' + '\n' + lof_content
    user_input += f'''Please analyze the genetic evidence of {md_gene_name} for {disease_name}''' + prompt_note()
    user_input = user_input.format(md_gene_name=md_gene_name, disease_name=disease_name)
    chat_history = []
    output = list(genetic_evidence_analyser_agent_executor.stream({"input": user_input, "chat_history":chat_history}))

    analysis = output[-1]['output']

    markdown_report_section(gene_name, disease_name, 'analysis', content=analysis, save_file_directory= os.path.join(save_dir, 'refine_reports',disease_name, gene_name))

    return_content = gof_content + '\n' + '\n' + lof_content + '\n' + analysis

    markdown_report_section(gene_name, disease_name, 'genetic_evidence', content=return_content,  save_file_directory= os.path.join(save_dir, 'refine_reports',disease_name, gene_name))

    distribution_report_path = os.path.join(md_dir, disease_name, md_gene_name, f'report_{gene_name}_human_tissue_distribution.md')
    human_tissue_distribution = load_md_report(distribution_report_path)

    markdown_report_section(gene_name, disease_name, 'human_tissue_distribution', content=human_tissue_distribution, save_file_directory= os.path.join(save_dir, 'refine_reports',disease_name, gene_name))



def inner_loop_together_withMP(
        gene_name,
        disease_name,
        report = None,
        complete_report = None,
        questions = None,
        section_name = 'genetic_evidence',
        prefix = 'test_bhy',
        mistake_pool_file = 'mistake_pool/mistake_pool.json',
        save_dir = directory_set_up() + '/Report_Reviewing_AgentReviewer/feedback_repo/'
        ):

    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
    
    if not questions:
        if not complete_report:
        # fill in the table, (finding more information to fill in)
            complete_report = fill_in_table(report, section_name, gene_name, disease_name)
        # develop questions
        questions = functions.obtain_questions(complete_report, section_name)
        
    # obtain feedbacks
    feedbacks = functions.obtain_feedbacks_together(complete_report, questions, section_name)
    feedback_input = '/n'.join(feedbacks)
    # 
    summarized_feedback = functions.summarize_feedback_with_mistakePool(feedback_input, complete_report, gene_name, section_name, mistake_pool_file, save_dir)
    refine_report = functions.refine_report_based_on_feedback(complete_report, summarized_feedback, section_name, gene_name, disease_name)
    results = [complete_report, refine_report, questions,feedback_input,summarized_feedback]
    res_types = ['complete_reports', 'refine_reports', 'questions','feedback_input','summarized_feedback']

    # save_dir + res_type, gene_name not exist create one
    for res,res_type in zip(results, res_types):
        # if the repo doesn't exist, create one
        os.makedirs(os.path.join(save_dir, res_type, disease_name, gene_name), exist_ok=True)
        if res_type == 'refine_reports':
            markdown_report_section(gene_name, disease_name, section_name, content=res, save_file_directory= os.path.join(save_dir, res_type))
            # with open(os.path.join(save_dir, res_type, disease_name, gene_name, f"report_{gene_name.lower()}_{section_name}.md"), 'w') as f:
            #     f.write(res)
        else:
            with open(os.path.join(save_dir, res_type, disease_name, gene_name, f"{prefix}_{res_type}_{gene_name}_{section_name}.md"), 'w') as f:
                f.write(res)
    return complete_report, refine_report, questions,feedback_input,summarized_feedback