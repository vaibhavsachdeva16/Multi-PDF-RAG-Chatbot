import tempfile
from streamlit.runtime.uploaded_file_manager import UploadedFile


def save_uploaded_file(uploaded_file: UploadedFile) -> str:
    """
    Save a Streamlit UploadedFile to a temporary file and return its path.

    Args:
        uploaded_file (UploadedFile): Uploaded PDF from Streamlit.

    Returns:
        str: Path to the temporary PDF file.
    """

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix='.pdf'
    ) as temp_file:

        temp_file.write(uploaded_file.getvalue())

        return temp_file.name
