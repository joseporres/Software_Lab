import boto3
import redis
import json

def lambda_handler(event, context):

    # Configura el cliente Redis para tu clúster ElastiCache
    elasticache_endpoint = 'pokemoncache.qos1uw.clustercfg.use1.cache.amazonaws.com'
    elasticache_port = 6379  # Puerto predeterminado de Redis
    elasticache_client = redis.StrictRedis(host=elasticache_endpoint, port=elasticache_port, decode_responses=True)

    # Insertar un valor (key-value) en la caché
    key = 'mi_key'
    value = 'mi_valor'
    elasticache_client.set(key, value)


    return {
        "statusCode": 200,
        "body": json.dumps("Pokémon data retrieval and storage complete.")
    }
