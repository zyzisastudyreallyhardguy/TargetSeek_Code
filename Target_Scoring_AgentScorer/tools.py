from langchain_openai import ChatOpenAI
from langchain import ConversationChain
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage
from Target_Scoring_AgentScorer.instructions import generate_final_table_instruction
# try:
from chembl_webresource_client.new_client import new_client
# except ImportError:
#     new_client = None
from concurrent.futures import ProcessPoolExecutor
import pandas as pd
import requests
import json
import re
import os

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

def map_ratings_to_categories(gene_ratings):
    # Define the category keys in the required order
    categories = [
        "CI_Genetic Association", "CI_Differential expression", "CI_Mechanism of Action", 
        "CI_In vitro_in vivo experiment", "T_Small molecules", "T_Antibody", "T_siRNA", 
        "CP_Competitiveness_Small_Molecules", "CP_Competitiveness_Antibody_or_siRNA", "CP_Unmet needs", "DO_experimental_model_availability", 
        "DO_biomarkers", "DO_Safety"
    ]
    
    # Initialize a dictionary to hold the mapped ratings
    mapped_ratings = {}

    # Iterate over the gene ratings dictionary
    for gene, ratings in gene_ratings.items():
        # Map each rating to its respective category
        mapped_ratings[gene] = {category: rating for category, rating in zip(categories, ratings)}
    
    return mapped_ratings

# store the final results in a csv file (append)
def store_final_results(ratings_of_genes, disease_name, file_type= 'direct'):

    cwd_path = directory_set_up()
    # Define the file path
    file_path = f"{cwd_path}/Target_Scoring_AgentScorer/scoring_result/overall_results/{disease_name.lower()}/{disease_name}_final_results.csv"

    # if the file path not exist, create one
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))
    
    # Check if the file exists
    if not os.path.exists(file_path):
        # Create the file if it does not exist
        with open(file_path, "w") as file:
            # Write the header
            file.write("Gene,CI_Genetic Association,CI_Differential expression,CI_Mechanism of Action,CI_In vitro_in vivo experiment,T_Small molecules,T_Antibody,T_siRNA,CP_Competitiveness_Small_Molecules,CP_Competitiveness_Antibody_or_siRNA,CP_Unmet needs,DO_experimental_model_availability,DO_biomarkers,DO_Safety\n")
    
    # Append the final results to the file
    with open(file_path, "a") as file:
        for gene, ratings in ratings_of_genes.items():
            # Write the gene name
            file.write(f"{gene},")
            
            # Write the ratings
            for rating in ratings.values():
                file.write(f"{rating},")
            
            # Move to the next line
            file.write("\n")

def tidy_json(input_str):
    try:
        # Load the input string as JSON
        data = json.loads(input_str)
        # Extract the required parts
        result = {
            "Score": data["Score"],
            "Rationale": data["Rationale"]
        }
        # Convert the result back to a JSON string with formatted output
        tidy_str = json.dumps(result, indent=4)
        return tidy_str
    except json.JSONDecodeError:
        return "Invalid JSON input"
    except KeyError as e:
        return f"Missing key in input: {e}"

def get_drug_info_for_target(target_gene):
    # Initialize ChEMBL clients
    target = new_client.target
    molecule = new_client.molecule
    mechanism = new_client.mechanism

    # Search for the targets
    targets = target.search(target_gene)
    
    if not targets:
        print(f"No targets found for gene: {target_gene}")
        return
    
    file_name = target_gene + "_drug_info.txt"
    
    with open(file_name, 'w') as file:
        for target_info in targets:
            target_chembl_id = target_info['target_chembl_id']
            print(f"\nProcessing target: {target_chembl_id}")
            
            # Get mechanisms of action for the target
            mechanisms = mechanism.filter(target_chembl_id=target_chembl_id)
            
            if not mechanisms:
                print(f"No mechanisms found for target: {target_chembl_id}")
                continue
            
            file.write(f"Drug and clinical candidate information for {target_gene} (ChEMBL ID: {target_chembl_id}):\n")
            print(f"Drug and clinical candidate information for {target_gene} (ChEMBL ID: {target_chembl_id}):")
            
            for mech in mechanisms:
                mol = molecule.get(mech['molecule_chembl_id'])
                
                file.write(f"\nMolecule: {mol['pref_name'] or mol['molecule_chembl_id']}\n")
                file.write(f"ChEMBL ID: {mol['molecule_chembl_id']}\n")
                file.write(f"Mechanism of Action: {mech['action_type']}\n")
                file.write(f"Max Phase: {mol['max_phase']}\n")
                file.write(f"Molecule Type: {mol['molecule_type']}\n")
                
                print(f"\nMolecule: {mol['pref_name'] or mol['molecule_chembl_id']}")
                print(f"ChEMBL ID: {mol['molecule_chembl_id']}")
                print(f"Mechanism of Action: {mech['action_type']}")
                print(f"Max Phase: {mol['max_phase']}")
                
                if mol['first_approval']:
                    file.write(f"First Approval: {mol['first_approval']}\n")
                    print(f"First Approval: {mol['first_approval']}")

