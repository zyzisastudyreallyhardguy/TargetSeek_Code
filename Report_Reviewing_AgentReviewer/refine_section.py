import sys
import os

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

# Add the parent directory to the sys.path
sys.path.append(directory_set_up())
from tern_self_evolution.functions import fill_in_table
import functions

from concurrent.futures import ThreadPoolExecutor

def save_refined_reports(gene_name, disease_name, section_names):
    for section_name in section_names:
        if section_name == 'genetic_evidence':
            genetic_evidence = load_original_report(gene_name, disease_name, section_name)
        elif section_name == 'mechanism_of_action':
            moa_content = load_original_report(gene_name, disease_name, section_name)
        elif section_name == 'in_vitro_or_vivo_data':
            invitro_invivo_exp_content = load_original_report(gene_name, disease_name, section_name)
        elif section_name == 'druggability':
            druggability_content = load_original_report(gene_name, disease_name, section_name)
        elif section_name == 'competitive_edge':
            competitive_edge_content = load_original_report(gene_name, disease_name, section_name)
        elif section_name == 'assays':
            assay_design_content = load_original_report(gene_name, disease_name, section_name)
        elif section_name == 'safety':
            safety_content = load_original_report(gene_name, disease_name, section_name)
            
    human_tissue_distribution_content = load_original_report(gene_name, disease_name, 'human_tissue_distribution')

    markdown_report_all(gene_name, disease_name, genetic_evidence, moa_content, invitro_invivo_exp_content, druggability_content, competitive_edge_content, assay_design_content, safety_content, human_tissue_distribution_content)

def markdown_report_all(gene_name, disease_name, genetic_evidence, moa_content, invitro_invivo_exp_content, druggability_content, competitive_edge_content, assay_design_content, safety_content, human_tissue_distribution_content):
    path = directory_set_up() + '/feedback_repo/revised_reports_complete/refine_reports/' + disease_name + '/' + gene_name.lower() + '/'
    if not os.path.exists(path):
        os.makedirs(path)
    with open(path + 'report_' + gene_name.lower() + '_all.md', 'w') as f:
        gene_name = gene_name.upper()
        disease_name = disease_name.upper()
        f.write('# Gene Report\n')
        f.write('## Gene Name: ' + gene_name + '\n')
        f.write('## Disease Name: ' + disease_name + '\n')
        f.write('### 1.Genetic Evidence\n' + genetic_evidence + '\n')
        f.write('### 2.Mechanism of Action\n' + moa_content + '\n')
        f.write('### 3.Human Tissue Distribution\n' + human_tissue_distribution_content + '\n')
        f.write('### 4.In vitro/In vivo Experiment\n' + invitro_invivo_exp_content + '\n')
        f.write('### 5.Druggability Evaluation\n' + druggability_content + '\n')
        f.write('### 6.Competitive Edge\n' + competitive_edge_content + '\n')
        f.write('### 7.Assay Design\n' + assay_design_content + '\n')
        f.write('### 8.Safety Evaluation\n' + safety_content + '\n')

def load_original_report(gene_name, disease_name, section_name, report_path=''):
    if disease_name == 'atherosclerosis':
        folder_name = 'reports_atherosclerosis_105'
    elif disease_name == 'nash':
        folder_name = 'reports_nash'
    elif disease_name =='inflammatory_bowel_disease':
        folder_name = 'reports_ibd'
    full_report_path = os.path.join(report_path, folder_name, gene_name, f'report_{gene_name}_{section_name}.md')
    with open(full_report_path, 'r') as f:
        report = f.read()
    return report

def load_refined_report(gene_name, disease_name, section_name, report_path=''):
    with open(os.path.join(report_path, disease_name, gene_name, f'{gene_name}_{section_name}_refine_reports_{gene_name}_{section_name}' + '.md'), 'r') as f:
        report = f.read()
    return report

def process_section(gene_name, disease_name, section_name, save_dir):
    """
    Process a single section by loading the report and running the inner loop.
    """
    complete_report = load_original_report(gene_name, disease_name, section_name)
    
    return inner_loop_together_withMP(
        gene_name,
        disease_name,
        report=None,
        complete_report=complete_report,
        section_name=section_name,
        prefix=gene_name + '_' + section_name,
        mistake_pool_file='tern_self_evolution/mistake_pool/mistake_pool.json',
        save_dir=save_dir,
    )

def run_parallel_refinement_for_a_gene(gene_name, disease_name, sections, save_dir):
    """
    Run the process_section function in parallel for each section.
    """
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_section, gene_name, disease_name, section, save_dir) for section in sections]
        results = [future.result() for future in futures]
    return results

def inner_loop_together_withMP(
        gene_name,
        disease_name,
        report = None,
        complete_report = None,
        questions = None,
        section_name = 'genetic_evidence',
        prefix = 'test_bhy',
        mistake_pool_file = 'mistake_pool/mistake_pool.json',
        save_dir = directory_set_up() + '/Report_Reviewing_AgentReviewer/' + '/feedback_repo/'
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
            with open(os.path.join(save_dir, res_type, disease_name, gene_name, f"report_{gene_name.lower()}_{section_name}.md"), 'w') as f:
                f.write(res)
        else:
            with open(os.path.join(save_dir, res_type, disease_name, gene_name, f"{prefix}_{res_type}_{gene_name}_{section_name}.md"), 'w') as f:
                f.write(res)
    return complete_report, refine_report, questions,feedback_input,summarized_feedback