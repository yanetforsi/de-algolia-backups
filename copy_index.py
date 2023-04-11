import os
import time
from algoliasearch.search_client import SearchClient
from algoliasearch.account_client import AccountClient



SOURCE_APP_ID =  os.environ["SOURCE_APP_ID"]
SOURCE_API_KEY = os.environ["SOURCE_API_KEY"]

TARGET_APP_ID = os.environ["TARGET_APP_ID"]
TARGET_API_KEY = os.environ["TARGET_API_KEY"]


def get_indices_names(app_id,api_key):
    client = SearchClient.create(app_id,api_key)
    indices = client.list_indices()["items"]
    indices_names = [ index["name"] for index in indices]
    return indices_names


def copy_index_between_applications(index_name):
    source_index = SearchClient.create(
        SOURCE_APP_ID, SOURCE_API_KEY
    ).init_index(index_name)

    target_index = SearchClient.create(
        TARGET_APP_ID, TARGET_API_KEY
    ).init_index(index_name)

    AccountClient.copy_index(source_index, target_index)


if __name__ == "__main__":
    indices = get_indices_names(SOURCE_APP_ID,SOURCE_API_KEY)

    # Get indices that have "qa","dev","test" on name
    indices_to_copy = [ name for name in indices if "dev" in name or "qa" in name or "test" in name] 
    
    indices_to_copy = indices_to_copy[0:2]

    for index_name in indices_to_copy:
        print("Processing :" + index_name)
        try:
            copy_index_between_applications(index_name=index_name)
            print("Index " + index_name + " was copied")
        except:
            print("Index " + index_name + " was not copied. Maybe already exists")
            continue

