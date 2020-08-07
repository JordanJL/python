import os
import uuid
import sys
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, PublicAccess
def run_sample():
    try:
        # Create the BlobServiceClient that is used to call the Blob service for the storage account
        conn_str = 'DefaultEndpointsProtocol=https;AccountName=fenix2fun2me;AccountKey=qEZhKqhySrIvLgiplmWIVwTR9kCFtznIFEmMhrfF56jWwlSnUJuh2fCXYmBtKl2dafQb+f/UYBUv1RQP5n9/Mg==;EndpointSuffix=core.windows.net'
        #os.environ['AZURE_STORAGE_CONNECTIONSTRING']
        blob_service_client = BlobServiceClient.from_connection_string(conn_str=conn_str)

        # Create a container called 'quickstartblobs' and Set the permission so the blobs are public.
        container_name = 'cosito'
        #blob_service_client.create_container(
            #container_name, public_access=PublicAccess.Container)

        # Create Sample folder if it not exists, and create a file in folder Sample to test the upload and download.
        local_path = os.path.expanduser("~/Sample")
        if not os.path.exists(local_path):
            os.makedirs(os.path.expanduser("~/Sample"))
        local_file_name = "QuickStart_" + str(uuid.uuid4()) + ".txt"
        full_path_to_file = os.path.join(local_path, local_file_name)

        # Write text to the file.
        file = open(full_path_to_file,  'w')
        file.write("Hello, World!")
        file.close()

        print("Temp file = " + full_path_to_file)
        print("\nUploading to Blob storage as blob" + local_file_name)

        # Upload the created file, use local_file_name for the blob name
        blob_client = blob_service_client.get_blob_client(
            container=container_name, blob=local_file_name)
        with open(full_path_to_file, "rb") as data:
            blob_client.upload_blob(data)
      

        sys.stdout.write("Sample finished running. When you hit <any key>, the sample will be deleted and the sample "
                         "application will exit.")
        sys.stdout.flush()
        input()

        # Clean up resources. This includes the container and the temp files
        blob_service_client.delete_container(container_name)
        os.remove(full_path_to_file)
        os.remove(full_path_to_file2)
    except Exception as e:
        print(e)


# Main method.
if __name__ == '__main__':
    run_sample()