# TargetSeek: Multi-agent LLMs Simulation of Drug Target Discovery

TargetSeek is a LLM-based multi-agent system designed for drug target discovery and evaluation.
It can do three things:

1. Generate detailed **analysis reports** for specific genes in relation to a disease.

2. Generate **scoring reports** based on the analysis reports for specific genes in relation to a disease.

3. **Rank target genes** for a specific disease based on the scoring results.

## Setup Instructions

### 1. Environment Setup

#### Prerequisites
- Python 3.8 or higher
- Jupyter Notebook
- pip or conda for package management


#### Creating a Virtual Environment (Recommended)
It's recommended to create a virtual environment to avoid conflicts with other projects:
```bash
python -m venv targetseek_env
```

```bash
source targetseek_env/bin/activate
```

#### Installing Required Packages
The project requires several Python packages. You can install them using pip:
```bash
pip install -r requirements.txt
```

If you prefer to install packages manually, the main dependencies include:
- langchain
- langchain-openai
- langchain-community
- pandas
- requests
- numpy
- scikit-learn
- tqdm
- chembl_webresource_client
- jupyter

The entire setup process should only take a few minutes to complete.

### 2. API Key Configuration

Before running any notebooks, you need to configure your API keys:

1. Get your API keys:
   - OpenAI API key (OPENAI_API_KEY) from: https://platform.openai.com/account/api-keys
   - Tutorial to get Google Custom Search Engine ID (GOOGLE_CSE_ID) from: https://developers.google.com/custom-search/docs/tutorial/creatingcse
   - Tutorial to get Google Search API key (GOOGLE_API_KEY) from: https://developers.google.com/custom-search/v1/overview

2. Open `config.py` and replace the placeholder values with your actual API keys:
   ```python
   os.environ["OPENAI_API_KEY"] = "your-openai-api-key-here"
   os.environ["GOOGLE_CSE_ID"] = "your-google-cse-id-here"
   os.environ["GOOGLE_API_KEY"] = "your-google-api-key-here"
   ```

## Cost Considerations

Running (Report Generation + Report Reviewing + Report Scoring) for one candidate gene through the TargetSeek pipeline costs approximately $1 in API usage fees (primarily OpenAI API costs). Please be mindful of this when experimenting with the system, especially when processing multiple genes or diseases.

## Using the Jupyter Notebooks

TargetSeek's workflow consists of three main steps, each represented by a Jupyter notebook:

### 1. Report Generation (1. Report_Generation_WithReview.ipynb)

This notebook generates detailed reports for specific genes in relation to a disease.

#### How to use:
1. Open the notebook in Jupyter.
2. Ensure your API keys are configured in `config.py`.
3. Set the disease name and gene list:
   ```python
   # Set the disease name
   disease_name = 'atherosclerosis'
   
   # Set the gene list (provide gene codes)
   gene_list = ['PCSK9']
   ```
   - For predefined diseases (atherosclerosis, non_small_cell_lung_cancer, rheumatoid_arthritis, type2_diabetes, inflammatory_bowel_disease), you can use the provided gene lists.
   - Alternatively, specify your own genes of interest.
4. Run the notebook cells sequentially.
5. Generated reports will be saved at:
   `Report_Generation_AgentAnalyst/reports/{disease_name}/{gene_name}/report_{gene_name}_all.md`

#### Optional: Review reports
The notebook includes an optional review stage that can improve report quality:
- Run the review cells to activate an AI reviewer
- The reviewer will identify potential issues and enhance the report content

### 2. Report Scoring (2. Report_Scoring.ipynb)

This notebook evaluates and scores the target genes based on their generated reports.

#### How to use:
1. Open the notebook after generating reports with the first notebook.
2. Ensure the disease name and gene list match what you used in the first notebook.
3. Run the notebook cells sequentially to score the genes based on 13 criteria across 4 categories:
   - Causal Inference (Genetic Evidence, Differential Expression, Mechanism of Action, In Vitro/In Vivo Experiments)
   - Tractability (Small Molecule, Antibody, siRNA)
   - Competitiveness (Small Molecule, Antibody/siRNA, Unmet Medical Needs)
   - Doability (Experimental Model Availability, Biomarker Availability, Safety)
4. The generated scoring results will be saved at:
   `Target_Scoring_AgentScorer/scoring_results/direct/markdown/{disease_name}/{gene_name}_{disease_name}_scoring.md`

### 3. Target Ranking (3. Target_Ranking.ipynb)

This notebook ranks and evaluates target genes across different diseases.

#### How to use:
1. Open the notebook after scoring genes with the second notebook.
2. Run the notebook to:
   - Load disease datasets and TargetSeek scoring results
   - Train and evaluate ranking models
   - Obtain ranking results for various indications
   - Calculate performance metrics (Recall@20, Precision@20, ROC-AUC)
3. The notebook will display various evaluation metrics and visualizations to help understand the ranking results.

## Output Files

The main outputs from running the notebooks are:
- Detailed gene reports in Markdown format
- Detailed scoring results in Markdown format
- Target ranking results and evaluation metrics

## License

This project is licensed under the Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0).
For more details, see the [Creative Commons Attribution-NonCommercial 4.0 International License](https://creativecommons.org/licenses/by-nc/4.0/).
