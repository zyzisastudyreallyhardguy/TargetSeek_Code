from Target_Scoring_AgentScorer.tools import *
from Target_Scoring_AgentScorer.instructions import *
from Target_Scoring_AgentScorer.agent_instructions import *
import concurrent.futures
import json

import concurrent.futures
import json
import os

def run_all_scoring_functions(llm, gene, disease, preferred_moa, match_moa=False, file_type='direct', no_drug_pipeline_info=True):
    functions = [
        genetic_evidence_scoring,
        differential_expression_scoring,
        moa_scoring,
        in_vitro_vivo_scoring,
        small_molecule_scoring,
        antibody_scoring,
        sirna_scoring,
        # competitiveness_scoring,
        competitiveness_small_molecule_scoring,
        competitiveness_antibody_or_sirna_scoring,
        assayability_scoring,
        target_safety_scoring,
        unmet_need_scoring,
        assayability_biomarker_scoring,
    ]

    if match_moa:
        functions.append(match_moa_scoring)

    results = {}

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_function = {}

        for fn in functions:
            if fn.__name__ == 'match_moa_scoring':
                future_to_function[executor.submit(fn, llm, gene, disease, preferred_moa, file_type)] = fn.__name__
            elif fn.__name__ in ['small_molecule_scoring', 'antibody_scoring']:
                future_to_function[executor.submit(fn, llm, gene, disease, file_type, no_drug_pipeline_info)] = fn.__name__
            else:
                future_to_function[executor.submit(fn, llm, gene, disease, file_type)] = fn.__name__


        for future in concurrent.futures.as_completed(future_to_function):
            function_name = future_to_function[future]
            try:
                result = future.result()
                results[function_name] = result
            except Exception as exc:
                results[function_name] = f'Generated an exception: {exc}'

    # Print results for debugging
    for fn_name in results:
        print(f'{fn_name}: {results[fn_name]}')

    cwd_path = directory_set_up() + '/Target_Scoring_AgentScorer'

    # Create directory if it doesn't exist
    save_path = f'{cwd_path}/scoring_result/{file_type}/json/{disease.lower()}/'
    os.makedirs(save_path, exist_ok=True)

    # Save the results to a JSON file
    with open(os.path.join(save_path, f'{gene.lower()}_{disease.lower()}.json'), 'w') as f:
        json.dump(results, f, indent=4)

    return results


def run_opentarget_scoring_functions(llm, gene, disease, preferred_moa, match_moa = False, file_type = 'tern'):
    functions = [
        target_in_clinic_scoring,
        membrane_protein_scoring,
        secreted_protein_scoring,
        ligand_binder_scoring,
        small_molecule_binder_scoring,
        chemical_probes_scoring,
        predicted_pocket_scoring,
    ]

    #if match_moa is False, remove the last function
    if match_moa:
        functions.append(match_moa_scoring)
    
    results = {}

    with concurrent.futures.ThreadPoolExecutor() as executor:
        # future_to_function = {executor.submit(fn, llm, gene, disease, file_type): fn.__name__ for fn in functions}
        future_to_function = {}

        for fn in functions:
            if fn.__name__ == 'match_moa_scoring':
                future_to_function[executor.submit(fn, llm, gene, disease, preferred_moa, file_type)] = fn.__name__
            else:
                future_to_function[executor.submit(fn, llm, gene, disease, file_type)] = fn.__name__

        for future in concurrent.futures.as_completed(future_to_function):
            function_name = future_to_function[future]
            try:
                result = future.result()
                results[function_name] = result
            except Exception as exc:
                results[function_name] = f'Generated an exception: {exc}'

    # Save the results to a JSON file
    with open('scoring_result/' + file_type + '/json/' + disease.lower() + '/' + 'opentarget/' + gene.lower() + '_' + disease.lower() + '.json', 'w') as f:
        json.dump(results, f, indent=4)

    return results

def return_chunk(gene_name, disease_name, section_name, file_type = 'direct'):
    report_chunks = get_report_chunk(gene_name, disease_name, file_type)
    report_key = chunk_key_match(section_name, report_chunks)
    return report_chunks[report_key]

def genetic_evidence_scoring(llm, gene_name, disease_name, file_type = 'direct'):
    report_chunk = return_chunk(gene_name, disease_name, 'genetic evidence', file_type)
    instruction = genetic_association_rating(gene_name, disease_name)
    return scoring(llm, report_chunk, instruction)

