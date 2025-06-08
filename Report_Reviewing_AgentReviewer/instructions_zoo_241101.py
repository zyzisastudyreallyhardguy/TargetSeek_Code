
import os
import sys

# Add the parent directory to the sys.path
sys.path.append('/GeneSeek/')


from tern_deployment.agent_instructions_1_1 import prompt_conclusion

output_format_zoo = {
'lof': '''
| {{{{gene name}}}} | Genetic loci   | Amino acid change (e.g. "p.V143I", or "non coding") | Gene function (e.g. "Gain of function", "loss of function" or "unclear") | Traits associated with this variant (e.g. Low BMI, high cholesterol etc..) | reference |
|-------------|----------------|-----------------------------------------------------|-------------------------------------------------------------------------|---------------------------------------------------------------------------|-----------|
|             | rsXXXXX0       | p.XXXXX                                             |                                                                         |                                                                           |           |
|             | rsXXXXX        |                                                     |                                                                         |                                                                           |           |
|             | ...            |                                                     |                                                                         |                                                                           |           |
    ''',

'gof': '''
| {{{{gene name}}}} | Genetic loci   | Amino acid change (e.g. "p.V143I", or "non coding") | Gene function (e.g. "Gain of function", "loss of function" or "unclear") | Traits associated with this variant (e.g. Low BMI, high cholesterol etc..) | reference |
|-------------|----------------|-----------------------------------------------------|-------------------------------------------------------------------------|---------------------------------------------------------------------------|-----------|
|             | rsXXXXX0       | p.XXXXX                                             |                                                                         |                                                                           |           |
|             | rsXXXXX        |                                                     |                                                                         |                                                                           |           |
|             | ...            |                                                     |                                                                         |                                                                           |           |
    ''',

'assays': '''
    ------------Invitro and Invivo Experimental Assay Design---------
| Gene name | Experimental assay | Cell or animal model can be used | Tool compound | Disease relevant readout | Reference |
|-----------|--------------------|----------------------------------|---------------|--------------------------|-----------|
|| Study 1   | e.g. Human primary hepatocytes | e.g. siRNA | e.g. hepatocytes lipid droplet accumulation | |
|| Study 2   | e.g. GAN Diet induced fatty liver mice model | e.g. antibody | e.g. body weight change, HbA1C, Liver Histology.. | |
|| ....      |                    |                                  |               |                          |           |

    ------------Target Engagement Analysis---------
| Gene Name | Measurement Method | Target Engagement | Accessibility of Samples | Reference |
|------------|----------------------------------------------------------------|------------------------------------------|------------------------------------------|----------------------------|-----------|
| {{{{target_gene_name}}}} | describe how the level of  {{{{target_gene_name}}}} can be directly measured. (Indirect measurement to infer the target engagement level shouldn't be considered!) | e.g., {{{{target_gene_name}}}} can only be measured in liver tissue | e.g.,Blood samples (easily accessible) |  |

   ------------Disease Biomarker Analysis---------
| Disease Name | Measurement | Measurement Method Reference |
|--------------|-------------|-----------|
| {{{{disease_name}}}} | Describe how to detect disease progression | e.g., biopsy | |
    ''' + prompt_conclusion(),

'competitive_edge': '''
--------Small molecule--------

| Small molecule Pipeline/Program | Testing drug molecule | Current Pipeline/Program status | Inclusion/Exclusion criteria | Endpoint | Trial results | Reference | Targeted protein | Aligned |
|---------------------------------|-----------------------|-----------------|----------------|------------------------------|----------|---------------|-----------|----------------|-----------|
| trial 1 xxxx | e.g.,the drug name and modality: Ibuprofen (Small Molecule)/trastuzumab (Antibody) | e.g. Phase 1 | | e.g. NAS/fibrosis score|  | What is the targeted protein of the pipeline? Be specific. Search and validate before filling this. | Check if the targeted protein aligned with the target gene provided by the user|
| program 1 xxx | |  | | | |  |  |
| .... | |  | | | |  |  |

--------Antibody--------

| Antibody Pipeline/Program | Testing drug molecule | Current Pipeline/Program  status | Inclusion/Exclusion criteria | Endpoint | Trial results | Reference | Targeted protein | Aligned |
|---------------------------|-----------------------|-----------------|----------------|------------------------------|----------|---------------|-----------|----------------|-----------|
| trial 1 xxxx | e.g.,the drug name and modality: Ibuprofen (Small Molecule)/trastuzumab (Antibody) | e.g. Phase 1 | | e.g. NAS/fibrosis score|  | What is the targeted protein of the pipeline? Be specific. Search and validate before filling this.| Check if the targeted protein aligned with the target gene provided by the user|
| program 1 xxx | |  | | | |  |  |
| .... | |  | | | |  |  |

--------Sirna--------

| Sirna Pipeline/Program | Testing drug molecule | Current Pipeline/Program  status | Inclusion/Exclusion criteria | Endpoint | Trial results | Reference | Targeted protein | Aligned |
|------------------------|-----------------------|-----------------|----------------|------------------------------|----------|---------------|-----------|----------------|-----------|
| trial 1 xxxx | e.g.,the drug name and modality: Ibuprofen (Small Molecule)/trastuzumab (Antibody) | e.g. Phase 1 | | e.g. NAS/fibrosis score|  | What is the targeted protein of the pipeline? Be specific. Search and validate before filling this.| Check if the targeted protein aligned with the target gene provided by the user|
| program 1 xxx | |  | | | |  |  |
| .... | |  | | | |  |  |
    ''' + prompt_conclusion('''

    ---------------------------
    - Describe the highest phase reached in trials for each drug type: **small molecule**, **antibody**, and **siRNA**.
    '''
                            ),

'druggability': '''
| Gene name | Subcellular distribution | Tissue specific expression | Protein structure available? | Membrane protein | Ligand binder | Small molecule binder | Pocket | Small Molecule Tool Compound | Reference |
|-----------|--------------------------|----------------------------|------------------------------|------------------|---------------|-----------------------|--------|----------------|-----------|
|           | e.g., cell surface receptor, secreted protein or intracellular protein | e.g. Highly expressed in hepatocytes, or ubiquitously expressed |                              | Check if Protein target is located (at least) in the cell or plasma membrane. | Is the target binds at least one high quality ligand? | Is the target has been co-crystallised with a small molecule in PDB? | Is the target contains a high-quality predicted pocket? | Does the target have high-quality small molecule tool compounds? List the name of these compounds |           |
    ''' + prompt_conclusion(),

'in_vitro_or_vivo_data': '''
| Gene name | Experimental evidence | Clinical Trial/Cell/Animal Model Used | Key Results | Reference |
|-----------|-----------------------|---------------------------------------|-------------|-----------|
|           | Study 1...             | e.g. Human primary hepatocytes        | e.g. siRNA knockdown of {{{{gene_name}}}} in hepatocytes decreases lipid droplet formation |           |
|           | Study 2...             | e.g. Western Diet induced fatty liver mice model | e.g. {{{{gene_name}}}} knockout decreases food intake |           |
|           | Study 3...             | e.g. Clinical trials have been conducted with antibodies | e.g., anti-{{{{gene_name}}}} antibody leads to decreased inflammation |           |
    ''' + prompt_conclusion(),

'mechanism_of_action': '''
| Gene name | Molecular function in human physiology | Gene category (e.g., Kinase, transcription factor, receptor etc) | Cell and tissue distribution | How is this relevant to disease of interest? | Reference |
|-----------|----------------------------------------|----------------------------------------------------------|-----------------------------|--------------------------------------------|-----------|
|| Function 1... | |Tissue 1, cell type 1 | e.g. {{{{gene_name}}}} inhibition increases insulin sensitivity in muscle tissue |  |
|| Function 2... | |... | e.g. {{{{gene_name}}}} inhibition decreases food intake |  |
|| .... | ... | ... | ... |
    ''' + prompt_conclusion(),

'safety':'''
| Gene name | Safety issues have been reported in clinic | Human disease or traits linked to target gene mutation | Phenotype of target gene knockout mice | Is this an essential gene identified in human physiology or development |
|-----------|-------------------------------------------|-------------------------------------------------------|---------------------------------------|---------------------------------------------------------------------|
|           | 1.                                         |                                                       |                                       |                                                                     |
|           | 2.                                         |                                                       |                                       |                                                                     |
|       | ...                                       | ...                                                   | ...                                   | ...                                                                 |
    ''' + prompt_conclusion(),
}


def get_output_format_of_section(section_name):
    return output_format_zoo[section_name]