import sys

# Add the parent directory to the sys.path
sys.path.append('../')


from Report_Generation_AgentAnalyst.agent_instructions import prompt_conclusion


def get_format(section_name):

    formats_dict = {
'loss_of_function': '''
| {{{{gene name}}}} | Genetic loci   | Amino acid change (e.g. "p.V143I", or "non coding") | Gene function (e.g. "Gain of function", "loss of function" or "unclear") | Traits associated with this variant (e.g. Low BMI, high cholesterol etc..) | reference |
|-------------|----------------|-----------------------------------------------------|-------------------------------------------------------------------------|---------------------------------------------------------------------------|-----------|
|             | rsXXXXX0       | p.XXXXX                                             |                                                                         |                                                                           |           |
|             | rsXXXXX        |                                                     |                                                                         |                                                                           |           |
|             | ...            |                                                     |                                                                         |                                                                           |           |
''',

'gain_of_function': '''
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

    return formats_dict[section_name]





def get_format_old(section_name):

    formats_dict = {
    "genetic_evidence": '''
    | {{{{gene name}}}} | Genetic loci   | Amino acid change (e.g. "p.V143I", or "non coding") | Gene function (e.g. "Gain of function", "loss of function" or "unclear") | Traits associated with this variant (e.g. Low BMI, high cholesterol etc..) | reference |
    |-------------|----------------|-----------------------------------------------------|-------------------------------------------------------------------------|---------------------------------------------------------------------------|-----------|
    | {{{{gene name}}}} | rsXXXXX       | p.XXXXX                                             |                                                                         |                                                                           |           |
    | {{{{gene name}}}} | rsXXXXX       |                                                     |                                                                         |                                                                           |           |
    |             | ...            |       
    ''',
    
    "safety": '''
    {{{{gene name}}}} | Safety issues have been reported in clinic | Human disease or traits linked to target gene mutation | Phenotype of target gene knockout mice | Is this an essential gene identified in human physiology or development |
    |-----------|-------------------------------------------|-------------------------------------------------------|---------------------------------------|---------------------------------------------------------------------|
    |{{{{gene name}}}} | 1.                                         |                                                       |                                       |                                                                     |
    |{{{{gene name}}}} | 2.                                         |                                                       |                                       |                                                                     |
    |{{{{gene name}}}} | ...                                       | ...                                                   | ...                                   | ...                                                                 |
    ''',
    
    "mechanism_of_action": '''
    | Gene name | Molecular function in human physiology | Gene category (e.g., Kinase, transcription factor, receptor etc) | Cell and tissue distribution | How is this relevant to disease of interest? | Reference |
    |-----------|----------------------------------------|----------------------------------------------------------|-----------------------------|--------------------------------------------|-----------|
    || Function 1... | |Tissue 1, cell type 1 | e.g. {{{{gene_name}}}} inhibition increases insulin sensitivity in muscle tissue |  |
    || Function 2... | |... | e.g. {{{{gene_name}}}} inhibition decreases food intake |  |
    || .... | ... | ... | ... |
    ''',
    
    "assays": '''
    | Gene name | Experimental evidence | Cell or animal model used | Key results | Reference |
    |-----------|-----------------------|---------------------------|-------------|-----------|
    || Study 1... | e.g. Human primary hepatocytes | e.g. siRNA knockdown of {{{{gene_name}}}} in hepatocytes decreases lipid droplet formation | |
    || Study 2... | e.g. Western Diet induced fatty liver mice model | e.g. {{{{gene_name}}}} knockout decreases food intake | |
    || ...       | ...                   | ...                       | ...         | ...       |
    ''',
    
    "in_vitro_or_vivo_data": '''
    | Gene name | Experimental assay | Cell or animal model can be used | Tool compound | Disease relevant readout | Reference |
    |-----------|--------------------|----------------------------------|---------------|--------------------------|-----------|
    || Study 1   | e.g. Human primary hepatocytes | e.g. siRNA | e.g. hepatocytes lipid droplet accumulation | |
    || Study 2   | e.g. GAN Diet induced fatty liver mice model | e.g. antibody | e.g. body weight change, HbA1C, Liver Histology.. | |
    || ....      |                    |                                  |               |                          |           |
    ''',
    
    "druggability": '''
    | Gene name | Subcellular distribution | Tissue specific expression | Protein structure available? | Membrane protein | Ligand binder | Small molecule binder | Pocket | Chemical probes | Reference |
    |-----------|--------------------------|----------------------------|------------------------------|------------------|---------------|-----------------------|--------|----------------|-----------|
    |           | e.g., cell surface receptor, secreted protein or intracellular protein | e.g. Highly expressed in hepatocytes, or ubiquitously expressed |                              | Check if Protein target is located (at least) in the cell or plasma membrane. | Is the target binds at least one high quality ligand? | Is the target has been co-crystallised with a small molecule in PDB? | Is the target contains a high-quality predicted pocket? | Does the target have high-quality chemical probes? |           |
    ''',
    
    "competitive_edge": '''
    | Gene name | Pipeline/Program | Testing drug molecule | Current status | Inclusion/Exclusion criteria | Endpoint | Trial results | Reference |
    |-----------|------------------|-----------------------|----------------|------------------------------|----------|---------------|-----------|
    |  | trial 1 xxxx |  | e.g. Phase 1 | | e.g. NAS/fibrosis score|  |
    | | program 1 xxx | | | | | |  |
    |  |.... | | | | | | |
    '''
    }
    return formats_dict[section_name]



def genetic_evidence():
    genetic_evidence = '''
    | {{{{gene name}}}} | Genetic loci   | Amino acid change (e.g. "p.V143I", or "non coding") | Gene function (e.g. "Gain of function", "loss of function" or "unclear") | Traits associated with this variant (e.g. Low BMI, high cholesterol etc..) | reference |
    |-------------|----------------|-----------------------------------------------------|-------------------------------------------------------------------------|---------------------------------------------------------------------------|-----------|
    | {{{{gene name}}}} | rsXXXXX       | p.XXXXX                                             |                                                                         |                                                                           |           |
    | {{{{gene name}}}} | rsXXXXX       |                                                     |                                                                         |                                                                           |           |
    |             | ...            |       
    '''
    return genetic_evidence


def safety_format():
    safety_format = '''
 {{{{gene name}}}} | Safety issues have been reported in clinic | Human disease or traits linked to target gene mutation | Phenotype of target gene knockout mice | Is this an essential gene identified in human physiology or development |
|-----------|-------------------------------------------|-------------------------------------------------------|---------------------------------------|---------------------------------------------------------------------|
|{{{{gene name}}}} | 1.                                         |                                                       |                                       |                                                                     |
|{{{{gene name}}}} | 2.                                         |                                                       |                                       |                                                                     |
|{{{{gene name}}}} | ...                                       | ...                                                   | ...                                   | ...                                                                 |
'''
    return safety_format


def mechanism_of_action():
    output_format = '''
| Gene name | Molecular function in human physiology | Gene category (e.g., Kinase, transcription factor, receptor etc) | Cell and tissue distribution | How is this relevant to disease of interest? | Reference |
|-----------|----------------------------------------|----------------------------------------------------------|-----------------------------|--------------------------------------------|-----------|
|| Function 1... | |Tissue 1, cell type 1 | e.g. {{{{gene_name}}}} inhibition increases insulin sensitivity in muscle tissue |  |
|| Function 2... | |... | e.g. {{{{gene_name}}}} inhibition decreases food intake |  |
|| .... | ... | ... | ... |
    '''

    return output_format

def experiment_data_finder_profile():
    output_format = '''
| Gene name | Experimental evidence | Cell or animal model used | Key results | Reference |
|-----------|-----------------------|---------------------------|-------------|-----------|
|| Study 1... | e.g. Human primary hepatocytes | e.g. siRNA knockdown of {{{{gene_name}}}} in hepatocytes decreases lipid droplet formation | |
|| Study 2... | e.g. Western Diet induced fatty liver mice model | e.g. {{{{gene_name}}}} knockout decreases food intake | |
|| ...       | ...                   | ...                       | ...         | ...       |
    '''
    return output_format

def invitro_invivo_experiment_designer_profile():
    output_format = '''
| Gene name | Experimental assay | Cell or animal model can be used | Tool compound | Disease relevant readout | Reference |
|-----------|--------------------|----------------------------------|---------------|--------------------------|-----------|
|| Study 1   | e.g. Human primary hepatocytes | e.g. siRNA | e.g. hepatocytes lipid droplet accumulation | |
|| Study 2   | e.g. GAN Diet induced fatty liver mice model | e.g. antibody | e.g. body weight change, HbA1C, Liver Histology.. | |
|| ....      |                    |                                  |               |                          |           |
    '''
    return output_format

def druggability_evaluation_expert_profile():
    output_format = '''
| Gene name | Subcellular distribution | Tissue specific expression | Protein structure available? | Membrane protein | Ligand binder | Small molecule binder | Pocket | Chemical probes | Reference |
|-----------|--------------------------|----------------------------|------------------------------|------------------|---------------|-----------------------|--------|----------------|-----------|
|           | e.g., cell surface receptor, secreted protein or intracellular protein | e.g. Highly expressed in hepatocytes, or ubiquitously expressed |                              | Check if Protein target is located (at least) in the cell or plasma membrane. | Is the target binds at least one high quality ligand? | Is the target has been co-crystallised with a small molecule in PDB? | Is the target contains a high-quality predicted pocket? | Does the target have high-quality chemical probes? |           |
    '''
    return output_format

def competitive_edge_expert_profile():
    output_format = '''
    | Gene name | Pipeline/Program | Testing drug molecule | Current status | Inclusion/Exclusion criteria | Endpoint | Trial results | Reference |
|-----------|------------------|-----------------------|----------------|------------------------------|----------|---------------|-----------|
|  | trial 1 xxxx |  | e.g. Phase 1 | | e.g. NAS/fibrosis score|  |
| | program 1 xxx | | | | | |  |
|  |.... | | | | | | |
    '''
    return output_format