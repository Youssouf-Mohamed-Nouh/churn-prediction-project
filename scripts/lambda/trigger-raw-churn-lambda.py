import boto3

glue = boto3.client('glue')

def lambda_handler(event, context):
    try:
        # Étape 1 : On lance UNIQUEMENT le crawler
        print("S3 a détecté un fichier. Démarrage du crawler...")
        glue.start_crawler(Name='crawler-churn-raw')
        
        return {
            'statusCode': 200,
            'body': 'Crawler démarré avec succès.'
        }
    except Exception as e:
        print(f"Erreur au démarrage du crawler : {str(e)}")
        raise e