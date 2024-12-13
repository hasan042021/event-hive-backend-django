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


def upload_to_supabase(
    supabase_client, bucket_name, file, file_path, old_file_path=None
):
    if old_file_path:
        delete_response = supabase_client.storage.from_(bucket_name).remove(
            [old_file_path]
        )
        print("Delete response:", delete_response)  # Debugging the delete response

        # Check for any errors during deletion
        if "error" in delete_response:
            raise ValueError(f"Error deleting old file: {delete_response['error']}")
    """
    Upload the file to Supabase storage and return the public URL.
    """
    # Open the file and upload to Supabase storage
    print(file)
    file_bytes = file.read()
    response = supabase_client.storage.from_(bucket_name).upload(file_path, file_bytes)

    # Get the public URL for the uploaded file
    # Check for an error in the response
    public_url = supabase_client.storage.from_(bucket_name).get_public_url(file_path)

    return public_url
