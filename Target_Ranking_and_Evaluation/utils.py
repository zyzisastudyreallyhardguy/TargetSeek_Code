import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from sklearn.impute import SimpleImputer
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LogisticRegression
import os

def load_data(disease_path, geneseek_path):
    if disease_path.endswith('.csv') and disease_path != '':
        athero_dataset = pd.read_csv(disease_path)
    elif disease_path != '':
        # include columns
        athero_dataset = pd.read_excel(disease_path)
    else:
        athero_dataset = pd.DataFrame()
    geneseek = pd.read_csv(geneseek_path, on_bad_lines='skip')
    geneseek.columns = ['CI_Genetic Association', 'CI_Differential expression', 'CI_Mechanism of Action', 'CI_In vitro_in vivo experiment', 'T_Small molecules', 'T_Antibody', 'T_siRNA', 'CP_Competitiveness_Small_Molecules','CP_Competitiveness_Antibody_or_siRNA' ,'CP_Unmet Needs' ,'DO_experimental_model_availability', 'DO_biomarkers', 'DO_Safety', 'NAN']
    if geneseek_path == 'GeneSeek_MASH_Results.csv':
        # all columns go left one column, e.g., original values for the second column should be the values for the first column, and so on. Original first column becomes a new column named 'Gene'.
        # geneseek.columns = ['Gene'] + list(geneseek.columns[:-1])
        # # set Gene as the index
        # geneseek.set_index('Gene', inplace=True)
        pass
    return athero_dataset, geneseek

def get_paths(disease_name):
    if disease_name == 'atherosclerosis':
        disease_path = 'datasets/TargetSeek_Atherosclerosis_dataset.xlsx'
        geneseek_path = 'results/TargetSeek_Atherosclerosis_Results.csv'
    elif disease_name == 'ibd':
        disease_path = 'datasets/TargetSeek_IBD_dataset.csv'
        geneseek_path = 'results/TargetSeek_IBD_Results.csv'
    elif disease_name == 'type2_diabetes':
        disease_path = 'datasets/TargetSeek_type2_diabetes_dataset.csv'
        geneseek_path = 'results/TargetSeek_type2_diabetes_Results.csv'
    elif disease_name == 'rheumatoid_arthritis':
        disease_path = 'datasets/TargetSeek_RA_dataset.csv'
        geneseek_path = 'results/TargetSeek_RA_Results.csv'
    elif disease_name == 'non_small_cell_lung_cancer':
        disease_path = 'datasets/TargetSeek_NSCLC_dataset.csv'
        geneseek_path = 'results/TargetSeek_NSCLC_Results.csv'
    elif disease_name == 'metabolic_dysfunction_associated_steatohepatitis_mash':
        disease_path = ''
        geneseek_path = 'results/TargetSeek_MASH_Results.csv'
    return disease_path, geneseek_path

def process_diseases(diseases=None):
    if diseases is None:
        diseases = ['atherosclerosis', 'ibd', 'type2_diabetes', 'rheumatoid_arthritis', 
                   'non_small_cell_lung_cancer', 'metabolic_dysfunction_associated_steatohepatitis_mash']
    all_data = []

    for disease in diseases:
        print(f"Processing {disease}...")
        disease_path, geneseek_path = get_paths(disease)
        
        disease_dataset, geneseek = load_data(disease_path, geneseek_path)
        
        geneseek.index = geneseek.index.str.lower().str.replace(' ', '')
        if disease != 'metabolic_dysfunction_associated_steatohepatitis_mash':
            disease_dataset.set_index('symbol', inplace=True)
            disease_dataset.index = disease_dataset.index.str.lower().str.replace(' ', '')

            # add the column of ['DiseaseSpecific_ClinicLabel'] of disease_dataset to the geneseek, need to match the index
            # Ensure gene names are consistent by using the normalized index
            common_genes = geneseek.index.intersection(disease_dataset.index)
            # Check for duplicate indices and handle them
            if not geneseek.index.is_unique:
                geneseek = geneseek.groupby(level=0).first()  # Keep the first occurrence of each duplicate index
            if not disease_dataset.index.is_unique:
                disease_dataset = disease_dataset.groupby(level=0).first()  # Keep the first occurrence of each duplicate index
            
            # Now proceed with the assignment using the normalized indices
            geneseek.loc[common_genes, 'DiseaseSpecific_ClinicLabel'] = disease_dataset.loc[common_genes, 'DiseaseSpecific_ClinicLabel']

        # add one more column to geneseek, indicating the disease name
        geneseek['Disease'] = disease
        
        all_data.append(geneseek)
    
    all_data = pd.concat(all_data)
    
    return all_data


