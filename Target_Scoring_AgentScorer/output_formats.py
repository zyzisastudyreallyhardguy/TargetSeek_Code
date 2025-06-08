genetic_association_output_format = '''
| Disease Phenotype | Gene Variant Traits | Rating | Rationale of Rating |
|-------------------|---------------------|--------|---------------------|
| Consider the specific characteristics and symptoms associated with {disease_name}. | Analyze how the variants of {gene_name} influence the disease phenotype. | After evaluating the content, select a category from the following options: [Strong - positive (+1), Weak - positive (+0.5), Neutral (0), Weak - negative (-0.5), Strong - negative (-1)]. **Only put the category and say nothing else** | Illustrate why you give this rating |
    '''

differential_expression_output_format = '''
| Gene Expression | Rationale of Rating | Rating |
|-----------------|---------------------|--------|
| Is it differentially expressed during disease progression (this is a strong positive sign)?/Is {gene_name} specifically differentially expressed in the disease tissue (this is a weak positive sign)?/ Is {gene_name} expression pattern of the target gene is not clear (this is a neutral sign)? /Is {gene_name} ubiquitously expressed (this is a weak negative sign)?/ If {gene_name} is not expressed in the disease tissue, it is a strong negative sign. | Illustrate why you give this rating | After evaluating the content, select a category from the following options: [Strong - positive (+1), Weak - positive (+0.5), Neutral (0), Weak - negative (-0.5), Strong - negative (-1)]. **Only put the category and say nothing else** |
'''

moa_output_format = '''
| Molecular Mechanism of the target | Rating | Rationale of Rating |
|-----------------------------------|--------|---------------------|
| you have to illustrate the relatedness of molecular mechanism of {gene_name} with the {disease_name} | After evaluating the content, select a category from the following options: [Strong - positive (+1), Weak - positive (+0.5), Neutral (0), Weak - negative (-0.5), Strong - negative (-1)]. **Only put the category and say nothing else** | Illustrate why you give this rating. Why it is the category, not others? |
    '''

in_vitro_vivo_output_format = '''
| Evidence supporting target gene and disease progression | Rating | Rationale of Rating |
|---------------------------------------------------------|--------|---------------------|
| Is {gene_name} for {disease_name} being evaluated on in human, cell or animal perturbation? Any conflict results? | After evaluating the content, select a category from the following options: [Strong - positive (+1), Weak - positive (+0.5), Neutral (0), Weak - negative (-0.5), Strong - negative (-1)]. **Only put the category and say nothing else** | Illustrate why you give this rating |
    '''

small_molecule_output_format = '''
| Data Availability | Rating | Rationale of Rating |
|-------------------|--------|---------------------|
| - Are there any existing small molecule drugs on {gene_name}? - Are crystal structures available? (If yes, then if there is an obvious pocket site?) - Are there tool compounds for {gene_name}? | After evaluating the content, select a category from the following options:<br>[Strong - positive (+1), Weak - positive (+0.5), Neutral (0), Weak - negative (-0.5), Strong - negative (-1)]. **Only put the category and say nothing else** | Illustrate why you give this rating |
'''

antibody_output_format = '''
| Data Availability | Rating | Rationale of Rating |
|--------------------|--------|---------------------|
| Are there any existing antibodies drugs on {gene_name}? <br> Are experimental antibodies available that modulates the target {gene_name}? | After evaluating the content, you **can only select a category from the following options**: <br> **[Strong - positive (+1), Weak - positive (+0.5), Neutral (0), Weak - negative (-0.5), Strong - negative (-1)]** <br> **Only put the category and say nothing else** | Illustrate why you give this rating |
'''

sirna_output_format = '''
| Tissue Distribution | Rating | Rationale of Rating |
|---------------------|--------|---------------------|
| Which tissues and organs are the target {gene_name} mainly expressed? Which tissues and organs are the target {gene_name} mainly function? Are there good sirna strategy so far and is the therapeutic direction clear? | After evaluating the content, you **can only select a category from the following options**: <br> **[Strong - positive (+1), Weak - positive (+0.5), Neutral (0), Weak - negative (-0.5), Strong - negative (-1)]** <br> **Only put the category and say nothing else** | Illustrate why you give this rating |


| After evaluating the content, you **can only select a category from the following options**: <br> **[Strong - positive (+1), Weak - positive (+0.5), Neutral (0), Weak - negative (-0.5), Strong - negative (-1)]** <br> **Only put the category and say nothing else** | Illustrate why you give this rating |
'''

