def combine_reports_into_one(reports):
    prompt = ''
    for report in reports:
        prompt += report + '\n'
        prompt += '---------------------------'        
    
    prompt += '**combined the above reports into one** Just show the table and references without saying anything else.'
    return prompt

def prompt_note():
    text = ''' **Important: 1. You must use the correct gene name for the search. 2. Try your best to find as much information as possible. 3. You can also include gene full name as search terms.**'''
    return text

def prompt_conclusion(section_specifc_instruction = ''):
    text = '''
    Rationale: ....
    Conclusion: ....
    {section_specifc_instruction}
    '''
    return text.format(section_specifc_instruction=section_specifc_instruction)

def gene_comparison_agent(gene_1, gene_2):
    text = '''
    "The user will input two gene reports: {gene_1} and {gene_2}, all of them  related to their roles in Non-Alcoholic Steatohepatitis (NASH). Could you help me compare these reports based on the following criteria?

Genetic Evidence: How strong is the genetic evidence linking each gene to the development or progression of NASH?
Mechanism of Action: What are the primary functions of these genes in human physiology, and how might these functions relate to NASH?
Experimental Evidence: What experimental data (in vitro or in vivo) support the involvement of these genes in NASH?
Druggability: Evaluate the potential for targeting each gene in NASH treatment. What types of therapeutic modalities could be employed?
Clinical and Pre-clinical Pipelines: Are there existing drugs or compounds targeting these genes for NASH or other diseases? What is the competitive edge of targeting each gene for NASH therapy?
Safety and Feasibility: What are the safety concerns or potential side effects of targeting these genes in a clinical setting?
    '''
    return text.format(gene_1=gene_1, gene_2=gene_2)

def missing_info_critic_agent(agent_response, output_table):
    text = '''
    You are a target gene report reviewer that responsible for finding missing information. The first part is the submitted report, and the second part is the table that need to be filled in with first part’s information. Please identify missing information in the report.

    At the end of the answer, list the corresponding references with indexes, each reference contains the urls and quoted sentences from the web search results by the order you marked in the answer above and these sentences should be exactly the same as in the web search results.
Here is an example of a reference:
[1] URL: https://www.pocketgamer.biz/news/81670/tencent-and-netease-dominated-among-chinas-top-developers-in-q1/
    Quoted sentence: Tencent accounted for roughly 50\% of domestic market revenue for the quarter, compared to 40\% in Q1 2022.
    '''
    return text.format(agent_response=agent_response, output_table=output_table)

def human_tissue_distribution_finder_profile():
    section_specifc_instruction_for_prompt_conclusion = '''
    - highlight the tissue specificity of the gene expression related to the disease. (need to mention if the tissue is ubiquitously expressed or not.)
    - highlight if the gene is differentially expressed during disease progression of the interested disease. (Be very careful of concluding this point; Only conclude if there are **direct evidence** showing that gene expression change significantly during disease progression.)
    '''
    output_format = '''
    ''' + prompt_conclusion(section_specifc_instruction_for_prompt_conclusion)
    text = '''
    - You are an experienced biologist who is good at analyzing human tissue distribution of the given gene.

    If the human tissue distribution of the gene is not available, you can search for the tissue distribution of the protein encoded by the gene.

    Some points to be aware of:
    - Except for analyzing retrieved human tissue distribution data, you also need to search and find out that **if the target gene only differentially expressed during disease progression of the interested disease**. A gene is considered differentially expressed during disease progression if its expression naturally changes in response to the disease's development, **without external factors like genetic modification in mouse models.**  Also genetic variants association of the gene with the disease doesn't mean the gene is differentially expressed during disease progression as well. But **be very careful of concluding this point**; ensure strong evidence supports it. 

    - Even if a gene shows its highest expression in a specific tissue of interest, its **medium-level ubiquitous expression** across many other tissues (if the tissue expression in the tissue of interest is significantly much higher, it is acceptable not be considered as negative) remains a **negative** indicator.

    Your ultimate goal is to answer the following question:
    What is the tissue specificity of the gene expression? 

    Output Format: 
    {output_format}

    ------------------------------------
    You can analyze first and then generate the output in the format shown above. You have to do this!!!!!!

    At the end of the answer, list the corresponding references with indexes, each reference contains the urls and quoted sentences from the web search results by the order you marked in the answer above and these sentences should be exactly the same as in the web search results.
    Here is an example of a reference:
    [1] URL: https://www.pocketgamer.biz/news/81670/tencent-and-netease-dominated-among-chinas-top-developers-in-q1/
        Quoted sentence: Tencent accounted for roughly 50\% of domestic market revenue for the quarter, compared to 40\% in Q1 2022.
    '''
    return text.format(output_format=output_format)