def print_na_values_by_disease(all_data):
    # Filter for IBD genes with NA values in the 'CI_Genetic Association' column
    ibd_na_values = all_data[(all_data['Disease'] == 'ibd') & (all_data['CI_Genetic Association'].isna())]

    print("IBD genes with NA values in 'CI_Genetic Association':")
    for idx, row in ibd_na_values.iterrows():
        print(f"{idx}: Value - {row['CI_Genetic Association']}")

    print(f"\nNumber of IBD genes with NA values: {len(ibd_na_values)}")

    # For other diseases
    for disease in ['atherosclerosis', 'type2_diabetes', 'rheumatoid_arthritis', 'non_small_cell_lung_cancer', 'metabolic_dysfunction_associated_steatohepatitis_mash']:
        disease_na_values = all_data[(all_data['Disease'] == disease) & (all_data['CI_Genetic Association'].isna())]
        
        print(f"\n{disease.capitalize()} genes with NA values in 'CI_Genetic Association':")
        for idx, row in disease_na_values.iterrows():
            print(f"{idx}: Value - {row['CI_Genetic Association']}")
        
        print(f"\nNumber of {disease} genes with NA values: {len(disease_na_values)}")

# write a function to obtain the maximum value of T_Small molecules, T_Antibody, T_siRNA, and make it a new column in the dataframe called 'T_max'
def get_T_max(data):
    data['T_max'] = data[['T_Small molecules', 'T_Antibody', 'T_siRNA']].max(axis=1)
    return data

def train_model(X_train_scaled, y_train, model_type='logistic_regression'):
    """Train a logistic regression model"""
    if model_type == 'logistic_regression':
        model = LogisticRegression(random_state=np.random.randint(0, 10000))
    elif model_type == 'hist_gradient_boosting':
        model = HistGradientBoostingClassifier(random_state=np.random.randint(0, 10000))
    elif model_type == 'random_forest':
        model = RandomForestClassifier(random_state=np.random.randint(0, 10000), min_samples_leaf=2)
    model.fit(X_train_scaled, y_train)
    return model

def preprocess_data(train_data, test_data):
    """Preprocess training and test data by scaling and imputing"""
    # Select features (all columns except excluded ones) to avoid information leakage
    excluded_columns = ['NAN', 'Disease', 'DiseaseSpecific_ClinicLabel', 
                       'CP_Competitiveness_Small_Molecules', 
                       'CP_Competitiveness_Antibody_or_siRNA', 
                       'CP_Unmet Needs']

    feature_columns = [col for col in train_data.columns if col not in excluded_columns]
    X_train = train_data[feature_columns]
    y_train = (train_data['DiseaseSpecific_ClinicLabel'] > 0).astype(int)
    X_test = test_data[feature_columns]
    y_test = (test_data['DiseaseSpecific_ClinicLabel'] > 0).astype(int)

    # Scale features and impute missing values
    scaler = StandardScaler()
    imputer = SimpleImputer(strategy='mean')
    
    X_train_scaled = pd.DataFrame(
        scaler.fit_transform(imputer.fit_transform(X_train)), 
        columns=X_train.columns
    )
    X_test_scaled = pd.DataFrame(
        scaler.transform(imputer.transform(X_test)), 
        columns=X_test.columns
    )
    
    return X_train_scaled, X_test_scaled, y_train, y_test

