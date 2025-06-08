from Target_Scoring_AgentScorer.scoring_criteria import *
from Target_Scoring_AgentScorer.output_formats import *

def instructions_set_up(table, task_descirption, task_name, output_format, task_specific_instruction = ''):
    instruction = '''
{table}
    **************************
You are a genetic researcher tasked with evaluating **{task_descirption}**.

Please use the table above to **rate the level of {task_name} based on a report user provided.** Each column represents a different level of {task_name}, from strong positive to strong negative. Carefully consider the evidence and select the most appropriate rating based on the descriptions provided in the table.

{task_specific_instruction}

Output Format:
{output_format}

Please organize your output according to the Output Format. Fill in each cell based on descriptions in each cell. If the Output Format is empty, you can ignore it.
    '''.format(task_descirption=task_descirption, task_name=task_name, table=table, output_format = output_format, task_specific_instruction = task_specific_instruction)
    return instruction

def moa_match_instruction(moa_match_criteria, user_preference, moa_match_output_format):
    moa_match_instruction = instructions_set_up(moa_match_criteria, 'mechanism of action of the {gene_name} for {disease_name} match the user preferred MOA:' + user_preference, 'matching', moa_match_output_format)
    return moa_match_instruction

def open_target_instructions_set_up(criteria, task_descirption, output_format, task_specific_instruction = ''):
    instruction = '''
    {criteria}
    **************************
You are a genetic researcher tasked with evaluating **{task_descirption}**.

Please use the criteria above to give a score based on a report user provided. Carefully consider the evidence and select the most appropriate rating based on the descriptions provided in the criteria.

{task_specific_instruction}

Output Format:
{output_format}

Please organize your output according to the Output Format. Give the score in int format and provide a rationale for the score.
    '''.format(task_descirption=task_descirption, criteria=criteria, output_format = output_format, task_specific_instruction = task_specific_instruction)
    return instruction


genetic_association_instruction = instructions_set_up(genetic_association_criteria, 'genetic association of the {gene_name} with a specific disease {disease_name}', 'genetic association', genetic_association_output_format)

## differential_expression
differential_expression_specific_instruction = '''
- **If the target gene is differentially expressed during disease progression, it is a strong positive sign.**. IGNORE all other factors in this case.
- If the gene is **predominantly expressed** in the tissue associated with the disease (or significantly higher in relevant tissues, even if moderately expressed in others), it is a **weak positive indicator**.
- If the gene is **ubiquitously expressed**, it is a **weak negative indicator**.
'''
differential_expression_instruction = instructions_set_up(differential_expression_criteria, 'differential expression of {gene_name}', 'differential expression', differential_expression_output_format, differential_expression_specific_instruction)

moa_instruction = instructions_set_up(moa_criteria, 'mechanism of action of the {gene_name} with a specific disease {disease_name}', 'mechanism of action', moa_output_format)

## in_vitro_vivo
in_vitro_vivo_specific_instruction = '''
- Read competitive edge reports to identify if there is clinical trials evidence supporting the gene's role in the disease.
- If there is clinical trial (i.e., in human perturbation) evidence directly supporting the gene's role in the disease, then it is a **strong positive (+1)**.
'''
in_vitro_vivo_instruction = instructions_set_up(in_vitro_vivo_criteria, 'strength of target {gene_name} and {disease_name} disease progression evidence based on found in vitro/vivo experiments', 'evidence supporting {gene_name} role in {disease_name} disease progression', in_vitro_vivo_output_format, in_vitro_vivo_specific_instruction)

small_molecule_specific_instruction = '''
- If there are small molecule drugs in clinical trial or being approved for {gene_name},, it **means the target is strong positive (+1)**.
- If **crystal structures and tool compounds** (have to have both) for {gene_name} are available, it **means the target is weak positive (+0.5)**.
- If only crystal structures are available for {gene_name},, it **means the target is neutral (0)**.
- If only obvious pocket site is available for {gene_name}, it **means the target is weak negative (-0.5)**.
- If none of the structure and tool compounds are available for {gene_name}, it **means the target is strong negative (-1)**.
'''
small_molecule_instruction = instructions_set_up(small_molecule_criteria, 'suitability of small molecules targeting the {gene_name}', 'suitability of small molecule for {gene_name}', small_molecule_output_format, small_molecule_specific_instruction)