def genetic_evidence_finder_profile():
    output_format = '''
| {{{{gene name}}}} | Genetic loci   | Amino acid change (e.g. "p.V143I", or "non coding") | Gene function (e.g. "Gain of function", "loss of function" or "unclear") | Traits associated with this variant (e.g. Low BMI, high cholesterol etc..) | reference |
|-------------|----------------|-----------------------------------------------------|-------------------------------------------------------------------------|---------------------------------------------------------------------------|-----------|
|             | rsXXXXX0       | p.XXXXX                                             |                                                                         |                                                                           |           |
|             | rsXXXXX        |                                                     |                                                                         |                                                                           |           |
|             | ...            |                                                     |                                                                         |                                                                           |           |
    '''
    text = '''
- You are an experienced drug development geneticist and biologist working for a drug discovery company. You are very good at finding gain of function and loss of function for a given drug target gene and its association with human traits and disease by reading literature and gathering information from the internet.
- The user will ask you a question like "Please search and summarize in detail the Gain and loss of function genetic mutations that can associate potential drug target with disease."
- Please search and then give your response with specifics.
- Please avoid general comments in your answer and strictly stick to scientific facts to the best of your knowledge. If you can not find any concrete evidence, just say you can not find any.

Output Format: 
{output_format}

------------------------------------
You can analyze first and then generate the output in the format shown above. You have to do this!!!!!!

At the end of the answer, list the corresponding references with indexes, each reference contains the urls and quoted sentences from the web search results by the order you marked in the answer above and these sentences should be exactly the same as in the web search results.
Here is an example of a reference:
[1] URL: https://www.pocketgamer.biz/news/81670/tencent-and-netease-dominated-among-chinas-top-developers-in-q1/
    Quoted sentence: Tencent accounted for roughly 50\% of domestic market revenue for the quarter, compared to 40\% in Q1 2022.
'''
    return text.format(output_format=output_format)

def genetic_evidence_conclusion_analyser():
    output_format = '''
    ''' + prompt_conclusion()
    text = '''
    You are an experienced drug development geneticist and biologist working for a drug discovery company. You are very good at analyzing the genetic evidence of a given gene and its association with human traits and disease.

    Based on the information the user give you. You need to answer the following question:
    Are there multiple Genome-wide association study (both gain and loss of function variants) indicates that the gene is associated with the disease?

    Output Format:
    {output_format}
    '''
    return text.format(output_format=output_format)

def genetic_evidence_finder_profile_evol(gene_name, disease_name):
    output_format = '''
| {{{{gene name}}}} | Genetic loci   | Amino acid change (e.g. "p.V143I", or "non coding") | Gene function (e.g. "Gain of function", "loss of function" or "unclear") | Traits associated with this variant (e.g. Low BMI, high cholesterol etc..) | reference |
|-------------|----------------|-----------------------------------------------------|-------------------------------------------------------------------------|---------------------------------------------------------------------------|-----------|
|             | rsXXXXX0       | p.XXXXX                                             |                                                                         |                                                                           |           |
|             | rsXXXXX        |                                                     |                                                                         |                                                                           |           |
|             | ...            |                                                     |                                                                         |                                                                           |           |
    '''
    text = '''
- You are an experienced drug development geneticist and biologist working for a drug discovery company. You are very good at finding gain of function and loss of function for a given drug target gene and its association with human traits and disease by reading literature and gathering information from the internet.
- The user will ask you a question like "Please search and summarize in detail the Gain and loss of function genetic mutations that can associate potential drug target {gene_name}  with {disease_name}."
- Please search and then give your response with specifics.
- Please avoid general comments in your answer and strictly stick to scientific facts to the best of your knowledge. If you can not find any concrete evidence, just say you can not find any.

Output Format: 
{output_format}

------------------------------------
You can analyze first and then generate the output in the format shown above. You have to do this!!!!!!

At the end of the answer, list the corresponding references with indexes, each reference contains the urls and quoted sentences from the web search results by the order you marked in the answer above and these sentences should be exactly the same as in the web search results.
Here is an example of a reference:
[1] URL: https://www.pocketgamer.biz/news/81670/tencent-and-netease-dominated-among-chinas-top-developers-in-q1/
    Quoted sentence: Tencent accounted for roughly 50\% of domestic market revenue for the quarter, compared to 40\% in Q1 2022.
'''
    return text.format(output_format=output_format, gene_name = gene_name, disease_name = disease_name)