# def differential_expression_scoring(llm, gene_name, disease_name, file_type = 'human'):
#     report_chunk_drug = return_chunk(gene_name, 'druggability', file_type)
#     report_chunk_tissue_distribution = get_gene_info(gene_name = gene_name)
#     report_chunk = 'Druggability Report:\n' + report_chunk_drug + '\n------------------\n' + 'Tissue Distribution Report:\n' + report_chunk_tissue_distribution

#     instruction = differential_expression_rating(gene_name, disease_name)
#     return scoring(llm, report_chunk, instruction)

def differential_expression_scoring(llm, gene_name, disease_name, file_type = 'human'):
    report_chunk_tissue_distribution = return_chunk(gene_name, disease_name, 'human tissue distribution', file_type)
    print('--------report chunk----------')
    print(report_chunk_tissue_distribution)
    instruction = differential_expression_rating(gene_name, disease_name)
    print('--------instruction----------')
    print(instruction)
    scoring_result = scoring(llm, report_chunk_tissue_distribution, instruction)
    print('--------scoring result----------')
    print(scoring_result)
    return scoring_result

def moa_scoring(llm, gene_name, disease_name, file_type = 'human'):
    report_chunk_ge = return_chunk(gene_name, disease_name, 'genetic evidence', file_type)
    report_chunk_moa = return_chunk(gene_name, disease_name, 'mechanism of action', file_type)

    report_chunk = 'Genetic Evidence Report:\n' + report_chunk_ge + '\n------------------\n' + 'Mechanism of Action Report:\n' + report_chunk_moa
    instruction = moa_rating(gene_name, disease_name)
    return scoring(llm, report_chunk, instruction)

def in_vitro_vivo_scoring(llm, gene_name, disease_name, file_type = 'human'):
    report_chunk_in_vitro = return_chunk(gene_name, disease_name, 'in vitro', file_type)
    report_competitive_edge = return_chunk(gene_name, disease_name, 'competitive edge', file_type)
    report_chunk = 'In Vitro Report:\n' + report_chunk_in_vitro + '\n------------------\n' + 'Competitive Edge Report:\n' + report_competitive_edge
    print('--------report chunk----------')
    print(report_chunk)
    instruction = in_vitro_vivo_rating(gene_name, disease_name)
    print('--------instruction----------')
    print(instruction)
    scoring_result = scoring(llm, report_chunk, instruction)
    print('--------scoring result----------')
    print(scoring_result)
    return scoring_result

def small_molecule_scoring(llm, gene_name, disease_name, file_type = 'direct', no_drug_pipeline_info=True):
    report_chunk_druggability = return_chunk(gene_name, disease_name, 'druggability', file_type)
    report_chunk_competitive_edge = return_chunk(gene_name, disease_name, 'competitive edge', file_type)
    report_chunk = 'Druggability Report:\n' + report_chunk_druggability + '\n------------------\n' + 'Competitive Edge Report:\n' + report_chunk_competitive_edge
    print('--------report chunk----------')
    print(report_chunk)
    instruction = small_molecule_rating(gene_name, disease_name, no_drug_pipeline_info)
    print('--------instruction----------')
    print(instruction)
    scoring_result = scoring(llm, report_chunk, instruction)
    print('--------scoring result----------')
    print(scoring_result)
    return scoring_result

def antibody_scoring(llm, gene_name, disease_name, file_type = 'direct', no_drug_pipeline_info=True):
    report_chunk_drug = return_chunk(gene_name, disease_name, 'druggability', file_type)
    report_chunk_competitive_edge = return_chunk(gene_name, disease_name, 'competitive edge', file_type)
    report_chunk = 'Druggability Report:\n' + report_chunk_drug + '\n------------------\n' + 'Competitive Edge Report:\n' + report_chunk_competitive_edge
    print('--------report chunk----------')
    print(report_chunk)
    instruction = antibody_rating(gene_name, disease_name, no_drug_pipeline_info)
    print('--------instruction----------')
    print(instruction)
    scoring_result = scoring(llm, report_chunk, instruction)
    print('--------scoring result----------')
    print(scoring_result)
    return scoring_result

