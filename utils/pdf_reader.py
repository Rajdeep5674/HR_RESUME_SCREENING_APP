import pdfplumber
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_text_from_pdf(pdf_file) -> str:
    """
    Extracts all text from a PDF file object or file path.
    
    Args:
        pdf_file: A path to a PDF file, or a file-like object (e.g., BytesIO from Streamlit's file uploader).
        
    Returns:
        str: Extracted text from all pages of the PDF, or an empty string if extraction fails.
    """
    text = []
    try:
        # Open the PDF file
        with pdfplumber.open(pdf_file) as pdf:
            # Loop through all pages and extract text
            for i, page in enumerate(pdf.pages):
                page_text = page.extract_text()
                if page_text:
                    text.append(page_text)
                else:
                    logger.warning(f"No text found on page {i + 1}")
        
        # Combine text from all pages
        full_text = "\n".join(text)
        return full_text.strip()
        
    except Exception as e:
        logger.error(f"Error extracting text from PDF: {str(e)}")
        raise RuntimeError(f"Failed to read the PDF file: {str(e)}")
