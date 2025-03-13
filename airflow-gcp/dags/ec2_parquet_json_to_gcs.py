import os
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from google.cloud import storage
import time

# TODO: convert .csv.gz to a file format processable by BigQuery

#Change this to your bucket name
BUCKET_NAME = "dtc-de-446723-fitbit-bucket"

# If you authenticated through the GCP SDK you can comment out these two lines
CREDENTIALS_FILE = "google_credentials.json"  
client = storage.Client.from_service_account_json(CREDENTIALS_FILE)

# e.g.  "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-01.csv.gz"
BASE_URL = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/"
DOWNLOAD_DIR = "."

FILE_SUFFIX = ".csv.gz"

CHUNK_SIZE = 8 * 1024 * 1024  

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

bucket = client.bucket(BUCKET_NAME)

def download_file(filename):
    
    url = f"{BASE_URL}/{filename}{FILE_SUFFIX}"
    file_path = os.path.join(DOWNLOAD_DIR, f"{filename}{FILE_SUFFIX}")

    if os.path.exists(f"{filename}{FILE_SUFFIX}"):
        print(f"Found {url} Locally...")
        return file_path

    try:
        print(f"Downloading {url}...")
        urllib.request.urlretrieve(url, file_path)
        print(f"Downloaded: {file_path}")
        return file_path
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return None


def verify_gcs_upload(blob_name):
    return storage.Blob(bucket=bucket, name=blob_name).exists(client)


def upload_to_gcs(file_path, max_retries=3):
    blob_name = os.path.basename(file_path)
    blob = bucket.blob(blob_name)
    blob.chunk_size = CHUNK_SIZE  
    
    for attempt in range(max_retries):
        try:
            print(f"Uploading {file_path} to {BUCKET_NAME} (Attempt {attempt + 1})...")
            blob.upload_from_filename(file_path)
            print(f"Uploaded: gs://{BUCKET_NAME}/{blob_name}")
            
            if verify_gcs_upload(blob_name):
                print(f"Verification successful for {blob_name}")
                return
            else:
                print(f"Verification failed for {blob_name}, retrying...")
        except Exception as e:
            print(f"Failed to upload {file_path} to GCS: {e}")
        
        time.sleep(5)  
    
    print(f"Giving up on {file_path} after {max_retries} attempts.")


if __name__ == "__main__":
    private_jsons = ["google_credentials.json", "fitbit_project_info.json", "fitbit_tokens.json", "fitbit_data.json"]
    file_paths = [os.path.join(DOWNLOAD_DIR, f) for f in os.listdir(DOWNLOAD_DIR) if (f not in private_jsons) and (f.startswith('.parquet') or f.endswith('.json'))]
    
    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(upload_to_gcs, filter(None, file_paths))  # Remove None values

    print("All files processed and verified.")