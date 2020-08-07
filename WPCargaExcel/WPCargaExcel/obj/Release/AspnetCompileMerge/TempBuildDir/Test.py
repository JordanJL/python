class Test(object):
    """description of class"""

    import os
    import sys
    import time
    from azure.storage.blob import BlobServiceClient


    #CONNECTION_STRING = os.environ['DefaultEndpointsProtocol=https;AccountName=fenix2fun2me;AccountKey=qEZhKqhySrIvLgiplmWIVwTR9kCFtznIFEmMhrfF56jWwlSnUJuh2fCXYmBtKl2dafQb+f/UYBUv1RQP5n9/Mg==;EndpointSuffix=core.windows.net']
    status = None
    blob_service_client = BlobServiceClient.from_connection_string('DefaultEndpointsProtocol=https;AccountName=fenix2fun2me;AccountKey=qEZhKqhySrIvLgiplmWIVwTR9kCFtznIFEmMhrfF56jWwlSnUJuh2fCXYmBtKl2dafQb+f/UYBUv1RQP5n9/Mg==;EndpointSuffix=core.windows.net')
    source_blob = "http://www.gutenberg.org/files/59466/59466-0.txt"
    copied_blob = blob_service_client.get_blob_client("cosito", '59466-0.txt')
    # Copy started
    copied_blob.start_copy_from_url(source_blob)
    for i in range(10):
        props = copied_blob.get_blob_properties()
        status = props.copy.status
        print("Copy status: " + status)
        if status == "success":
            # Copy finished
            break
        time.sleep(10)

    if status != "success":
        # if not finished after 100s, cancel the operation
        props = copied_blob.get_blob_properties()
        print(props.copy.status)
        copy_id = props.copy.id
        copied_blob.abort_copy(copy_id)
        props = copied_blob.get_blob_properties()
        print(props.copy.status)
