import sys
import boto3
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
# 1. DÉTECTION AUTOMATIQUE DE LA TABLE (Data Catalog)
# ===================================================================
glue_client = boto3.client('glue', region_name='us-east-1')
tables = glue_client.get_tables(DatabaseName='churndata')
table_name = tables['TableList'][0]['Name']

datasource = glueContext.create_dynamic_frame.from_catalog(
    database='churndata',
    table_name=table_name
)
df = datasource.toDF()
print("Nombre de lignes initial :", df.count())

# ===================================================================
# 1.2 RENOMMAGE DES COLONNES
# ===================================================================
df = df.withColumnRenamed('CustomerID', 'Identifiant_Unique') \
       .withColumnRenamed('Gender', 'Sexe') \
       .withColumnRenamed('Tenure', 'Anciennete') \
       .withColumnRenamed('Usage Frequency', 'Utilisation_Service') \
       .withColumnRenamed('Support Calls', 'Nombre_Appel') \
       .withColumnRenamed('Payment Delay', 'Delai_Paiement') \
       .withColumnRenamed('Subscription Type', 'Type_Abonnement') \
       .withColumnRenamed('Contract Length', 'Duree_Contact') \
       .withColumnRenamed('Total Spend', 'Montant_Total') \
       .withColumnRenamed('Last Interaction', 'Derniere_Interaction') \
       .withColumnRenamed('Churn', 'Target')

# ===================================================================
# 2. TRAITEMENT DES VALEURS MANQUANTES
# ===================================================================
valeurs_vides = ['', ' ', '?', 'NA', 'na', 'N/A', 'n/a', 'none', '.', 'None']
for col_name, data_type in df.dtypes:
    if data_type == 'string':
        df = df.withColumn(col_name,
            F.when(F.col(col_name).isin(valeurs_vides), F.lit(None))
             .otherwise(F.col(col_name)))

# Colonne inutile + suppression des lignes avec NaN
df = df.drop('Identifiant_Unique')
df = df.dropna()
print("Après nettoyage :", df.count())

# ===================================================================
# 3. ÉCHANTILLONNAGE (6000 Target=1 / 4000 Target=0, seed=3031)
# ===================================================================
df_oui = df.filter(F.col('Target') == 1).orderBy(F.rand(3031)).limit(6000)
df_non = df.filter(F.col('Target') == 0).orderBy(F.rand(3031)).limit(6000)
df = df_oui.union(df_non)
print("Après échantillonnage :", df.count())

# ===================================================================
# 4. RECODAGE DES VARIABLES
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
# 7. SORTIE
# ===================================================================
df.write.mode('overwrite').parquet('s3://telecom-customer-churn-v2/processud/')
job.commit()