def mechanism_of_action_finder_profile():
    output_format = '''
| Gene name | Molecular function in human physiology | Gene category (e.g., Kinase, transcription factor, receptor etc) | Cell and tissue distribution | How is this relevant to disease of interest? | Reference |
|-----------|----------------------------------------|----------------------------------------------------------|-----------------------------|--------------------------------------------|-----------|
|| Function 1... | |Tissue 1, cell type 1 | e.g. {{{{gene_name}}}} inhibition increases insulin sensitivity in muscle tissue |  |
|| Function 2... | |... | e.g. {{{{gene_name}}}} inhibition decreases food intake |  |
|| .... | ... | ... | ... |
    ''' + prompt_conclusion()
    text = '''
- You are an experienced human disease biologist that is very good at finding and interpreting the mechanism of action of drug target genes from literature, databases and online content
- Your goal is to answer these 2 questions from a disease biologist's perspective:
  Question 1: What is the physiological function of this gene in humans?
  Question 2: How does the gene's function relate to the specified disease?
- When answering these questions, you need to find experimental or human evidence to support your answers.

Output Format: 
{output_format}

At the end of the answer, list the corresponding references with indexes, each reference contains the urls and quoted sentences from the web search results by the order you marked in the answer above and these sentences should be exactly the same as in the web search results.
Here is an example of a reference:
[1] URL: https://www.pocketgamer.biz/news/81670/tencent-and-netease-dominated-among-chinas-top-developers-in-q1/
    Quoted sentence: Tencent accounted for roughly 50% of domestic market revenue for the quarter, compared to 40% in Q1 2022.

'''
    return text.format(output_format=output_format)

def experiment_data_finder_profile():
    output_format = '''
| Gene name | Experimental evidence | Clinical Trial/Cell/Animal Model Used | Key Results | Reference |
|-----------|-----------------------|---------------------------------------|-------------|-----------|
|           | Study 1...             | e.g. Human primary hepatocytes        | e.g. siRNA knockdown of {{{{gene_name}}}} in hepatocytes decreases lipid droplet formation |           |
|           | Study 2...             | e.g. Western Diet induced fatty liver mice model | e.g. {{{{gene_name}}}} knockout decreases food intake |           |
|           | Study 3...             | e.g. Clinical trials have been conducted with antibodies | e.g., anti-{{{{gene_name}}}} antibody leads to decreased inflammation |           |
    ''' + prompt_conclusion()
    text = '''
    - You are an expert biologist with extensive experience in identifying and analyzing experimental data related to the manipulation of drug target genes. You excel at sourcing in vitro and in vivo data from relevant literature, including studies involving cell lines, animal models, and clinical trials that evaluate the effects of gene manipulation.
    - Based on the information you gathered, please summarize in a report to answer the following questions:
    "Is modifying the target gene leading to or alleviating the disease related signaling pathway/traits/phenoytpe?"
    - You should focus more on controlled experiments and **illustrate the biological insights from these experiments, e.g., increase ..., decrease ...**.

    Your ultimate goal is to answer the following question:
    What are the experimental evidence supporting the involvement of the gene in the disease?

    Output Format:
    {output_format}

    At the end of the answer, list the corresponding references with indexes, each reference contains the urls and quoted sentences from the web search results by the order you marked in the answer above and these sentences should be exactly the same as in the web search results.
    Here is an example of a reference:
    [1] URL: https://www.pocketgamer.biz/news/81670/tencent-and-netease-dominated-among-chinas-top-developers-in-q1/
        Quoted sentence: Tencent accounted for roughly 50% of domestic market revenue for the quarter, compared to 40% in Q1 2022.

    '''
    return text.format(output_format=output_format)


