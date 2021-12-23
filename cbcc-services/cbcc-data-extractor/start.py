import json
import requests
from requests.exceptions import Timeout
import os
import subprocess

def guess_and_check(priconne_cdn_host, current_truth_version, current_hash, max_test_amount, test_multiplier):
    latest_truth_version, latest_hash = current_truth_version, current_hash
    
    i = 0
    while i < max_test_amount:
        truth_version_guess = current_truth_version + (i * test_multiplier)
        
        asset_manifest_endpoint = f'{priconne_cdn_host}/dl/resources/{truth_version_guess}/Jpn/AssetBundles/Windows/manifest/masterdata_assetmanifest'
        masterdata_assetmanifest_response = requests.get(asset_manifest_endpoint)
        
        if (masterdata_assetmanifest_response.ok):
            print('Found new truth version, updating the new truth')
            response_text = masterdata_assetmanifest_response.text
            
            latest_truth_version = truth_version_guess
            latest_hash = response_text.split(',')[1]
            
            break
        
        i += 1
    
    return latest_truth_version, latest_hash

def check_and_update_master_db():
    with open('config.json', 'r') as config_file:
        data = json.load(config_file)
    
    ## Determine latest truth version
    current_dir = os.getcwd()
    
    current_truth_version = data["database"]["current_truth_version"] 
    current_hash = data["database"]["current_hash"]
    latest_version_endpoint = data["latest_version_endpoint"]
    database_directory = data["database"]["master_db_directory"]
    priconne_cdn_host = data["priconne_cdn_host"]
    max_test_amount = data["database"]["max_test_amount"]
    test_multiplier = data["database"]["test_multiplier"]
    
    initial_load = not os.path.exists(os.path.join(current_dir, database_directory, f'master_{current_hash}.db'))
    
    try:
        print("Attempting to hit estertion endpoint")
        latest_version_response = requests.get(latest_version_endpoint, timeout=10)
    except Timeout:
        print('Estertion request timed out, beginning the guess and check method')
        latest_truth_version, latest_hash = guess_and_check(priconne_cdn_host, current_truth_version, current_hash, max_test_amount, test_multiplier)
    else:
        print("Estertion request successful")
        latest_version_response_json = latest_version_response.json()
        latest_truth_version, latest_hash = latest_version_response_json["TruthVersion"], latest_version_response_json["hash"]
        
    if (not initial_load and latest_truth_version == current_truth_version):
        print("Current truth version matches the current latest truth version, no master database updates required.")
    else:
        print("New truth version and hash required (or there was no initial load), beginning new master db retrieval")
        
        database_dir_path = os.path.join(current_dir, database_directory)
        
        if not os.path.exists(database_dir_path):
            os.makedirs(database_dir_path)
        
        cdb_path = os.path.join(database_dir_path, 'master.cdb')
        db_path = os.path.join(database_dir_path, f'master_{latest_hash}.db')
        
        db_endpoint = f'{priconne_cdn_host}/dl/pool/AssetBundles/{latest_hash[0:2]}/{latest_hash}'
        encrypted_db_response = requests.get(db_endpoint)
        
        with open(cdb_path, 'wb') as cdb_file:
            cdb_file.write(encrypted_db_response.content)
            
        coneshell_exe = os.path.join(current_dir, 'Coneshell_call.exe')
        coneshell_call = f"{coneshell_exe} -cdb {cdb_path} {db_path}"
        subprocess.run(coneshell_call, shell=True)
        print("new database has been retrieved")
        
        data["database"]["current_truth_version"] = latest_truth_version
        data["database"]["current_hash"] = latest_hash
        
        with open("config.json", "w") as config_file:
            json.dump(data, config_file, indent=4)
        
        print('Updated config with latest truth version and hash')
        
        os.remove(cdb_path)
        print("Removed cdb file")

        
if __name__ == "__main__":
    check_and_update_master_db()