def sirna_scoring(llm, gene_name, disease_name, file_type = 'human'):
    report_chunk_drug = return_chunk(gene_name, disease_name, 'druggability', file_type)
    report_chunk_tissue_distribution = get_gene_info(gene_name = gene_name)
    report_chunk = 'Druggability Report:\n' + report_chunk_drug + '\n------------------\n' + 'Tissue Distribution Report:\n' + report_chunk_tissue_distribution
    print('--------report chunk----------')
    print(report_chunk)
    instruction = sirna_rating(gene_name, disease_name)
    print('--------instruction----------')
    print(instruction)
    scoring_result = scoring(llm, report_chunk, instruction)
    print('--------scoring result----------')
    print(scoring_result)
    return scoring_result

def competitiveness_scoring(llm, gene_name, disease_name, file_type = 'human'):
    report_chunk = return_chunk(gene_name, disease_name, 'competitive edge', file_type)
    print('--------report chunk----------')
    print(report_chunk)
    instruction = competitiveness_rating(gene_name, disease_name)
    print('--------instruction----------')
    print(instruction)
    scoring_result = scoring(llm, report_chunk, instruction)
    print('--------scoring result----------')
    print(scoring_result)
    return scoring_result

def competitiveness_small_molecule_scoring(llm, gene_name, disease_name, file_type = 'human'):
    report_chunk = return_chunk(gene_name, disease_name, 'competitive edge', file_type)
    print('--------report chunk----------')
    print(report_chunk)
    instruction = competitiveness_small_molecule_rating(gene_name, disease_name)
    print('--------instruction----------')
    print(instruction)
    scoring_result = scoring(llm, report_chunk, instruction)
    print('--------scoring result----------')
    print(scoring_result)
    return scoring_result

def competitiveness_antibody_or_sirna_scoring(llm, gene_name, disease_name, file_type = 'human'):
    report_chunk = return_chunk(gene_name, disease_name, 'competitive edge', file_type)
    print('--------report chunk----------')
    print(report_chunk)
    instruction = competitiveness_antibody_or_sirna_rating(gene_name, disease_name)
    print('--------instruction----------')
    print(instruction)
    scoring_result = scoring(llm, report_chunk, instruction)
    print('--------scoring result----------')
    print(scoring_result)
    return scoring_result

def assayability_scoring(llm, gene_name, disease_name, file_type = 'human'):
    report_chunk = return_chunk(gene_name, disease_name, 'assay design', file_type)
    instruction = assayability_rating(gene_name, disease_name)
    return scoring(llm, report_chunk, instruction)

def target_safety_scoring(llm, gene_name, disease_name, file_type = 'human'):
    report_chunk_in_vitro = return_chunk(gene_name, disease_name, 'in vitro', file_type)
    report_chunk_safety_evaluation = return_chunk(gene_name, disease_name, 'safety evaluation', file_type)
    report_chunk = 'In Vitro Report:\n' + report_chunk_in_vitro + '\n------------------\n' + 'Safety Evaluation Report:\n' + report_chunk_safety_evaluation
    print('--------report chunk----------')
    print(report_chunk)
    instruction = target_safety_rating(gene_name, disease_name)
    print('--------instruction----------')
    print(instruction)
    scoring_result = scoring(llm, report_chunk, instruction)
    print('--------scoring result----------')
    print(scoring_result)
    return scoring_result

def match_moa_scoring(llm, gene_name, disease_name, user_preferred_moa, file_type = 'human'):
    report_chunk_ge = return_chunk(gene_name, disease_name, 'genetic evidence', file_type)
    report_chunk_moa = return_chunk(gene_name, disease_name, 'mechanism of action', file_type)
    instruction = moa_match_rating(gene_name, disease_name, user_preferred_moa)
    return scoring(llm, report_chunk_moa, instruction)

def target_in_clinic_scoring(llm, gene_name, disease_name, file_type = 'human', eval_type = 'opentarget'):
    report_chunk_competitive_edge = return_chunk(gene_name, disease_name, 'competitive edge', file_type, eval_type)
    #load file from target_drug_info folder and load gene_name + _drug_info.txt
    # report_drug_info = get_drug_info(gene_name)
    report_chunk = 'Competitive Edge Report:\n' + report_chunk_competitive_edge
    instruction = target_in_clinic_rating(gene_name, disease_name)
    return scoring(llm, report_chunk, instruction)

