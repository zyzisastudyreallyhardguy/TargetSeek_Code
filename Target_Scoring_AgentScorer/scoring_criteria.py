genetic_association_criteria ='''
    |                 | Strong - positive (+1)                    | Weak - positive (+0.5)                          | Neutral (0)            | Weak negative (-0.5)                           | Strong negative (-1)                             |
    |-----------------|-------------------------------------------|------------------------------------------------|------------------------|-----------------------------------------------|-------------------------------------------------|
    | Genetic association | Human variants lead to disease phenotype | Human variants associated with disease phenotype | No report              | Human variants show conflict phenotypes       | Human variants of the target gene show clearly no effect on disease phenotype |
    '''

differential_expression_criteria ='''
|                         | strong - positive (+1)                             | Weak - positive (+0.5)                          | neutral (0)                        | Weak negative (-0.5)                      | Strong negative (-1)                                    |
|-------------------------|----------------------------------------------------|-------------------------------------------------|------------------------------------|--------------------------------------------|--------------------------------------------------------|
| Differential expression | Target gene differentially expressed during disease progression | Target gene specifically expressed in disease associated tissue and not expressed much in other tissues. If it is also expressed much in many other tissues, then it is not positive. | The expression pattern of the target gene is not clear | Target gene is ubiquitously expressed | Target gene not expressed in the intent to target tissue |
'''

moa_criteria ='''
| Causal inference | 3. Mechanism of action | strong-positive (+1) | Weak-positive (+0.5) | neutral (0) | Weak negative (-0.5) | Strong negative (-1) |
|------------------|------------------------|----------------------|----------------------|-------------|----------------------|----------------------|
|                  |                        | Molecular mechanism of the target drive disease traits | Molecular mechanism of the target related to disease traits | The molecular mechanism of the target is unknown | The molecular mechanism of the target is associated with a lot of different traits | Molecular mechanism of the target is clearly not relevant to disease traits |
'''

in_vitro_vivo_criteria ='''
|                           | Strong - positive (+1)                               | Weak - positive (+0.5)                                                   | Neutral (0)                                    | Weak negative (-0.5)                                                       | Strong negative (-1)                             |
|---------------------------|-----------------------------------------------------|--------------------------------------------------------------------------|------------------------------------------------|----------------------------------------------------------------------------|-------------------------------------------------|
|  | In human perturbation (i.e., clinical trials) of the target gene modulates disease progression | **Both Cell & In animal perturbation** of the target gene modulates disease progression | **Only Cell** perturbation of the target gene modulates disease progression | **Conflict results** upon target gene perturbation in disease associated experimental model | Clinical programme tested but failed due to lack of efficacy |
'''

small_molecule_criteria ='''
|     | strong - positive (+1)                           | Weak - positive (+0.5)                       | neutral (0)                         | Weak negative (-0.5)                     | Strong negative (-1)               |
|-----|--------------------------------------------------|---------------------------------------------|-------------------------------------|------------------------------------------|-------------------------------------|
|   | Small molecule drugs in clinical trials or on the market | **Both Target Crystal structure and Tool compound small molecule** available | Target Crystal structure available | No obvious binding pocket for the target | No structure, no tool compound     |
| Small molecules |
'''

# no leakage version
small_molecule_no_leakage_criteria ='''
|     | strong - positive (+1)                           | Weak - positive (+0.5)                       | neutral (0)                         | Weak negative (-0.5)                     | Strong negative (-1)               |
|-----|--------------------------------------------------|---------------------------------------------|-------------------------------------|------------------------------------------|-------------------------------------|
|   | **Both Target Crystal structure and Tool compound small molecule** available | Validated Small Molecule Tool Compounds Available  | Target Crystal structure available | No obvious binding pocket for the target | No structure, no tool compound     |
| Small molecules |
'''

antibody_criteria = '''
|     | strong - positive (+1)                                                                 | Weak - positive (+0.5)                                                              | neutral (0)                  | Weak negative (-0.5)                                             | Strong negative (-1)         |
|-----|----------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------|------------------------------|------------------------------------------------------------------|------------------------------|
| | There are antibody drugs in clinical trials or on the market                           | There are experimental antibodies that have been developed and shown to modulate target activity | Cell surface or secreted proteins | Cross blood brain barrier needed for modulating the target       | Intracellular protein        |
'''

# no leakage version
antibody_no_leakage_criteria = '''
|     | strong - positive (+1)                                                                 | Weak - positive (+0.5)                                                              | neutral (0)                  | Weak negative (-0.5)                                             | Strong negative (-1)         |
|-----|----------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------|------------------------------|------------------------------------------------------------------|------------------------------|
|  | Antibody-Mediated Modulation Demonstrated | There are experimental antibodies that have been developed and shown to modulate target activity | Cell surface or secreted proteins | Cross blood brain barrier needed for modulating the target       | Intracellular protein        |
| antibody |
'''

