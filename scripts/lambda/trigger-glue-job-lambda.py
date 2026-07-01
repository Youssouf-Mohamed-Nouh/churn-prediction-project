import boto3
import os
glue = boto3.client('glue')
job_name = os.environ['JOB_NAME']
def lambda_handler(event, context):
    try:
        # Étape 2 : Le crawler est prêt, on lance le Job de nettoyage
        print("EventBridge a détecté que le crawler est READY. Lancement du Job Glue...")
        response = glue.start_job_run(JobName=job_name)
        
        return {
            'statusCode': 200,
            'body': f"Job Glue démarré avec succès. RunId: {response['JobRunId']}"
        }
    except Exception as e:
        print(f"Erreur au démarrage du Job Glue : {str(e)}")
        raise e