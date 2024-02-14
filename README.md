# A4_Resume_Parser

![image](https://github.com/edvyan/A4_Resume_Parser/assets/46171741/0c237593-f8c4-4766-9e99-8c73c9decbd0)

To Run the application, navigate to app folder and type:  
- python app.py

This Dash-based web application provides a convenient way to extract and analyze key information from PDF documents. It's designed to be user-friendly and efficient, making it ideal for users who need to process PDFs to extract structured data like skills, education, and languages.

## Features

- **PDF Upload**: Easy-to-use drag-and-drop interface for uploading PDF files. 
- **Data Parsing**: After uploading, users can initiate the parsing process with a "Parse" button. The application leverages a spaCy NLP pipeline to extract text from the PDF and identify relevant information.
- **Information Extraction**: The app focuses on extracting specific details such as skills, educational background, and languages from the text. This process includes cleaning and preprocessing the data to ensure accuracy and relevance.
- **Data Display**: Extracted information is immediately displayed on the web page, providing users with instant insights into the contents of the uploaded PDF.
- **Excel Download**: Users have the option to download the extracted data as an Excel file for further use. This feature is enabled by a "Download Excel" button on the interface.

## Usage

1. **Upload a PDF**: Drag and drop a PDF file into the designated area or use the file dialog to select a file.
2. **Parse the PDF**: Click the "Parse" button to start the extraction process.
3. **Review Extracted Data**: View the extracted skills, education, and languages directly on the web page.
4. **Download Excel File**: Click the "Download Excel" button to save the processed data to your device.

## Technical Details

- **Framework**: The application is built using the Dash framework, a Python framework for building web applications.
- **Data Processing**: Utilizes PyPDF2 for reading PDF files and spaCy for natural language processing.
- **Styling**: Styled with Dash Bootstrap Components for a responsive and modern user interface.

## System Requirements

- Python 3.x
- Required Python libraries: Dash, Pandas, spaCy, PyPDF2, Dash Bootstrap Components