def testChat():
    model = ChatOpenAI(
        openai_api_key=os.environ["OPENAI_API_KEY"],
        max_tokens=4096,
        model_name='gpt-4o-2024-05-13'
    )
    return model

def conversation(llm, user_input):
    conversation = ConversationChain(llm=llm)
    response = conversation(user_input)
    return response['response']

def load_json(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

def get_gene_info_expression_atlas(gene_name):
    data = get_gene_expression(gene_name)

    # Extract the expressions data
    expressions = data['data']['target']['expressions']
    
    # Sort expressions by value in descending order
    sorted_expressions = sorted(expressions, key=lambda x: x['rna']['value'], reverse=True)
    
    # Generate markdown table
    markdown_table = "| Tissue Type | Expression Value |\n"
    markdown_table += "|-------------|------------------|\n"
    
    for expression in sorted_expressions:
        tissue = expression['tissue']['label']
        value = expression['rna']['value']
        unit = expression['rna']['unit'] if expression['rna']['unit'] else 'N/A'
        
        # Add row to table
        markdown_table += f"| {tissue} | {value} {unit} |\n"
    
    return markdown_table

def get_gene_expression(gene_name):
    """
    Fetch gene expression data from OpenTargets API for a given Ensembl ID.
    
    Args:
    ensembl_id (str): The Ensembl ID of the gene.
    
    Returns:
    dict: A dictionary containing the gene expression data, or None if the request fails.
    """
    ensembl_id = get_ensembl_id(gene_name)

    # OpenTargets GraphQL API endpoint
    url = "https://api.platform.opentargets.org/api/v4/graphql"

    # GraphQL query
    query = """
    query GeneExpression($ensemblId: String!) {
      target(ensemblId: $ensemblId) {
        id
        approvedSymbol
        expressions {
          tissue {
            id
            label
          }
          rna {
            value
            unit
          }
        }
      }
    }
    """

    # Variables for the query
    variables = {
        "ensemblId": ensembl_id
    }

    # Combine query and variables
    payload = {
        "query": query,
        "variables": variables
    }

    try:
        # Make the POST request
        response = requests.post(url, json=payload)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            result = response.json()
            return result
        else:
            print(f"Request failed with status code: {response.status_code}")
            print(response.text)
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def get_ensembl_id(gene_name):
    """
    Retrieve the Ensembl ID for a given gene name using the OpenTargets API.
    
    Args:
    gene_name (str): The name of the gene (e.g., official gene symbol).
    
    Returns:
    str: The Ensembl ID if found, None otherwise.
    """
    # OpenTargets GraphQL API endpoint
    url = "https://api.platform.opentargets.org/api/v4/graphql"

    # GraphQL query
    query = """
    query GetEnsemblId($geneSymbol: String!) {
      search(queryString: $geneSymbol) {
        hits {
          id
          entity
          object {
            ... on Target {
              id
              approvedSymbol
            }
          }
        }
      }
    }
    """

    # Variables for the query
    variables = {
        "geneSymbol": gene_name
    }

    # Combine query and variables
    payload = {
        "query": query,
        "variables": variables
    }

    try:
        # Make the POST request
        response = requests.post(url, json=payload)
        
        # Check if the request was successful
        if response.status_code == 200:
            result = response.json()
            hits = result.get('data', {}).get('search', {}).get('hits', [])
            
            # Check if we got any hits
            for hit in hits:
                if hit['entity'] == 'target' and hit['object']['approvedSymbol'].upper() == gene_name.upper():
                    return hit['id']
            
            print(f"No Ensembl ID found for gene: {gene_name}")
            return None
        else:
            print(f"Request failed with status code: {response.status_code}")
            print(response.text)
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

# Function to get gene expression info from human protein atlas
def get_gene_info(gene_name, tsv_file = 'tissue_distribution/rna_tissue_consensus.tsv'):
    os.chdir(directory_set_up() + '/Report_Generation_AgentAnalyst/')

    # Read the TSV file into a DataFrame
    df = pd.read_csv(tsv_file, sep='\t')
    
    # change this to ignore the case gene_info = df[df['Gene name'] == gene_name]
    gene_info = df[df['Gene name'].str.lower() == gene_name.lower()]
    
    if gene_info.empty:
        return f"No information found for gene name: {gene_name}"
    
    # Calculate percentiles
    percentiles = gene_info["nTPM"].quantile([0.1, 0.3, 0.5, 0.7, 0.9])
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

    # Generate markdown table
    markdown_table = "| Tissue Type | Expression Value | Expression Level |\n"
    markdown_table += "|-------------|------------------|------------------|\n"
    for _, row in gene_info.iterrows():
        markdown_table += f"| {row['Tissue']} | {row['nTPM']} | {row['Expression Level']} |\n"

    return markdown_table

def load_md_file(file_path):
    with open(file_path, 'r') as f:
        md = f.read()
    return md

# use ### \d\\.+ to split a file
def split_report(file_content, file_type = 'human'):
    # get both the matched string and the rest of the string
    matched = ['Intro']
    if file_type == 'human':
        matched += re.findall(r'### \d\\.+', file_content)
    else:
        matched += re.findall(r'### \d.+', file_content)

    # clean up matched, remove signs like #., only remain characters and space and lower case 
    matched = [re.sub(r'[^a-z ]', '', m.lower()) for m in matched]

    #delete space at the beginning of each matched string
    matched = [re.sub(r'^\s+', '', m) for m in matched]

    if file_type == 'human':
        report_chunks = re.split(r'### \d\\.+', file_content)
    else:
        report_chunks = re.split(r'### \d.+', file_content)

    report_chunks = {f"{i}": chunk for i, chunk in zip(matched, report_chunks)}
    return report_chunks

def retrieve_report(gene_name, disease_name, file_type):
    gene_name = gene_name.lower().replace(' ', '')
    cwd_path = directory_set_up()
    if file_type == 'direct':
        direct_files = os.listdir(cwd_path + '/Report_Generation_AgentAnalyst/reports/' + disease_name.lower() + '/' + gene_name.lower().replace(' ', ''))
        for file in direct_files:
            if '_all.md' in file:
                return file
    elif file_type == 'review':
        review_files = os.listdir(cwd_path + '/Report_Reviewing_AgentReviewer/feedback_repo/revised_reports_complete/refine_reports/' + disease_name + '/' + gene_name.lower().replace(' ', ''))
        review_file = []
        for file in review_files:
            if gene_name.lower().replace(' ', '') in file.lower():
                review_file.append(file)
        # get the one with _all.md
        for file in review_file:
            if '_all.md' in file:
                return file

def get_report_chunk(gene_name, disease_name, file_type):
    gene_name = gene_name.lower().replace(' ', '')
    file_name = retrieve_report(gene_name, disease_name, file_type)
    print(file_name)
    cwd_path = directory_set_up()
    if file_type == 'direct':
        file_path = os.path.join(cwd_path + '/Report_Generation_AgentAnalyst/reports/' + disease_name.lower() + '/' + gene_name.lower().replace(' ', ''), file_name)
    elif file_type == 'review':
        file_path = os.path.join(cwd_path + '/Report_Reviewing_AgentReviewer/feedback_repo/summary_feedback_tmp/refine_reports/' + disease_name.lower() + '/' + gene_name.lower() + '/', file_name)
    file_content = load_md_file(file_path)
    report_chunks = split_report(file_content, file_type)
    return report_chunks

def get_drug_info(gene_name):
    # load the gene_name + _drug_info.txt file and return, it is stored in the target_drug_info folder
    file_path = os.path.join('target_drug_info', gene_name.upper() + '_drug_info.txt')
    # check both upper and lower case
    if not os.path.exists(file_path):
        file_path = os.path.join('target_drug_info', gene_name.lower() + '_drug_info.txt')
    with open(file_path, 'r') as f:
        drug_info = f.read()
    
    return drug_info

def chunk_key_match(section_name, report_chunks):
    # lower the key and delete the space for report_chunks.keys()
    report_chunks_keys = [re.sub(r'[^a-z ]', '', key.lower()) for key in report_chunks.keys()]
    report_chunks_keys = [re.sub(r' ', '', key) for key in report_chunks_keys]

    # check how many characters the section_name match with each report_chunk_keys, don't use RE
    match = [len([c for c in section_name if c in key]) for key in report_chunks_keys]
    max_match = max(match)

    # if the max_match is 0, return None, find the most matched key and return the corresponding key in report_chunks.keys()
    if max_match == 0:
        return None
    else:
        return list(report_chunks.keys())[match.index(max_match)]

def scoring(llm, report_chunk, instruction, prompt='', market_info=''):
    #choose section
    prompt_template = PromptTemplate.from_template('''
    {market_info}
    ----------------------
    {report}
    ----------------------
    {prompt}
    ''')

    # fill in the template
    prompt_template = prompt_template.format(report = report_chunk, prompt = prompt, market_info = market_info)
    agent_instruction = instruction

    messages = [SystemMessage(content = agent_instruction), HumanMessage(content = prompt_template)]

    result = ''
    # run the agent
    for chunk in llm.stream(messages):
        # print(chunk.content)
        result += chunk.content

    return result

def initialize_llm():
    return testChat()

# Define the function to process each gene
def process_gene(gene, disease_name, file_type, match_moa = False):
    llm = initialize_llm()
    return generate_final_report(llm, gene, disease_name, file_type=file_type, match_moa=match_moa)

def in_batch_generate_final_report(gene_list, disease_name, file_type, match_moa=False):
    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(process_gene, gene, disease_name, file_type, match_moa) 
                   for gene in gene_list]
        results = [future.result() for future in futures]
    return results