sirna_criteria ='''
|     |          | strong - positive (+1) | Weak - positive (+0.5) | neutral (0) | Weak negative (-0.5) | Strong negative (-1) |
|-----|----------|-------------------------|------------------------|-------------|----------------------|-----------------------|
|   | siRNA    | Target gene mainly expressed and function in hepatocytes. | The target gene is primarily expressed and functions in the CNS, muscle, adipose tissue, or blood cells. | No good sirna strategy so far and therapeutic direction is not clear. | Target exon skipping is needed as a therapeutics for the intended disease | Target activation needed as a therapeutics for the intended disease |
'''

# no leakage version
sirna_no_leakage_criteria ='''
|     |          | strong - positive (+1) | Weak - positive (+0.5) | neutral (0) | Weak negative (-0.5) | Strong negative (-1) |
|-----|----------|-------------------------|------------------------|-------------|----------------------|-----------------------|
|   | siRNA    | Target gene mainly expressed and function in hepatocytes. | The target gene is primarily expressed and functions in the CNS, muscle, adipose tissue, or blood cells. | No good sirna strategy so far and therapeutic direction is not clear. | Target exon skipping is needed as a therapeutics for the intended disease | Target activation needed as a therapeutics for the intended disease |
'''

competitiveness_criteria ='''
|                        | strong - positive (+1)               | Weak - positive (+0.5)          | neutral (0)                       | Weak negative (-0.5)                    | Strong negative (-1)                        |
|------------------------|--------------------------------------|---------------------------------|----------------------------------|------------------------------------------|---------------------------------------------|
|                        | No reported drug development activity | There are pre-clinical development activities | There are early clinical development activities (**phase 1, phase 2**) | There are pipelines in late stage clinical (**phase 3**) | **Approved drugs** for the same target for the same indication |
'''

competitiveness_small_molecules_criteria ='''
|                        | strong - positive (+1)               | Weak - positive (+0.5)          | neutral (0)                       | Weak negative (-0.5)                    | Strong negative (-1)                        |
|------------------------|--------------------------------------|---------------------------------|----------------------------------|------------------------------------------|---------------------------------------------|
|                        | No reported drug development activity for {gene_name} **small molecule** drugs in {disease_name}| There are pre-clinical development activities for {gene_name} **small molecules** drugs in {disease_name}| There are early clinical development activities (**phase 1, phase 2**) for {gene_name} **small molecule** drugs in {disease_name}| There are pipelines in late stage clinical (**phase 3**) for {gene_name} **small molecules** in {disease_name}| **There are approved {gene_name} small molecule drugs** in {disease_name}|
'''

competitiveness_antibody_or_sirna_criteria ='''
|                        | strong - positive (+1)               | Weak - positive (+0.5)          | neutral (0)                       | Weak negative (-0.5)                    | Strong negative (-1)                        |
|------------------------|--------------------------------------|---------------------------------|----------------------------------|------------------------------------------|---------------------------------------------|
|                        | No reported drug development activity for **antibodies or sirna**| There are pre-clinical development activities for **antibodies or sirna**| There are early clinical development activities (**phase 1, phase 2**) for **antibodies or sirna**| There are pipelines in late stage clinical (**phase 3**) for **antibodies or sirna**| **Approved for antibodies or sirna drugs** for the same target for the same indication|
'''

assayability_criteria ='''
|     |                | strong - positive (+1) | Weak - positive (+0.5) | neutral (0) | Weak negative (-0.5) | Strong negative (-1)            |
|-----|----------------|-------------------------|------------------------|-------------|----------------------|---------------------------------|
| 8.  | assayability   | There are animal and cellular models that have been tested with tool compounds for drug discovery | There are animal and cellular models that have been tested using genetic perturbations | Only cellular models have been reported | No animal model | No animal model and no cellular model |
'''

target_safety_criteria = '''
| Rating                   | Strong Positive (+1)                                                                  | Weak Positive (+0.5)                                                        | Neutral (0)                                                                  | Weak Negative (-0.5)                                                      | Strong Negative (-1)                             |
|--------------------------|-------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------|----------------------------------------------------------------------------------|--------------------------------------------------------------------------------|---------------------------------------------------------------------------------|
| Description              | -**Human** variants are healthy in clinical programme for {gene_name} in {disease_name}. OR - Have drugs approved and are generally considered safe, i.e., shows a favorable safety profile in humans and no severe side effects.            | No side effects or safety issue has been identified in **mice or other animal models**.    | There is no studies have been conducted, e.g., animal models or clinical trials.                                            | - **Severe side effect or safety issues** have been identified in **mice or other animal models.** | - Clinical programs tested but failed due to safety issues.  OR  - **Severe side effects** (side effects means adversary phenotype in addition to desired therapeutic effects) have been detected in humans|
'''

# '''
# # |     |                | strong - positive (+1) | Weak - positive (+0.5) | neutral (0) | Weak negative (-0.5) | Strong negative (-1)            |
# # |-----|----------------|-------------------------|------------------------|-------------|----------------------|---------------------------------|
# # |   | safety         | - Clinical programme tested and approved to be safe, e.g., approved drugs - Human variants are healthy  | No defect or safety issue has been identified in mice or other animal model | No safety studies have been conducted | Defects or safety issues have been identified in mice or other animal model | **Clinical programme tested but failed** due to safety issues |
# '''

