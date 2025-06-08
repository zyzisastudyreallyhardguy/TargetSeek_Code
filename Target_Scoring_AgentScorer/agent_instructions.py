from Target_Scoring_AgentScorer.instructions import *
from Target_Scoring_AgentScorer.scoring_criteria import *
from Target_Scoring_AgentScorer.output_formats import *

def instruction_initialization(output_format, criteria, instruction, gene_name, disease_name):
    output_format = output_format
    table = criteria
    instruction = instruction
    return instruction.format(table=table, gene_name=gene_name, disease_name=disease_name, output_format=output_format)

def genetic_association_rating(gene_name, disease_name):
    return instruction_initialization(genetic_association_output_format, genetic_association_criteria, genetic_association_instruction, gene_name, disease_name)

def differential_expression_rating(gene_name, disease_name):
    return instruction_initialization(differential_expression_output_format, differential_expression_criteria, differential_expression_instruction, gene_name, disease_name)

def moa_rating(gene_name, disease_name):
    return instruction_initialization(moa_output_format, moa_criteria, moa_instruction, gene_name, disease_name)

def in_vitro_vivo_rating(gene_name, disease_name):
    return instruction_initialization(in_vitro_vivo_output_format, in_vitro_vivo_criteria, in_vitro_vivo_instruction, gene_name, disease_name)

def small_molecule_rating(gene_name, disease_name, no_drug_pipeline_info=True):
    return instruction_initialization(small_molecule_output_format, small_molecule_no_leakage_criteria, small_molecule_instruction, gene_name, disease_name) if no_drug_pipeline_info else instruction_initialization(small_molecule_output_format, small_molecule_criteria, small_molecule_instruction, gene_name, disease_name)

def antibody_rating(gene_name, disease_name, no_drug_pipeline_info=True):
    return instruction_initialization(antibody_output_format, antibody_no_leakage_criteria, antibody_instruction, gene_name, disease_name) if no_drug_pipeline_info else instruction_initialization(antibody_output_format, antibody_criteria, antibody_instruction, gene_name, disease_name)

def sirna_rating(gene_name, disease_name):
    return instruction_initialization(sirna_output_format, sirna_no_leakage_criteria, sirna_instruction, gene_name, disease_name)

def competitiveness_rating(gene_name, disease_name):
    return instruction_initialization(competitiveness_output_format, competitiveness_criteria, competitiveness_instruction, gene_name, disease_name)

def competitiveness_small_molecule_rating(gene_name, disease_name):
    return instruction_initialization(competitiveness_small_molecule_output_format, competitiveness_small_molecules_criteria, competitiveness_small_molecule_instruction, gene_name, disease_name)

def competitiveness_antibody_or_sirna_rating(gene_name, disease_name):
    return instruction_initialization(competitiveness_sirna_or_antibody_output_format, competitiveness_antibody_or_sirna_criteria, competitiveness_antibody_or_sirna_instruction, gene_name, disease_name)

def assayability_rating(gene_name, disease_name):
    return instruction_initialization(assayability_output_format, assayability_criteria, assayability_instruction, gene_name, disease_name)

def target_safety_rating(gene_name, disease_name):
    return instruction_initialization(target_safety_output_format, target_safety_criteria, target_safety_instruction, gene_name, disease_name)

def moa_match_rating(gene_name, disease_name, user_preference):
    return instruction_initialization(moa_match_output_format, moa_match_criteria, moa_match_instruction(moa_criteria, user_preference, moa_match_output_format), gene_name, disease_name)

def target_in_clinic_rating(gene_name, disease_name):
    return instruction_initialization(opentarget_output_format, target_in_clinic_criteria, target_in_clinic_instruction, gene_name, disease_name)

def membrane_protein_rating(gene_name, disease_name):
    return instruction_initialization(opentarget_output_format, membrane_protein_criteria, membrane_protein_instruction, gene_name, disease_name)

def secreted_protein_rating(gene_name, disease_name):
    return instruction_initialization(opentarget_output_format, secreted_protein_criteria, secreted_protein_instruction, gene_name, disease_name)

def tissue_specificity_rating(gene_name, disease_name):
    return instruction_initialization(opentarget_output_format, tissue_specificity_criteria, tissue_specificity_instruction, gene_name, disease_name)

def tissue_distribution_rating(gene_name, disease_name):
    return instruction_initialization(opentarget_output_format, tissue_distribution_criteria, tissue_distribution_instruction, gene_name, disease_name)

def ligand_binder_rating(gene_name, disease_name):
    return instruction_initialization(opentarget_output_format, ligand_binder_criteria, ligand_binder_instruction, gene_name, disease_name)

def small_molecule_binder_rating(gene_name, disease_name):
    return instruction_initialization(opentarget_output_format, small_molecule_binder_criteria, small_molecule_binder_instruction, gene_name, disease_name)

def chemical_probes_rating(gene_name, disease_name):
    return instruction_initialization(opentarget_output_format, chemical_probes_criteria, chemical_probes_instruction, gene_name, disease_name)

def predicted_pocket_rating(gene_name, disease_name):
    return instruction_initialization(opentarget_output_format, predicted_pocket_criteria, predicted_pocket_instruction, gene_name, disease_name)

def assayability_biomarker_rating(gene_name, disease_name):
    return instruction_initialization(assayability_biomarker_output_format, assayability_biomarker_criteria, assayability_biomarker_instruction, gene_name, disease_name)

def unmet_need_rating(gene_name, disease_name):
    return instruction_initialization(unmet_need_output_format, unmet_need_criteria, unmet_need_instruction, gene_name, disease_name)