def generate_final_report(llm, gene_name, disease_name, file_type, match_moa=False):
    #load json file
    file_name = gene_name.lower().replace(' ', '') + '_' + disease_name.lower().replace(' ', '') + '.json'
    gene_name = gene_name.lower().replace(' ', '')
    disease_name = disease_name.lower().replace(' ', '')
    print('llm' + str(llm))
    print('gene_name' + str(gene_name))
    print('disease_name' + str(disease_name))
    print('file_type' + str(file_type))
    print('match_moa' + str(match_moa))
    # ensure cwd_path variable is under the TargetSeek folder
    cwd_path = directory_set_up()
    file_path = os.path.join(cwd_path + '/Target_Scoring_AgentScorer/scoring_result/' + file_type + '/json/' + disease_name + '/', file_name)
    #if file path not exist, create
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))
    data = load_json(file_path)

    #generate final scoring_table
    result = scoring(llm, data, generate_final_table_instruction(match_moa))

    #store the result in markdown file
    storing_path = os.path.join(cwd_path + '/Target_Scoring_AgentScorer/scoring_result/' + file_type + '/markdown/' + disease_name, gene_name.lower() + '_' + disease_name.lower() + '_scoring.md')

    #if path not exist, create
    if not os.path.exists(os.path.dirname(storing_path)):
        os.makedirs(os.path.dirname(storing_path))

    with open(storing_path, 'w') as f:
        f.write(result)

