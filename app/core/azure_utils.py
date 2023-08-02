from datetime import datetime, timedelta
import os
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions

CONTAINER_NAME = "uploads"


def get_blob_service_client():
    connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    if not connection_string:
        raise ValueError(
            "Azure Storage Connection String not found in environment variables."
        )
    return BlobServiceClient.from_connection_string(connection_string)


def generate_download_link(blob_service_client: BlobServiceClient, file_path: str):
    blob_client = blob_service_client.get_blob_client(CONTAINER_NAME, file_path)
    sas_token = generate_blob_sas(
        blob_service_client.account_name,
        CONTAINER_NAME,
        file_path,
        account_key=blob_service_client.credential.account_key,
        permission=BlobSasPermissions(read=True),
        expiry=datetime.utcnow() + timedelta(days=1),  # token valid for 1 hour
    )
    sas_url = blob_client.url + "?" + sas_token
    return sas_url


from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()
    blob_service_client = get_blob_service_client()
    file_path = "ab2f11263d9297ab/out/screen.bmp"
    dl_link = generate_download_link(blob_service_client, file_path)
    print(dl_link)
