import requests
import re
import pandas as pd
import time
from chembl_webresource_client.new_client import new_client

'''set_up_google_search_tool'''
import os
from langchain_community.utilities import GoogleSearchAPIWrapper
from langchain_google_community import GoogleSearchAPIWrapper
from langchain_core.tools import Tool

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

def google_search():
    # Verify API keys are set
    if not os.getenv("GOOGLE_CSE_ID") or not os.getenv("GOOGLE_API_KEY"):
        raise ValueError("Google Search API keys not configured. Please run setup_api_keys() first.")
        
    search = GoogleSearchAPIWrapper()
    k = 10
    delay = 3
    max_attempts = 5

    def top_k_results(query):
        attempts = 0
        while attempts < max_attempts:
            try:
                time.sleep(delay)
                return search.results(query, k)
            except Exception as e:
                attempts += 1
                print(f"Attempt {attempts} failed with error: {e}. Retrying...")
                time.sleep(delay)
        raise Exception("Maximum attempts reached. Could not complete the search.")

    google_tool = Tool(
        name="google_search",
        description="Search Google for recent results.",
        func=top_k_results,
    )
    return google_tool


def google_search_test(query):
    search = GoogleSearchAPIWrapper()
    k = 10
    return search.results(query, k)

def remove_references(text):
    # Remove all reference lines, both the numeric reference and the URL + quoted sentence.
    # This regex matches the reference pattern including optional whitespace and newlines
    cleaned_text = re.sub(r'\[\d+\] URL: .*\n\s*Quoted sentence: .*', '', text)
    # Additional cleanup to remove any orphaned reference numbers within the text
    cleaned_text = re.sub(r'\[\d+\]', '', cleaned_text)
    cleaned_text = re.sub(r'### References\n', '', cleaned_text)
    return cleaned_text.strip()

def clean_up_blank_lines(text):
    # Split the text into lines
    lines = text.split('\n')
    # Remove blank lines
    non_blank_lines = [line for line in lines if line.strip() != '']
    # Join the non-blank lines back into a single string
    cleaned_text = '\n'.join(non_blank_lines)
    return cleaned_text

def load_md_report(file_path):
    with open(file_path, 'r') as f:
        return f.read()

def markdown_report(gene_name, disease_name, gof_content, lof_content, analysis, moa_content, invitro_invivo_exp_content, druggability_content, competitive_edge_content, assay_design_content, safety_content, human_tissue_distribution_content):
    cwd_path = directory_set_up() + '/Report_Generation_AgentAnalyst'
    path = cwd_path + '/reports/' + disease_name.lower() + '/' + gene_name.lower() + '/'
    with open(path + 'report_' + gene_name.lower() + '_all.md', 'w') as f:
        gene_name = gene_name.upper()
        disease_name = disease_name.upper()
        f.write('# Gene Report\n')
        f.write('## Gene Name: ' + gene_name + '\n')
        f.write('## Disease Name: ' + disease_name + '\n')
        f.write('### 1.Genetic Evidence\n')
        f.write('#### Gain of Function\n' + gof_content + '\n')
        f.write('#### Loss of Function\n' + lof_content + '\n')
        f.write(analysis + '\n' )
        f.write('### 2.Mechanism of Action\n' + moa_content + '\n')
        f.write('### 3.Human Tissue Distribution\n' + human_tissue_distribution_content + '\n')
        f.write('### 4.In vitro/In vivo Experiment\n' + invitro_invivo_exp_content + '\n')
        f.write('### 5.Druggability Evaluation\n' + druggability_content + '\n')
        f.write('### 6.Competitive Edge\n' + competitive_edge_content + '\n')
        f.write('### 7.Assay Design\n' + assay_design_content + '\n')
        f.write('### 8.Safety Evaluation\n' + safety_content + '\n')

def markdown_report_section(gene_name, disease_name, section_name, content, save_file_directory=None):
    if gene_name.lower().split('_')[0] != 'itga4'.lower():
        gene_name = gene_name.lower().split('_')[0]
    elif gene_name.lower().split('_')[0] == 'itga4'.lower():
        gene_name = 'itga4_itgb7'
    
    print(save_file_directory)
    if save_file_directory:
        path = save_file_directory + '/'
    else:
        path = 'reports/' + disease_name + '/' + gene_name.lower() + '/'
    # lower case and replace space with underscore
    os.makedirs(path, exist_ok=True)
        
    section_name = section_name.lower().replace(' ', '_')
    with open(path + 'report_' + gene_name.lower() + '_' + section_name + '.md', 'w') as f:
        f.write('### ' + section_name + '\n' + content + '\n')

def get_gene_name_short(gene_name):
    first_part = gene_name.lower().split('_')[0]
    # if first_part != 'itga4':
    #     gene_name = first_part
    # else:
    #     gene_name = 'itga4_itgb7'
    return first_part