def calculate_metrics(y_test, y_pred, y_pred_proba):
    """Calculate model performance metrics"""
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='binary')
    recall = recall_score(y_test, y_pred, average='binary') 
    f1 = f1_score(y_test, y_pred, average='binary')
    roc_auc = roc_auc_score(y_test, y_pred_proba)
    
    return accuracy, precision, recall, f1, roc_auc

def get_feature_importance(model, X_test_scaled, y_test):
    """Calculate feature importance scores"""
    perm_importance = permutation_importance(
        model, X_test_scaled, y_test, 
        n_repeats=10, 
        random_state=np.random.randint(0, 10000)
    )
    feature_importance = pd.DataFrame({
        'feature': X_test_scaled.columns,
        'importance': perm_importance.importances_mean
    }).sort_values('importance', ascending=False)
    
    return feature_importance

def get_rankings(test_data, y_pred_proba):
    """Get rankings for all samples"""
    test_data_with_proba = test_data.copy()
    test_data_with_proba['predicted_proba'] = y_pred_proba.round(2)
    test_data_with_proba['rank'] = test_data_with_proba['predicted_proba'].rank(
        ascending=False, method='min'
    )

    # Sort samples by predicted probability
    all_samples_ranked = test_data_with_proba.sort_values('predicted_proba', ascending=False)
    positive_samples_ranked = all_samples_ranked[all_samples_ranked['DiseaseSpecific_ClinicLabel'] > 0]
    
    return positive_samples_ranked, all_samples_ranked

def calculate_ranking_metrics(positive_samples_ranked, all_samples_ranked):
    """Calculate ranking-based metrics"""
    avg_ranking = positive_samples_ranked['rank'].mean()
    
    # Calculate recall@10 and precision@10
    top_10 = all_samples_ranked.head(10)
    true_positives_10 = top_10[top_10['DiseaseSpecific_ClinicLabel'] > 0]
    recall_at_10 = len(true_positives_10) / len(positive_samples_ranked)
    precision_at_10 = len(true_positives_10) / 10
    
    return avg_ranking, recall_at_10, precision_at_10

def train_and_evaluate(train_data, test_data, test_disease, model_type='logistic_regression', show_rank=False, save_ranked_results=False):
    """Main function to train model and evaluate performance"""
    # Preprocess data
    X_train_scaled, X_test_scaled, y_train, y_test = preprocess_data(train_data, test_data)
    
    # Train model
    model = train_model(X_train_scaled, y_train, model_type)
    
    # Make predictions
    y_pred = model.predict(X_test_scaled)
    y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]
    
    # Calculate metrics
    accuracy, precision, recall, f1, roc_auc = calculate_metrics(y_test, y_pred, y_pred_proba)
    
    # Get feature importance
    feature_importance = get_feature_importance(model, X_test_scaled, y_test)
    
    # Get rankings
    positive_samples_ranked, all_samples_ranked = get_rankings(test_data, y_pred_proba)
    
    if show_rank:
        print(f"\nPositive samples predictions for {test_disease}:")
        print(positive_samples_ranked[['predicted_proba', 'rank']].to_string())
    
    # Calculate ranking metrics
    avg_ranking, recall_at_10, precision_at_10 = calculate_ranking_metrics(
        positive_samples_ranked, all_samples_ranked
    )
    
    # Save ranked results if requested
    if save_ranked_results:
        save_ranked_samples(all_samples_ranked, test_disease)
        print(f"Saved ranked results for {test_disease}")
    
    return (accuracy, precision, recall, f1, roc_auc, positive_samples_ranked, 
            all_samples_ranked, avg_ranking, feature_importance, recall_at_10, precision_at_10)

def calculate_recall_precision(samples_ranking):
    # samples_ranking is a list of 20 ranks for positive samples
    total_positives = 20
    # Count how many ranks are <= 20 (i.e. in top 20)
    top_20_positives = sum(1 for rank in samples_ranking if rank <= 20)
    recall_20 = top_20_positives / total_positives
    precision_20 = top_20_positives / 20
    
    # For ROC AUC, need to create binary labels and scores
    # Create array of 100 zeros (total samples from context)
    y_true = np.zeros(100)
    # Set 1s at the rank positions
    for rank in samples_ranking:
        y_true[rank-1] = 1
    # Create scores array - higher score for lower rank
    scores = np.array([(100-i) for i in range(100)])
    roc_auc = roc_auc_score(y_true, scores)
    
    return recall_20, precision_20, roc_auc

