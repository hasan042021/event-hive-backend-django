from supabase import create_client
from django.conf import settings


def get_supabase_client():
    """
    Initialize and return a Supabase client instance.
    Ensure settings are configured with SUPABASE_URL and SUPABASE_API_KEY.
    """
    if not settings.SUPABASE_URL or not settings.SUPABASE_API_KEY:
        raise ValueError("SUPABASE_URL and SUPABASE_API_KEY must be set in settings.")

    return create_client(settings.SUPABASE_URL, settings.SUPABASE_API_KEY)


def upload_to_supabase(supabase_client, bucket, file, path):
    """
    Upload a file to Supabase Storage and return the public URL.

    Args:
        supabase_client: The Supabase client instance.
        bucket: The bucket name.
        file: The file object to upload.
        path: The destination path in the bucket.

    Returns:
        str: Public URL of the uploaded file.

    Raises:
        Exception: If the upload fails.
    """
    # Ensure the bucket exists before uploading
    response = supabase_client.storage.from_(bucket).list()
    if response.get("error"):
        raise Exception(f"Bucket validation error: {response['error']['message']}")

    # Perform the upload
    response = supabase_client.storage.from_(bucket).upload(path, file)
    if response.get("error"):
        raise Exception(f"Upload error: {response['error']['message']}")

    return supabase_client.storage.from_(bucket).get_public_url(path)["publicURL"]