antibody_specific_instruction = '''
- If there are antibody drugs in clinical trial or being approved , it **means the target is strong positive (+1)**. NOTE: The drug has to **directly target** the target gene.
'''
antibody_instruction = instructions_set_up(antibody_criteria, 'suitability of antibodies targeting the {gene_name}', 'suitability of antibodies for {gene_name}', antibody_output_format, antibody_specific_instruction)

sirna_specific_instruction = '''
- IMPORTANT: Don't only check where the gene is expressed, but also check where the gene functions.
- Only assign negative ratings if target gene exon skipping or target activation are needed for siRNA to work for the intended disease.
- It is essential to consider which organs express the target gene and whether these organs are accessible and amenable to siRNA targeting strategies. Think about if there are clear strategies to use siRNA for targeting the gene when considering the organ.
'''
sirna_instruction = instructions_set_up(sirna_criteria, 'suitability of siRNA targeting the {gene_name}', 'suitability of siRNA for {gene_name}', sirna_output_format)

# competitiveness
competitiveness_instruction = instructions_set_up(competitiveness_criteria, 'competitiveness of the {gene_name} in the market', 'competitiveness of {gene_name}', competitiveness_output_format)


competitiveness_small_molecule_specific_instruction = '''
- NOTE: CHECK the "targeted protein" columns in competitive edge report tables to check if the pipelines is for {gene_name}. If not, you need to IGNORE the pipeline.
- Think about the clinical phases of the existing small molecule drugs **directly** targeting the {gene_name} in **{disease_name}**. If it is not directly targeted, then it is not considered. 
- Phase 1 and 2 leads to **Netural (0)** rating.
- Phase 3 leads to **Weak negative (+0.5)** rating.
- Approved leads to **Strong negative (-1)** rating.
- If there are only preclinical development activties, it leads to **Weak positive (+0.5)** rating.
'''
competitiveness_small_molecule_instruction = instructions_set_up(competitiveness_small_molecules_criteria, 'competitiveness of the {gene_name} in the small molecules drug market', 'competitiveness of {gene_name}', competitiveness_output_format, competitiveness_small_molecule_specific_instruction)

competitiveness_antibody_or_sirna_instruction = instructions_set_up(
competitiveness_antibody_or_sirna_criteria, 'competitiveness of the {gene_name} in the antibody or sirna drug market', 'competitiveness of {gene_name}', competitiveness_output_format)

assayability_instruction = instructions_set_up(assayability_criteria, 'assayability of the {gene_name}', 'assayability of {gene_name}', assayability_output_format)

target_safety_specific_instruction = '''
- Think about the desired therapeutic effect of {gene_name} in {disease_name} first.
- Please note that side effect means adversary phenotype **in addition to desired therapeutic effects**.
- If the knockout mice of {gene_name} shows desired therapeutic effects, it is not an adverse phenotype.
'''
target_safety_instruction = instructions_set_up(target_safety_criteria, 'safety of targeting {gene_name} for {disease_name}', 'safety of {gene_name} for {disease_name}', target_safety_output_format)

target_in_clinic_instruction = open_target_instructions_set_up(target_in_clinic_criteria, 'clinical trial status of the {gene_name}', opentarget_output_format)

membrane_protein_instruction = open_target_instructions_set_up(membrane_protein_criteria, 'if the target {gene_name} locates in the cell membrane', opentarget_output_format)

secreted_protein_instruction = open_target_instructions_set_up(secreted_protein_criteria, 'if the target {gene_name} is secreted', opentarget_output_format)

tissue_specificity_instruction = open_target_instructions_set_up(tissue_specificity_criteria, 'tissue specificity of the {gene_name}', opentarget_output_format)

tissue_distribution_instruction = open_target_instructions_set_up(tissue_distribution_criteria, 'tissue distribution of the {gene_name}', opentarget_output_format)

ligand_binder_instruction = open_target_instructions_set_up(ligand_binder_criteria, 'if the target {gene_name} binds to a ligand. If there are small molecule', opentarget_output_format)

small_molecule_binder_instruction = open_target_instructions_set_up(small_molecule_binder_criteria, 'if the target {gene_name} binds to a small molecule. Considers any high-quality ligand, which could be a peptide, nucleotide, ion, or small molecule.', opentarget_output_format)