def train_model_only(train_data, model='RandomForest', show_feature_importance=False):
    # Select features (all columns except 'NAN', 'Disease', 'DiseaseSpecific_ClinicLabel', and the three excluded columns)
    excluded_columns = ['NAN', 'Disease', 'DiseaseSpecific_ClinicLabel', 'CP_Competitiveness_Small_Molecules', 'CP_Competitiveness_Antibody_or_siRNA', 'CP_Unmet Needs', 'T_Small molecules', 'T_Antibody', 'T_siRNA']
    feature_columns = [col for col in train_data.columns if col not in excluded_columns]
    X_train = train_data[feature_columns]
    y_train = (train_data['DiseaseSpecific_ClinicLabel'] > 0).astype(int)

    # Scale the features and impute missing values
    scaler = StandardScaler()
    imputer = SimpleImputer(strategy='mean')
    
    X_train_scaled = pd.DataFrame(scaler.fit_transform(imputer.fit_transform(X_train)), columns=X_train.columns)

    # #print shape of X_trained_scaled
    # print(X_train_scaled.shape)
    # print(X_train.shape)

    if model == 'random_forest':
        model = RandomForestClassifier(random_state=np.random.randint(0, 10000), min_samples_leaf=2)
    elif model == 'hist_gradient_boosting':
        model = HistGradientBoostingClassifier(random_state=np.random.randint(0, 10000))
    elif model == 'logistic_regression':
        model = LogisticRegression(random_state=np.random.randint(0, 10000))
    model.fit(X_train_scaled, y_train)
    
    # Only calculate feature importance for RandomForest
    if isinstance(model, RandomForestClassifier):
        # Get feature importance scores and correlations
        feature_importance = pd.DataFrame({
            'Feature': feature_columns,
            'Importance': model.feature_importances_
        })
        feature_importance = feature_importance.sort_values('Importance', ascending=False)
        
        # Calculate correlations with target
        correlations = []
        for feature in feature_columns:
            corr = np.corrcoef(X_train_scaled[feature], y_train)[0,1]
            correlations.append(corr)
        
        feature_importance['Correlation'] = correlations
        feature_importance['Correlation_Direction'] = ['Positive' if c > 0 else 'Negative' for c in correlations]
        if show_feature_importance:
            print("\nFeature Importance:")
            print(feature_importance)
    
    return model, scaler, imputer, feature_columns

def save_ranked_samples(ranked_samples, disease_name):
    # how to go back to the parent directory
    work_path = os.path.expanduser('~/TargetSeek')

    # save_path
    save_path = os.path.join(work_path, 'Ranked_Results', f'{disease_name}_ranked_samples.csv')

    ranked_samples.to_csv(save_path, index=True)

def predict_new_disease(model, scaler, imputer, feature_columns, mash_data, save_samples=True):
    X_test = mash_data[feature_columns]
    X_test_scaled = pd.DataFrame(scaler.transform(imputer.transform(X_test)), columns=X_test.columns)
    
    y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]
    
    # Add predictions and rankings
    mash_data_with_proba = mash_data.copy()
    mash_data_with_proba['predicted_proba'] = y_pred_proba.round(2)
    mash_data_with_proba['rank'] = mash_data_with_proba['predicted_proba'].rank(ascending=False, method='min')
    
    # Sort by predicted probability
    ranked_samples = mash_data_with_proba.sort_values('predicted_proba', ascending=False)

    # get the disease name
    disease_name = mash_data['Disease'].iloc[0]

    # Save the ranked samples if requested
    if save_samples:
        save_ranked_samples(ranked_samples, disease_name)

    return ranked_samples