def extract_ratings(markdown_table):
    # Split the markdown table into lines
    lines = markdown_table.strip().split('\n')
    
    # Initialize a list to hold the rating scores
    ratings = []
    
    # Regex to match the rating value in the markdown table
    rating_regex = re.compile(r'[\+-]?\d+(\.\d+)?')

    # Iterate over the lines to extract ratings
    for line in lines:
        # Check if the line contains a rating
        if "|" in line:
            # Split the line into columns
            columns = line.split('|')
            if len(columns) > 3:
                # Extract the rating column and match the rating value
                rating_text = columns[3].strip()
                match = rating_regex.search(rating_text)
                if match:
                    # Convert the matched rating to float and append to the list
                    ratings.append(float(match.group()))

    return ratings

# load gene_list in the gene_name_lists folder
def load_gene_list(prefix, disease_name):
    if disease_name == 'non_small_cell_lung_cancer':
        file_path = os.path.join(prefix, 'gene_name_lists', 'nsclc_gene_list.txt')
    elif disease_name == 'rheumatoid_arthritis':
        file_path = os.path.join(prefix, 'gene_name_lists', 'ra_gene_list.txt')
    elif disease_name == 'type2_diabetes':
        file_path = os.path.join(prefix, 'gene_name_lists', 'type2_gene_list.txt')
    elif disease_name == 'inflammatory_bowel_disease':
        file_path = os.path.join(prefix, 'gene_name_lists', 'ibd_gene_list.txt')
    elif disease_name == 'atherosclerosis':
        file_path = os.path.join(prefix, 'gene_name_lists', 'atherosclerosis_gene_list.txt')
    elif disease_name == 'metabolic_dysfunction_associated_steatohepatitis_mash':
        file_path = os.path.join(prefix, 'gene_name_lists', 'mash_gene_list.txt')
    elif disease_name == 'non_alcoholic_steatohepatitis_nash':
        file_path = os.path.join(prefix, 'gene_name_lists', 'mash_gene_list.txt')
    elif disease_name == 'non_alcoholic_fatty_liver_disease_nafld':
        file_path = os.path.join(prefix, 'gene_name_lists', 'mash_gene_list.txt')
    elif disease_name == 'metabolic_dysfunction_associated_fatty_liver_disease_mafld':
        file_path = os.path.join(prefix, 'gene_name_lists', 'mash_gene_list.txt')
    with open(file_path, 'r') as f:
        gene_list = f.read().splitlines()
    return gene_list

