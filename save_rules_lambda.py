import json
import boto3
from algoliasearch.search_client import SearchClient
from datetime import datetime,date
import os

BUCKET_NAME = "algolia-backup"
s3_client = boto3.client("s3")
client = SearchClient.create('BC4SA39FG5', '93423bf7ae47361625ee676735d541e2')APP_ID = os.environ["APP_ID"]
API_KEY = os.environ["API_KEY"]
client = SearchClient.create(APP_ID,API_KEY )

def upload_index_s3(index_name, rules, date):   
    print("Uploadinf new json")
    # Upload new json with availability data
    output_key = f"{date}/{index_name}/{index_name}-rules.json" 
    uploadByteStream = bytes(json.dumps(rules).encode('utf-8'))
    s3_client.put_object(Bucket=BUCKET_NAME, Key=output_key, Body=uploadByteStream)
    
def get_rules(index_name):
    result = {}
    rules = []
    index_object = client.init_index(index_name)
    for rule in index_object.browse_rules():
        rules.append(rule)
    if len(rules) > 0:
        result["rules"] = rules
    else:
        return None
    return result
    
def lambda_handler(event, context):
    # TODO implement
    indices = client.list_indices()["items"]
    indices_names = [ index["name"] for index in indices]
    
    today = date.today()
    today_str = today.strftime("%Y-%m-%d")
    
    for index_name in indices_names:
        rules = get_rules(index_name)
        print("--> " + index_name)
        if rules:
            print(" -- Uploading rules")
            upload_index_s3(index_name,rules,today_str)  
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