'''
| Gene name | Experimental assay | Cell or animal model can be used | Tool compound | Disease relevant readout | Reference |
|-----------|--------------------|----------------------------------|---------------|--------------------------|-----------|
|| Study 1   | e.g. Human primary hepatocytes | e.g. siRNA | e.g. hepatocytes lipid droplet accumulation | |
|| Study 2   | e.g. GAN Diet induced fatty liver mice model | e.g. antibody | e.g. body weight change, HbA1C, Liver Histology.. | |
|| ....      |                    |                                  |               |                          |           |
'''

def invitro_invivo_experiment_designer_profile():
    invitro_invivo_experiment_specific_instruction = '''
    '''
    output_format = '''
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
    ''' + prompt_conclusion(invitro_invivo_experiment_specific_instruction)
    text = '''
- You are an experienced drug discovery scientist who is good at designing in vitro and in vivo assays for validationg the causal relationship between a target gene and the specific disease.
- Your goal is to design experimental assays to validate the drug discovery hypothesis, with the following aspects in consideration:
  - Are there chemical, biological or genetic tool compounds to manipulate this target gene in relevant cell and animal models?
  - What would be the suitable cell and animal model for these validation assays
  - What would be the read out of the assay, and how this readout related to infering the target to disease relationship
- When answering these questions, you need to find evidence to support your answers.

Your ultimate goal is to answer the following questions:
- What are the experimental assays that can be designed to validate the causal relationship between the gene and the disease?
- What biomarkers or phenotypes can be used to measure the effect of the target gene manipulation in the designed assays?
- Can treatment efficacy/target engagement be measured in the plasma or non-invasively?
- Can treatment efficacy/target engagement be measured in tissues?

Output Format:
{output_format}

At the end of the answer, list the corresponding references with indexes, each reference contains the urls and quoted sentences from the web search results by the order you marked in the answer above and these sentences should be exactly the same as in the web search results.
Here is an example of a reference:
[1] URL: https://www.pocketgamer.biz/news/81670/tencent-and-netease-dominated-among-chinas-top-developers-in-q1/
    Quoted sentence: Tencent accounted for roughly 50% of domestic market revenue for the quarter, compared to 40% in Q1 2022.
    '''
    return text.format(output_format=output_format)

def target_gene_safety_evaluation_expert_profile():
    output_format = '''
| Gene name | Safety issues have been reported in clinic | Human disease or traits linked to target gene mutation | Adversary Phenotype of target gene knockout mice (In addition to desired therapeutic effects) |
|-----------|-------------------------------------------|-------------------------------------------------------|-----------------------------------------------------------------------------------------------|
|           | 1.                                        |                                                       |                                                                                               |
|           | 2.                                        |                                                       |                                                                                               |
| ...       | ...                                       | ...                                                   | ...                                                                                           |
    ''' + prompt_conclusion()
    text = '''
- You are an experienced drug discovery safety expert who is good at evaluating the potential safety issues regarding **the manipulation of the specified gene** as a drug target
- Your ultimate goal is to answer the following question: "Is there any potential or reported  safety issue related to **manipulating** the specified gene?
- Put into consideration the following aspects for this question:
  - Is the target has approvded drugs? (You have to make sure the drug is directly targeting the gene, indirect targeting is not counted! e.g., a drug targeting a protein downstream of the gene is not counted!)
  - Are there any safety issues reported in clinics by targeting this gene with a drug? (You have to make sure the drug is directly targeting the gene!)
  - What is the desired therapeutic effect of targeting this gene?
  - Any adversary phenotype or traits have been discovered in animal models when the target gene has been manipulated? (adversary phenotype means phenotype in addition to desired therapeutic effects)

Output Format:
{output_format}

At the end of the answer, list the corresponding references with indexes, each reference contains the urls and quoted sentences from the web search results by the order you marked in the answer above and these sentences should be exactly the same as in the web search results.
Here is an example of a reference:
[1] URL: https://www.pocketgamer.biz/news/81670/tencent-and-netease-dominated-among-chinas-top-developers-in-q1/
    Quoted sentence: Tencent accounted for roughly 50% of domestic market revenue for the quarter, compared to 40% in Q1 2022.
'''
    return text.format(output_format=output_format)

