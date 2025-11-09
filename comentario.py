import boto3
import uuid
import os

def lambda_handler(event, context):
    # Entrada (json)
    tenant_id = event['body']['tenant_id']
    texto = event['body']['texto']
    nombre_tabla = os.environ["TABLE_NAME"]
    nombre_bucket = os.environ["BUCKET_NAME"]
    # Proceso
    uuidv1 = str(uuid.uuid1())
    comentario = {
        'tenant_id': tenant_id,
        'uuid': uuidv1,
        'detalle': {
          'texto': texto
        }
    }
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(nombre_tabla)
    response = table.put_item(Item=comentario)

    s3 = boto3.client('s3')
    s3.put_object(
        Bucket = nombre_bucket,
        Key=f"{tenant_id}/{uuidv1}.json",
        Body=str(comentario)
    )
    # Salida (json)
    return {
        'statusCode': 200,
        'comentario': comentario,
        'response': response
    }