moa_match_criteria = '''
| Match Level of Mechanism of Action (MOA) with User Preference | Positive (+1) | Neutral (0) | Negative (0.5)|
|--------------------------------------------------------------|----------|---------|----------|
|                                                              | The MOA of the gene clearly matches the user preference | It is hard to tell if the MOA of the gene matches user preference. | The MOA of the gene doesn't match the user preference |
'''

target_in_clinic_criteria = '''
Maximum clinical trial phase the target has been reported for, independently of the disease. Phases range from 0 to IV (corresponding to values of 0, 0.25, 0.5, 0.75 and 1).
0 = Phase 0
0.25 = Phase I
0.5 = Phase II
0.75 = Phase III
1 = Phase IV
'''

membrane_protein_criteria = '''
1 = Protein target is located (at least) in the cell or plasma membrane. 
0 = Protein target is not located in the cell membrane but some location information is accessible. 
NA = No location information available.
'''

secreted_protein_criteria = '''
1 = Protein target is (at least) secreted or predicted to be secreted. 
0 = Not secreted but with location information.
NA = No location information available.
'''

tissue_specificity_criteria = '''
| Tissue specificity HPA assessment                                          | Score |
|---------------------------------------------------------------------------|-------|
| Tissue enriched >=4 fold higher mRNA in a given tissue compared to any other | 1     |
| Group enriched >=4 fold higher average mRNA in 2-5 tissues compared to any other | 0.75  |
| Tissue enhanced >=4 fold higher mRNA level in a given tissue compared to average of all other tissues | 0.5   |
| Low tissue specificity                                                     | -1    |
| Not detected                                                               | NA    |
'''

tissue_distribution_criteria = '''
| Tissue distribution HPA assessment                                                                 | Score |
|----------------------------------------------------------------------------------------------------|-------|
| Detected in single: detected in a single tissue                                                     | 1     |
| Detected in some: detected in more than one but less than 1/3 of tissues                            | 0.5   |
| Detected in many: detected in at least 1/3 but not all tissues                                      | 0     |
| Detected in all                                                                                    | -1    |
| Not detected                                                                                       | NA    |
'''

# unmet_need_criteria = '''
# | Unmet Needs | Strong Positive (+1) | Weak Positive (+0.5) | Neutral (0) | Weak Negative (-0.5) | Strong Negative (-1) |
# | --- | --- | --- | --- | --- | --- |
# | Large patient population or estimated drug market >1 billion | No drug | Large market size - There are approved drugs but patients prefer less frequent dosing or oral format | Medium-sized market (<1 billion USD/year) and there is a need for better drug | There are many approved drugs | Small market size |
# '''

unmet_need_criteria = '''
| Unmet Needs | Strong Positive (+1) | Weak Positive (+0.5) | Neutral (0) | Weak Negative (-0.5) | Strong Negative (-1) |
| --- | --- | --- | --- | --- | --- |
|  | Large patient population or estimated drug market >1billion for the disease & No approved drugs for the target gene | Large Market for the disease & there are approved drugs but patients prefer less frequent dosing, oral format or reduced side effect (i.e., better drugs) for the target gene. | Medium Market Size (<1billion USD/year) for the disease & No approved drugs for the target gene.  | Medium Market Size for the disease and there are approved drugs but patients prefer less frequent dosing or oral format or reduced side effect (i.e., better drugs) for the target gene 2. Small market size for the disease & No approved Drugs for the target gene | Only need to meet one of the following requirements 1. Small market size for the disease 2. Patients are happy with current drugs for the target gene.|
'''

assayability_biomarker_criteria = '''
| Assayability - biomarkers & target engagement | Strong Positive (+1) | Weak Positive (+0.5) | Neutral (0) | Weak Negative (-0.5) | Strong Negative (-1) |
| --- | --- | --- | --- | --- | --- |
| --- | Treatment Efficacy and target engagement can be measured in plasma/non invasively | Either treatment efficacy or target engagement can be measured non-invasively. The other one needs to be measured in tissue. | Treatment Efficacy and target engagement can be measured in tissue. | Either treatment efficacy or target engagement need to be measured in a way that is more difficult than tissue inspection, e.g., biopsy.  | Treatment Efficacy and target engagement measurement need to be measured in a way that is more difficult than tissue inspection, e.g., biopsy. |
'''

ligand_binder_criteria = '''
1 = Target has a high-quality ligand reported. 
0 = Target does not have high-quality ligand reported.
NA = No information available.
'''

small_molecule_binder_criteria = '''
1 = Target has a small molecule reported. 
0 = Target does not have a small molecule reported.
NA = No information available.
'''

predicted_pocket_criteria = '''
1 = Target contains a high-quality predicted pocket. 
0 = Target does not have a high-quality predicted pocket.
NA= No information available.
'''

chemical_probes_criteria = '''
1 = Target has high-quality chemical probes.
0 = Target does not have high-quality chemical probes.
NA = No information available.
'''

gene_essentiality_criteria = '''
-1 = Target is essential.
0 = Target is not essential. 
NA = No information available.
'''