from io import BytesIO
import s3_manager


'''
    step 1: save_file_to_internal_storage
'''


def save_file_to_internal_storage(path: str, content: BytesIO) -> str:
    return s3_manager.upload_file(path, content)