# Function to get gene expression info from human protein atlas
def get_gene_info(gene_name, tsv_file = 'tissue_distribution/rna_tissue_consensus.tsv', expression_level = False):
    prefix = directory_set_up() + '/Report_Generation_AgentAnalyst/'
    tsv_file = prefix + tsv_file
    # Read the TSV file into a DataFrame
    df = pd.read_csv(tsv_file, sep='\t')
    
    # change this to ignore the case gene_info = df[df['Gene name'] == gene_name]
    gene_info = df[df['Gene name'].str.lower() == gene_name.lower()]
    
    if gene_info.empty:
        return f"No information found for gene name: {gene_name}"
    
    # Calculate percentiles
    thresholds = {
        # "Very High": 100,
        "High": 50,
        "Moderate": 10,
        "Low": 5,
        "Very Low": 0
    }

    # Function to categorize expression level
    def categorize_expression(value):
        # if value > thresholds["Very High"]:
        #     return "Very High"
        if value > thresholds["High"]:
            return "High"
        elif value > thresholds["Moderate"]:
            return "Moderate"
        elif value > thresholds["Low"]:
            return "Low"
        else:
            return "Very Low"

    # Apply the function to the DataFrame
    gene_info["Expression Level"] = gene_info["nTPM"].apply(categorize_expression)

    # rank
    gene_info = gene_info.sort_values(by="nTPM", ascending=False)

    if expression_level:
        # Generate markdown table
        markdown_table = "| Tissue Type | Expression Value | Expression Level |\n"
        markdown_table += "|-------------|------------------|------------------|\n"
        for _, row in gene_info.iterrows():
            markdown_table += f"| {row['Tissue']} | {row['nTPM']} | {row['Expression Level']} |\n"
    else:
        # Generate markdown table
        markdown_table = "| Tissue Type | Expression Value |\n"
        markdown_table += "|-------------|------------------|\n"
        for _, row in gene_info.iterrows():
            markdown_table += f"| {row['Tissue']} | {row['nTPM']} |\n"

    return markdown_table

def get_gene_list(disease_name, prefix = None, get_full_name = False):
    gene_list = []
    if prefix is None:
        prefix = ''
    if disease_name == 'non_small_cell_lung_cancer':
        # load nsclc_gene_list.txt in gene_name_lists folder
        file_name = prefix + 'gene_name_lists/nsclc_gene_list.txt'
    elif disease_name == 'rheumatoid_arthritis':
        # load ra_gene_list.txt in gene_name_lists folder
        file_name = prefix + 'gene_name_lists/ra_gene_list.txt'
    elif disease_name == 'type2_diabetes':
        file_name = prefix + 'gene_name_lists/type2_gene_list.txt'
    elif disease_name == 'inflammatory_bowel_disease':
        file_name = prefix + 'gene_name_lists/ibd_gene_list.txt'
    elif disease_name == 'atherosclerosis':
        file_name = prefix + 'gene_name_lists/atherosclerosis_gene_list.txt'
    elif disease_name == 'metabolic_dysfunction_associated_steatohepatitis_mash':
        file_name = prefix + 'gene_name_lists/mash_gene_list.txt'
    # elif disease_name == 'non_alcoholic_steatohepatitis_nash':
    #     file_name = prefix + 'gene_name_lists/mash_gene_list.txt'
    # elif disease_name == 'non_alcoholic_fatty_liver_disease_nafld':
    #     file_name = prefix + 'gene_name_lists/mash_gene_list.txt'
    # elif disease_name == 'metabolic_dysfunction_associated_fatty_liver_disease_mafld':
    #     file_name = prefix + 'gene_name_lists/mash_gene_list.txt'
    if get_full_name:
        with open(file_name, 'r') as f:
            for line in f:
                gene_code = line.strip()
                gene_full_name = get_gene_full_name(gene_code)
                gene_full_name = gene_full_name.replace(' ', '_').lower()
                gene_list.append(gene_code + '_' + gene_full_name)
    else:
        with open(file_name, 'r') as f:
            for line in f:
                gene_list.append(line.strip())
    return gene_list


def get_gene_full_name(gene_code):
    # Base URL for the NCBI Gene database
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    
    # Parameters for the API request
    params = {
        "db": "gene",
        "term": f"{gene_code}[Gene Name]",
        "retmode": "json",
        "species": "human"
    }
    
    try:
        # Make the API request
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an exception for bad responses
        
        data = response.json()
        
        # Check if we got any results
        if int(data['esearchresult']['count']) > 0:
            gene_id = data['esearchresult']['idlist'][0]
            
            # Now fetch the gene details
            summary_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
            summary_params = {
                "db": "gene",
                "id": gene_id,
                "retmode": "json"
            }
            
            summary_response = requests.get(summary_url, params=summary_params)
            summary_response.raise_for_status()
            
            summary_data = summary_response.json()
            
            # Extract the full name
            full_name = summary_data['result'][gene_id]['description']
            
            return full_name
        else:
            return f"No gene found with code {gene_code}"
    
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {str(e)}"

def get_drug_info_for_target(target_gene):
    # Initialize ChEMBL clients
    target = new_client.target
    molecule = new_client.molecule
    mechanism = new_client.mechanism

    try:
        # Search for the targets
        targets = target.search(target_gene)
        
        if not targets:
            print(f"No targets found for gene: {target_gene}")
            return
        
        file_name = 'drug_info/' + target_gene + "_drug_info.txt"
        
        with open(file_name, 'w') as file:
            for target_info in targets:
                target_chembl_id = target_info['target_chembl_id']
                
                # Get mechanisms of action for the target
                mechanisms = mechanism.filter(target_chembl_id=target_chembl_id)
                
                if not mechanisms:
                    continue
                
                # file.write(f"Drug and clinical candidate information for {target_gene} (ChEMBL ID: {target_chembl_id}):\n")
                
                for mech in mechanisms:
                    mol = molecule.get(mech['molecule_chembl_id'])
                    
                    file.write(f"\nMolecule: {mol['pref_name'] or mol['molecule_chembl_id']}\n")
                    file.write(f"ChEMBL ID: {mol['molecule_chembl_id']}\n")
                    file.write(f"Mechanism of Action: {mech['action_type']}\n")
                    file.write(f"Max Phase: {mol['max_phase']}\n")
                    file.write(f"Molecule Type: {mol['molecule_type']}\n")
                    
                    if mol['first_approval']:
                        file.write(f"First Approval: {mol['first_approval']}\n")
        
        #return the file content
        with open(file_name, 'r') as file:
            return file.read()
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == '__main__':
    result = google_search_test('what is happiness')
    print(result)