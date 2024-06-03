import os
import shutil
from pypdf import PdfReader
from langchain.tools import tool

class PDFManagementTool:

    @staticmethod
    @tool("UploadPDF")
    def upload_pdf(file_path: str) -> dict:
        """Uploads a PDF file to the server and returns a confirmation message."""
        # Assuming the PDF is uploaded to a local directory for simplicity
        if not os.path.exists('uploaded_files'):
            os.makedirs('uploaded_files')
        destination = os.path.join('uploaded_files', os.path.basename(file_path))
        shutil.move(file_path, destination)
        return {"status": "success", "file_path": destination}

    @staticmethod
    @tool("ProcessPDF")
    def process_pdf(file_path: str) -> str:
        """Processes the PDF file and returns its content."""
        try:
            # Read the PDF file
            with open(file_path, 'rb') as file:
                reader = PdfReader(file)
                text_content = ""
                for page_num in range(len(reader.pages)):
                    page = reader.pages[page_num]
                    text_content += page.extract_text() + "\n"

            return f"Extracted content from {file_path}:\n\n{text_content}"

        except Exception as e:
            return f"An error occurred while processing the PDF: {e}"

    @staticmethod
    @tool("ListPDFs")
    def list_files() -> dict:
        """Lists uploaded PDF files."""
        files = os.listdir('uploaded_files') if os.path.exists('uploaded_files') else []
        return {"files": files}

    @staticmethod
    @tool("RetrievePDFContent")
    def retrieve_file_content(file_name: str) -> str:
        """Retrieves the content of a specific PDF file."""
        file_path = os.path.join('uploaded_files', file_name)
        if os.path.exists(file_path):
            return PDFManagementTool.process_pdf(file_path)
        return f"File {file_name} not found."

    @staticmethod
    @tool("DeletePDF")
    def delete_file(file_name: str) -> dict:
        """Deletes a specific PDF file."""
        file_path = os.path.join('uploaded_files', file_name)
        if os.path.exists(file_path):
            os.remove(file_path)
            return {"status": "deleted", "file_name": file_name}
        return {"status": "file not found", "file_name": file_name}