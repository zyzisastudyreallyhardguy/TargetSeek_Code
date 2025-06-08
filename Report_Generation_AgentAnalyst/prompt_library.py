starting = ''''Gene name: {gene_name}
    Disease name: {disease_name}\n'''
 
def moa_promot(gene_name, disease_name):
    text = starting + '''
    Summarize {gene_name}'s cell and molecular mechanism of action related to {disease_name}'''
    return text.format(gene_name = gene_name, disease_name = disease_name)

def in_vitro_vivo_promot(gene_name, disease_name):
    text = starting +  '''Please find in vitro and in vivo experimental evidence supporting {gene_name}'s role in {disease_name}.'''
    return text.format(gene_name = gene_name, disease_name = disease_name)

def assay_prompt(gene_name, disease_name):
    text = starting + '''
Evaluate the readiness of in vitro and in vivo assays to validate the discovery hypothesis for {gene_name} in {disease_name}'''   
    return text.format(gene_name = gene_name, disease_name = disease_name)

def competitive_prompt(gene_name, disease_name):
    text = '''Please summarize the drug discovery programs targeting {gene_name} in clinical and pre-clinical with different drug modalities. This includes small molecules, antibodies, and siRNA. Try you best to search and gather as much information as possible.'''
    return text.format(gene_name = gene_name)

def safety_prompt(gene_name, disease_name):
    text = '''Please search and summarize the safety profile of drug targeting {gene_name}'''
    return text.format(gene_name = gene_name, disease_name = disease_name)