import sagemaker
import pandas as pd
import boto3
from sklearn.model_selection import train_test_split

session = sagemaker.Session()
bucket = 'telecom-customer-churn-v2'

# 1. Charger les données Parquet propres générées par ton Glue Job
df = pd.read_parquet(f"s3://{bucket}/processud/")

# 2. Encodage : Transformer les variables textes (sexe, type_abonnement...) en chiffres (0/1)
df_encoded = pd.get_dummies(df, drop_first=True)

# 3. Réorganisation : Placer 'target' en PREMIÈRE colonne
cols = ['target'] + [col for col in df_encoded.columns if col != 'target']
df_encoded = df_encoded[cols]

# 4. Séparation : 80% pour l'entraînement, 20% pour la validation
train_df, val_df = train_test_split(df_encoded, test_size=0.2, random_state=3031)

# 5. Sauvegarde locale temporaire en CSV sans en-tête (No Header)
train_df.to_csv('train.csv', header=False, index=False)
val_df.to_csv('validation.csv', header=False, index=False)

# 6. Envoi des fichiers sur S3 pour SageMaker
s3_train_path = session.upload_data(path='train.csv', bucket=bucket, key_prefix='sagemaker/train')
s3_val_path = session.upload_data(path='validation.csv', bucket=bucket, key_prefix='sagemaker/validation')

print(f"Fichier d'entraînement prêt sur S3 : {s3_train_path}")


from sagemaker.estimator import Estimator
from sagemaker.inputs import TrainingInput

# 1. Récupérer l'image Docker XGBoost officielle d'AWS
container = sagemaker.image_uris.retrieve("xgboost", session.boto_region_name, "1.5-1")

# 2. Configurer le cluster d'entraînement éphémère
xgb_model = Estimator(
    container,
    role=sagemaker.get_execution_role(),
    instance_count=1,
    instance_type='ml.m5.xlarge',
    output_path=f"s3://{bucket}/sagemaker/output",
    sagemaker_session=session
)

# 3. Paramétrer les hyperparamètres du modèle
xgb_model.set_hyperparameters(
    max_depth=5,
    eta=0.2,
    gamma=4,
    min_child_weight=6,
    subsample=0.8,
    objective='binary:logistic',
    num_round=100
)

# 4. Spécifier les entrées S3
train_input = TrainingInput(s3_train_path, content_type='text/csv')
val_input = TrainingInput(s3_val_path, content_type='text/csv')

# 5. Lancer l'entraînement !
xgb_model.fit({'train': train_input, 'validation': val_input})