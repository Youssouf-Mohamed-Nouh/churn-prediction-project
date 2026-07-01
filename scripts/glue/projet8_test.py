import sys
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql import functions as F

# INIT
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# ===================================================================
# 1. LECTURE DU FICHIER DE TEST DEPUIS S3
# ===================================================================
df = spark.read.option('header', True).option('inferSchema', True) \
    .csv('s3://telecom-customer-churn-v2/raw/classeur1.csv')
print("Nombre de lignes test :", df.count())
print("Colonnes test :", df.columns)

# ===================================================================
# 2. RENOMMAGE DES COLONNES (mêmes noms que le pipeline d'entraînement)
# ===================================================================
renommages = {
    'Gender': 'Sexe',
    'Tenure': 'Anciennete',
    'Usage Frequency': 'Utilisation_Service',
    'Support Calls': 'Nombre_Appel',
    'Payment Delay': 'Delai_Paiement',
    'Subscription Type': 'Type_Abonnement',
    'Contract Length': 'Duree_Contact',
    'Total Spend': 'Montant_Total',
    'Last Interaction': 'Derniere_Interaction',
    'Churn': 'Target'
}
for old_col, new_col in renommages.items():
    if old_col in df.columns:
        df = df.withColumnRenamed(old_col, new_col)

# ===================================================================
# 3. NETTOYAGE (identique au pipeline d'entraînement)
# ===================================================================
valeurs_vides = ['', ' ', '?', 'NA', 'na', 'N/A', 'n/a', 'none', '.', 'None']
for col_name, data_type in df.dtypes:
    if data_type == 'string':
        df = df.withColumn(col_name,
            F.when(F.col(col_name).isin(valeurs_vides), F.lit(None))
             .otherwise(F.col(col_name)))

df = df.dropna()
print("Après nettoyage test :", df.count())

# ===================================================================
# 4. RECODAGE (identique au pipeline d'entraînement)
# ===================================================================
df = df.withColumn('Sexe',
    F.when(F.col('Sexe') == 'Male', 'Homme')
     .when(F.col('Sexe') == 'Female', 'Femme')
     .otherwise(F.col('Sexe'))
).withColumn('Type_Abonnement',
    F.when(F.col('Type_Abonnement') == 'Basic', 'Basique')
     .otherwise(F.col('Type_Abonnement'))
).withColumn('Duree_Contact',
    F.when(F.col('Duree_Contact') == 'Annual', 'Annuel')
     .when(F.col('Duree_Contact') == 'Monthly', 'Mensuel')
     .when(F.col('Duree_Contact') == 'Quarterly', 'Trimestriel')
     .otherwise(F.col('Duree_Contact')))

# ===================================================================
# 5. SORTIE → données propres prêtes pour SageMaker Batch Transform
# ===================================================================
df.write.mode('overwrite').parquet('s3://telecom-customer-churn-v2/predictions/')
job.commit()