def return_ratings(gene_name, disease_name, file_type = 'direct'):
    cwd_path = directory_set_up() + '/Target_Scoring_AgentScorer'
    # Load the markdown file
    file_path = f'{cwd_path}/scoring_result/{file_type}/markdown/{disease_name.lower()}/{gene_name.lower()}_{disease_name.lower()}_scoring.md'
    markdown_table = load_md_file(file_path)
    
    # Extract the ratings from the markdown table
    ratings = extract_ratings(markdown_table)
    
    return ratings

rating_section_dict = {
    'genetic_association': 0,
    'differential_expression': 1,
    'moa': 2,
    'in_vitro_vivo': 3,
    'small_molecule': 4,
    'antibody': 5,
    'sirna': 6,
    'competitiveness': 7,
    'assayability': 8,
    'target_safety': 9,
    'moa_match': 10
}

# filtering based on criteria, safety > 0, [antibody, sirna, small_molecule] at least 1 > 0, differntial expression >= 0
# return the gene_name as a list, the input is a dictionary, key: gene_name, value: a list of ratings
def general_filtering(ratings):
    # Initialize an empty list to store the gene names
    gene_names = []
    
    # Iterate over the dictionary items
    for gene_name, values in ratings.items():
        # Check if the safety rating is greater than 0
        if ratings[gene_name]['CI_Genetic Association'] > 0:
            # Check if at least one of the ratings for antibody, siRNA, or small molecule is greater than 0
            if any(ratings[gene_name][key] > 0 for key in ['T_Antibody', 'T_siRNA', 'T_Small molecules']):
                # Check if the differential expression rating is greater than or equal to 0
                if ratings[gene_name]['CI_Differential expression'] >= 0:
                    gene_names.append(gene_name)
                else:
                    print(f"Discarding {gene_name}: Differential expression rating is less than 0")
            else:
                print(f"Discarding {gene_name}: No suitable modalities")
        
        # explain why a gene is discarded
        else:
            print(f"Discarding {gene_name}: Safety rating is not greater than 0")
    
    return gene_names

def customized_filtering(section_name, ratings, gene_names, threshold):
    # Initialize an empty list to store the gene names
    filtered_gene_names = []
    
    # Iterate over the gene names
    for gene_name in gene_names:
        # Get the rating for the specified section
        rating = ratings[gene_name][section_name]
        
        # Check if the rating is above the threshold
        if rating > threshold:
            filtered_gene_names.append(gene_name)
    
    return filtered_gene_names

def get_highest_score(ratings_of_genes, gene_list):
    for gene in gene_list:
        # Get the ratings for small molecule, antibody, and siRNA
        small_molecule = ratings_of_genes[gene][rating_section_dict['small_molecule']]
        antibody = ratings_of_genes[gene][rating_section_dict['antibody']]
        sirna = ratings_of_genes[gene][rating_section_dict['sirna']]
        
        # Create a dictionary to hold the ratings
        ratings = {
            'small_molecule': small_molecule,
            'antibody': antibody,
            'sirna': sirna
        }
        
        # Find the maximum rating
        max_rating = max(ratings.values())
        
        # Find the first key with the maximum rating
        for key in ratings:
            if ratings[key] == max_rating:
                highest_key = key
                break
        
        # Zero out all other ratings
        for key in ratings:
            if key != highest_key:
                ratings_of_genes[gene][rating_section_dict[key]] = 0
    
    return ratings_of_genes



if __name__ == "__main__":
    file_path = 'scoring_result/tern/markdown/angptl3_atheroscelrosis_scoring.md'
    markdown_table = load_md_file(file_path)
    ratings = extract_ratings(markdown_table)