chemical_probes_instruction = open_target_instructions_set_up(chemical_probes_criteria, 'if the target {gene_name} has chemical probes', opentarget_output_format)

predicted_pocket_instruction = open_target_instructions_set_up(predicted_pocket_criteria, 'if the target {gene_name} has a pocket', opentarget_output_format)

unmet_need_specific_instruction = '''
Think about following questions before doing rating.
- Is there a large patient population or estimated drug market >1 billion for {disease_name}? 
- Is there no drug available for {gene_name}? 
- Are there approved drugs for {gene_name}? 
- Do patients prefer less frequent dosing drugs for {gene_name}? If yes, there is unmet need.
- Do patients prefer oral format drugs for {gene_name}? If yes, there is unmet need.
- Do patients prefer reduced side effect drugs for {gene_name}? If yes, there is unmet need.
'''
unmet_need_instruction = instructions_set_up(unmet_need_criteria, 'unmet need of the {gene_name}', unmet_need_output_format, unmet_need_specific_instruction)

# assayability_biomarker_instruction = open_target_instructions_set_up(assayability_biomarker_criteria, 'assayability of the {gene_name} as a biomarker', assayability_biomarker_output_format)

assayability_biomarker_specific_instruction = '''
- Think about how the target engagement measurement can be done? (in plasma/non-invasively way or tissue)
- Think about how the biomarker measurement can be done? (in plasma/non-invasively way or tissue)
- NOTE: cannot be done in plasma/non-invasively way doesn't mean the target should be rated as negative scores.
- Please be aware that the target engagement measurement has to **directly** measure the target gene. If it is not directly targeted, then it is not considered.

- Criteria Guidance-
- Strong positive (+1) is assigned if both the target engagement and biomarker measurement can be done in plasma/non-invasively way.
- Weak positive (+0.5) is assigned if either target engagement or biomarker measurement can be done in plasma/non-invasively way.
- Neutral (0) is assigned if both the target engagement and biomarker measurement can be done in tissue but cannot be done non-invasively.
- Weak negative (-0.5) is assigned if either target engagement or biomarker measurement cannot be done easier than tissue inspection, e.g., biopsy. 
- Strong negative (-1) is assigned if both the target engagement and biomarker measurement  cannot be done easier than tissue inspection, e.g., biopsy.
'''
assayability_biomarker_instruction = instructions_set_up(assayability_biomarker_criteria, 'assayability of {gene_name}', assayability_biomarker_output_format, assayability_biomarker_specific_instruction)

def generate_final_table_instruction(moa_match=False):


    generate_final_table_instruction = '''
    | Gene_name    | Category                                  | Rating | Rationale |
    |--------------|-------------------------------------------|--------|-----------|
    | **Causal inference** | Genetic Association              |        |           |
    |                | Differential expression                |        |           |
    |                | Mechanism of Action                    |        |           |
    |                | In vitro/in vivo experiment            |        |           |
    | **Tractability** | Small molecules                      |        |           |
    |                | Antibody                               |        |           |
    |                | siRNA                                  |        |           |
    | **Competition/novelty** | Competitiveness (Small Molecule)              |        |           |
    |                | Competitiveness (Antibody or siRNA)           |        |           |
    |               | Unmet needs                             |        |           |
    | **Doability** | assayability - experimental model availability |        |           |
    |               | assayability - biomarkers               |        |           |
    |                | Safety                                 |        |           |
    '''

    if moa_match:
        generate_final_table_instruction += '''
        | **MOA Match** | Match Level |        |           |
        '''
        

    generate_final_table_instruction += '''
    --------------------
    the user will give you a json like report, use the report to fill in the table.
    '''

    return generate_final_table_instruction


