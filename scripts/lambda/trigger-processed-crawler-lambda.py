import json

def lambda_handler(event, context):
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
import boto3

glue = boto3.client('glue')

def lambda_handler(event, context):
    crawler_name = 'crawler-churn-processud'
    
    try:
        print(f"Le Job Glue est fini. Démarrage automatique du crawler : {crawler_name}")
        glue.start_crawler(Name=crawler_name)
        
        return {
            'statusCode': 200,
            'body': f"Crawler {crawler_name} lancé avec succès."
        }
    except Exception as e:
        print(f"Erreur au lancement du crawler final : {str(e)}")
        raise e