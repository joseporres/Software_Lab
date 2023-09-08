import os
import csv
import json
import requests
# import redis
import boto3

api_base_url = "https://pokeapi.co/api/v2/pokemon/"

# redis_endpoint = 'pokemoncache.qos1uw.clustercfg.use1.cache.amazonaws.com'
# redis_port = 6379  # Default Redis port

# redis_client = redis.StrictRedis(host=redis_endpoint, port=redis_port, decode_responses=True)

s3 = boto3.client('s3')

def lambda_handler(event, context):
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_name = event['Records'][0]['s3']['object']['key']
    
    csv_file_path = '/tmp/' + file_name
    s3.download_file(bucket_name, file_name, csv_file_path)

    with open(csv_file_path, "r", newline="") as csvfile:
        csv_reader = csv.DictReader(csvfile)
        
        for row in csv_reader:
            pokemon_name = row["pokemon"]

            pokemon_url = api_base_url + pokemon_name.lower()

            response = requests.get(pokemon_url)

            if response.status_code == 200:
                pokemon_data = response.json()['abilities']
                # redis_key = f"pokemon:{pokemon_name}"
                # redis_client.set(redis_key, json.dumps(pokemon_data))
                stringData = json.dumps(pokemon_data)
                print("Retrieved data of " + pokemon_name + " from API:" + stringData)
            else:
                print(f"Failed to retrieve data for {pokemon_name}")
    
    os.remove(csv_file_path)

    return {
        "statusCode": 200,
        "body": json.dumps("Pokémon data retrieval.")
    }