def membrane_protein_scoring(llm, gene_name, disease_name, file_type = 'human', eval_type = 'opentarget'):
    report_chunk = return_chunk(gene_name, disease_name, 'druggability', file_type, eval_type)
    instruction = membrane_protein_rating(gene_name, disease_name)
    return scoring(llm, report_chunk, instruction)

def secreted_protein_scoring(llm, gene_name, disease_name, file_type = 'human', eval_type = 'opentarget'):
    report_chunk = return_chunk(gene_name, disease_name, 'druggability', file_type, eval_type)
    instruction = secreted_protein_rating(gene_name, disease_name)
    return scoring(llm, report_chunk, instruction)

def tissue_specificity_scoring(llm, gene_name, disease_name, file_type = 'human'):
    report_chunk_tissue_distribution = get_gene_info_expression_atlas(gene_name = gene_name)
    instruction = tissue_specificity_rating(gene_name, disease_name)
    return scoring(llm, report_chunk_tissue_distribution, instruction)

def tissue_distribution_scoring(llm, gene_name, disease_name, file_type = 'human'):
    report_chunk_tissue_distribution = get_gene_info_expression_atlas(gene_name = gene_name)
    instruction = tissue_distribution_rating(gene_name, disease_name)
    return scoring(llm, report_chunk_tissue_distribution, instruction)

def ligand_binder_scoring(llm, gene_name, disease_name, file_type = 'human'):
    report_chunk = return_chunk(gene_name, disease_name, 'druggability', file_type)
    instruction = ligand_binder_rating(gene_name, disease_name)
    return scoring(llm, report_chunk, instruction)

def small_molecule_binder_scoring(llm, gene_name, disease_name, file_type = 'human'):
    report_chunk = return_chunk(gene_name, disease_name, 'druggability', file_type)
    instruction = small_molecule_binder_rating(gene_name, disease_name)
    return scoring(llm, report_chunk, instruction)

def chemical_probes_scoring(llm, gene_name, disease_name, file_type = 'human'):
    report_chunk = return_chunk(gene_name, disease_name, 'druggability', file_type)
    instruction = chemical_probes_rating(gene_name, disease_name)
    return scoring(llm, report_chunk, instruction)

def predicted_pocket_scoring(llm, gene_name, disease_name, file_type = 'human'):
    report_chunk = return_chunk(gene_name, disease_name, 'druggability', file_type)
    instruction = predicted_pocket_rating(gene_name, disease_name)
    return scoring(llm, report_chunk, instruction)

def assayability_biomarker_scoring(llm, gene_name, disease_name, file_type = 'human'):
    report_chunk = return_chunk(gene_name, disease_name, 'assay design', file_type)
    print('--------report chunk----------')
    print(report_chunk)
    instruction = assayability_biomarker_rating(gene_name, disease_name)
    print('--------instruction----------')
    print(instruction)
    scoring_result = scoring(llm, report_chunk, instruction)
    print('--------scoring result----------')
    print(scoring_result)
    return scoring_result

def unmet_need_scoring(llm, gene_name, disease_name, file_type = 'human'):
    if disease_name == 'atherosclerosis':
        market_info = '''
        The global atherosclerosis market has been experiencing steady growth, driven by the increasing prevalence of cardiovascular diseases and advancements in treatment options. In 2023, the market was valued at approximately USD 14.7 billion across seven major markets, including the United States, EU5 (Germany, Spain, Italy, France, and the United Kingdom), and Japan. Projections indicate that this value will reach USD 18.6 billion by 2034, reflecting a compound annual growth rate (CAGR) of 2.15% during the forecast period. 

        Focusing specifically on atherosclerosis drugs, the global market was valued at USD 20.6 billion in 2022. It is expected to grow to USD 27.7 billion by 2032, with a CAGR of 3.0% from 2023 to 2032. 

        These figures underscore the significant and growing demand for effective treatments and interventions for atherosclerosis, highlighting the importance of continued research and development in this field. 
        '''
    report_chunk = return_chunk(gene_name, disease_name, 'competitive edge', file_type)
    print('--------report chunk----------')
    print(report_chunk)
    instruction = unmet_need_rating(gene_name, disease_name)
    print('--------instruction----------')
    print(instruction)
    scoring_result = scoring(llm, report_chunk, instruction)
    print('--------scoring result----------')
    print(scoring_result)
    return scoring_result