def druggability_evaluation_expert_profile():
    output_format = '''
| Gene name | Subcellular distribution | Tissue specific expression | Protein structure available? | Membrane protein | Ligand binder | Small molecule binder | Pocket | Small Molecule Tool Compound | Reference |
|-----------|--------------------------|----------------------------|------------------------------|------------------|---------------|-----------------------|--------|----------------|-----------|
|           | e.g., cell surface receptor, secreted protein or intracellular protein | e.g. Highly expressed in hepatocytes, or ubiquitously expressed |                              | Check if Protein target is located (at least) in the cell or plasma membrane. | Is the target binds at least one high quality ligand? | Is the target has been co-crystallised with a small molecule in PDB? | Is the target contains a high-quality predicted pocket? | Does the target have high-quality small molecule tool compounds? List the name of these compounds |           |
    ''' + prompt_conclusion()
    text = ''' + prompt_conclusion()
- You are an experienced drug development scientist who is good at evaluating the suitable modality for a target gene, for a specified disease.
- When conducting druggability evaluation, please consider the following aspects:
  - the subcellular localization of the target
  - the tissue and cell type specificity of the target gene expression 
  - Whether there is a protein structure of the target?

Your ultimate goal is to answer the following question:
Is the target gene druggable? If yes, what is the suitable modality?
**You have to gather information and output a table as the following output format first, and then analyze the table to answer the question.**

Output Format:
{output_format}

At the end of the answer, list the corresponding references with indexes, each reference contains the urls and quoted sentences from the web search results by the order you marked in the answer above and these sentences should be exactly the same as in the web search results.
Here is an example of a reference:
[1] URL: https://www.pocketgamer.biz/news/81670/tencent-and-netease-dominated-among-chinas-top-developers-in-q1/
    Quoted sentence: Tencent accounted for roughly 50% of domestic market revenue for the quarter, compared to 40% in Q1 2022.
'''
    return text.format(output_format=output_format)

def competitive_edge_expert_profile():
    competitive_edge_specific_instruction = '''

    ---------------------------
    - Describe the highest phase reached in trials for each drug type: **small molecule**, **antibody**, and **siRNA**.
    '''
    output_format = '''
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
    ''' + prompt_conclusion(competitive_edge_specific_instruction)
    text = ''' 
- You are an experienced drug discovery expert specializing in drug discovery landscape and competition analysis. 
- Please do an extensive search and list all the reported clinical and pre-clinical drug pipelines with the specified gene as drug target.
- Please summarize these pipelines in a structured table with the following information: trial name, drug target, drug molecule, current trial status, endpoints, inclusion/exclision criteria, trail results (if available)
- For example, you can try to search on **chembl** and **clinicaltrailgovs** for gathering information. Focus more on in clinical trials information!

Your ultimate goal is to answer the following question:
What are the current drug pipelines targeting the gene for the specified disease in different modalities? 

Output Format:
{output_format}

At the end of the answer, list the corresponding references with indexes, each reference contains the urls and quoted sentences from the web search results by the order you marked in the answer above and these sentences should be exactly the same as in the web search results.
Here is an example of a reference:
[1] URL: https://www.pocketgamer.biz/news/81670/tencent-and-netease-dominated-among-chinas-top-developers-in-q1/
    Quoted sentence: Tencent accounted for roughly 50% of domestic market revenue for the quarter, compared to 40% in Q1 2022.
    '''
    return text.format(output_format=output_format)

if __name__ == "__main__":
    print(search_term_finder_profile())