class scoringReviewerPrompts:
    def __init__(self) -> None:
        self.instructions_overall_reviewer = '''\
You are a reviewer for scoring. Based on the provided **Scoring Criteria**, **Materials for Scoring**, and **Agent's Score and Rationale**, you need to determine whether the given score aligns with the scoring criteria.
'''
        self.reviewer_instruction = """
Do you think the Rating score and conclusion is correct? 

Think about what is the criteria for the score first, and then check if the score is correct.

If it is incorrect, correct and update the the Agent's Score and Rational.
If it is correct, keep the original Agent's Score and Rational table.

Think and Then return the correct Agent's Score and Rational table in the same format of the original one
"""

        self.prompt_for_reviewer = """{instructions_overall_reviewer}
-------------Here is the Scoring Criteria------------
{criteria}
-------------Here is the Materials for scoring------------
{scoring_task_instr}
-------------Here is the Agent's Score and Rationale------------
{score_pre}
-----------------------------------------------------
{reviewer_instruction}
"""
        self.prompt_for_new_score = """
Extract the corrected Agent's Score and Rationale from the analysis below:
-------------Here is the analysis------------
{review_scores}

-------------Here is Output format------------
{output_format}

Please return your output according to the Output Format. If the Output Format is empty, you can ignore it.
"""
        self.section_names = [
                'genetic_evidence_scoring',
                'differential_expression_scoring',
                'moa_scoring',
                'in_vitro_vivo_scoring',
                'small_molecule_scoring',
                'antibody_scoring',
                'sirna_scoring',
                'competitiveness_scoring',
                'assayability_scoring',
                'target_safety_scoring',
                'unmet_need_scoring',
                'assayability_biomarker_scoring'
            ]

        self.section_criteria = {
                'genetic_evidence_scoring':genetic_association_criteria,
                'differential_expression_scoring':differential_expression_criteria,
                'moa_scoring':moa_criteria,
                'in_vitro_vivo_scoring':in_vitro_vivo_criteria,
                'small_molecule_scoring':small_molecule_criteria,
                'antibody_scoring':antibody_criteria,
                'sirna_scoring':sirna_criteria,
                'competitiveness_scoring':competitiveness_criteria,
                'assayability_scoring':assayability_criteria,
                'target_safety_scoring':target_safety_criteria,
                'unmet_need_scoring':unmet_need_criteria,
                'assayability_biomarker_scoring':assayability_biomarker_criteria,
            }
        self.section_required_reports = {
                'genetic_evidence_scoring':['genetic evidence'],
                'differential_expression_scoring':['druggability','tissue_distribution'],
                'moa_scoring':['genetic evidence','mechanism of action'],
                'in_vitro_vivo_scoring':['in vitro'],
                'small_molecule_scoring':['druggability'],
                'antibody_scoring':['druggability'],
                'sirna_scoring':['druggability','tissue_distribution'],
                'competitiveness_scoring':['competitive edge'],
                'assayability_scoring':['assay design'],
                'target_safety_scoring':['safety evaluation'],
                'unmet_need_scoring':['competitive edge'],
                'assayability_biomarker_scoring':['assay design'],
            }

        self.section_task_instructions = {
                'genetic_evidence_scoring':'genetic association of the {gene_name} with a specific disease {disease_name}',
                'differential_expression_scoring':'differential expression of {gene_name}',
                'moa_scoring':'mechanism of action of the {gene_name} with a specific disease {disease_name}',
                'in_vitro_vivo_scoring':'strength of target {gene_name} and {disease_name} disease progression evidence based on found in vitro/vivo experiments',
                'small_molecule_scoring':'suitability of small molecules targeting the {gene_name}',
                'antibody_scoring':'suitability of antibodies targeting the {gene_name}',
                'sirna_scoring':'suitability of siRNA targeting the {gene_name}',
                'competitiveness_scoring':'competitiveness of the {gene_name} in the market',
                'assayability_scoring':'assayability of the {gene_name}',
                'target_safety_scoring':'safety of the {gene_name}',
                'unmet_need_scoring':'unmet need of the {gene_name}',
                'assayability_biomarker_scoring':'assayability of the {gene_name} as a biomarker',
            }
        
        self.section_format_instructions = {
                'genetic_evidence_scoring':genetic_association_output_format,
                'differential_expression_scoring':differential_expression_output_format,
                'moa_scoring':moa_output_format,
                'in_vitro_vivo_scoring':in_vitro_vivo_output_format,
                'small_molecule_scoring':small_molecule_output_format,
                'antibody_scoring':antibody_output_format,
                'sirna_scoring':sirna_output_format,
                'competitiveness_scoring':competitiveness_output_format,
                'assayability_scoring':assayability_output_format,
                'target_safety_scoring':target_safety_output_format,
                'unmet_need_scoring':unmet_need_output_format,
                'assayability_biomarker_scoring':assayability_biomarker_output_format,
            }
