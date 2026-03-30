import pandas as pd
from io import BytesIO
from docx import Document


def process_files(docx_path):
    # Load the DOCX file
    doc = Document(docx_path)
    data = []

    # Process the document and extract text
    for paragraph in doc.paragraphs:
        if paragraph.text:
            data.append(paragraph.text)

    # Create a DataFrame from the extracted data
    df = pd.DataFrame(data, columns=['Text'])

    # Save the DataFrame to an Excel file in memory
    excel_file = BytesIO()
    df.to_excel(excel_file, index=False)
    excel_file.seek(0)  # Move to the beginning of the BytesIO stream

    return excel_file.getvalue()  # Return Excel file bytes