competitiveness_output_format = '''
| Drug Development Pipelines Information | Rating | Rationale of Rating |
|----------------------------------------|--------|---------------------|
| Are there drug development activities and pipelines of {gene_name} for {disease_name}? (Only consider those pipelines for {disease_name}) | After evaluating the content, you **can only select a category from the following options**: <br> **[Strong - positive (+1), Weak - positive (+0.5), Neutral (0), Weak - negative (-0.5), Strong - negative (-1)]** <br> **Only put the category and say nothing else** | Illustrate why you give this rating |
'''

competitiveness_small_molecule_output_format = '''
| Small Molecule Drug Development Pipelines Information | Rating | Rationale of Rating |
|-------------------------------------------------------|--------|---------------------|
| Are there small molecule drug development activities and pipelines of {gene_name} for {disease_name}? | After evaluating the content, you **can only select a category from the following options**: <br> **[Strong - positive (+1), Weak - positive (+0.5), Neutral (0), Weak - negative (-0.5), Strong - negative (-1)]** <br> **Only put the category and say nothing else** | Illustrate why you give this rating |
'''

competitiveness_sirna_or_antibody_output_format = '''
| siRNA or Antibody Drug Development Pipelines Information | Rating | Rationale of Rating |
|----------------------------------------------------------|--------|---------------------|
| Are there siRNA or antibody drug development activities and pipelines of {gene_name} for {disease_name}? | After evaluating the content, you **can only select a category from the following options**: <br> **[Strong - positive (+1), Weak - positive (+0.5), Neutral (0), Weak - negative (-0.5), Strong - negative (-1)]** <br> **Only put the category and say nothing else** | Illustrate why you give this rating |
'''

assayability_output_format = '''
| Models Availability | Rating | Rationale of Rating |
|----------------------|--------|---------------------|
| Ask yourself these questions. Are there existing animal and cellular models available for {gene_name} in {disease_name}? Have these models been tested on tool compounds or genetic perturbation? | After evaluating the content, you **can only select a category from the following options**: <br> **[Strong - positive (+1), Weak - positive (+0.5), Neutral (0), Weak - negative (-0.5), Strong - negative (-1)]** <br> **Only put the category and say nothing else** | Illustrate why you give this rating |
'''

assayability_biomarker_output_format = '''
| Biomarker | Rating | Rationale of Rating |
|-----------|--------|---------------------|
|  | After evaluating the content, you **can only select a category from the following options**: <br> **[Strong Positive (+1), Weak Positive (+0.5), Neutral (0), Weak Negative (-0.5), Negative (-1)]** <br> **Only put the category and say nothing else** | Illustrate why you give this rating |
'''

unmet_need_output_format = '''
| Unmet Need | Rating | Rationale of Rating |
|------------|--------|---------------------|
| | After evaluating the content, you **can only select a category from the following options [Strong - positive (+1), Weak - positive (+0.5), Neutral (0), Weak - negative (-0.5), Strong - negative (-1)] Only put the category and say nothing else** | Illustrate why you give this rating |
'''

target_safety_output_format = '''
| Safety-related Information | Rating | Rationale of Rating |
|-----------------------------|--------|---------------------|
| What is the desired therapeutic effect of {gene_name} for {disease_name}? Are there any approved drugs targeting {gene_name} for {disease_name}? If yes, are they generally considered as safe? Are there any animal studies of {gene_name}? Are there any side effects in these animal studies? | After evaluating the content, you **can only select a category from the following options**: <br> **[Strong - positive (+1), Weak - positive (+0.5), Neutral (0), Weak - negative (-0.5), Strong - negative (-1)]** <br> **Only put the category and say nothing else** | Illustrate why you give this rating |
'''

moa_match_output_format = '''
| MOA Match | Rating | Rationale of Rating |
|-----------|--------|---------------------|
| Does the mechanism of action of the {gene_name} for {disease_name} match the user preferred MOA: {user_preference}? | After evaluating the content, you **can only select a category from the following options** from the following options: <br> **[Positive (+1),  Neutral (0), Negative (-1)]** <br> **Only put the category and say nothing else** | Illustrate why you give this rating |
'''

opentarget_output_format = '''
{{'Score': '',
'Rationale': 'I give this score because...'}}
'''