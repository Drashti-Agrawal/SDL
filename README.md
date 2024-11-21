1.	Introduction
1.1	Objective
This document specifies the requirements for the development of a PDF Processing API. The API is designed to automate the process of extracting attendance data from a PDF and generating subject-specific reports in both PDF and Excel formats. This API will help distribute individual subject reports to students based on the extracted attendance data.
1.2	Scope
The system will allow users to upload PDF files containing attendance sheets. It will extract the data, convert it into CSV format, and then generate reports for each subject, providing attendance statistics in both PDF and Excel formats.


2.	Functional Requirements
2.1	PDF Upload
API must accept PDF file uploads.
Input: PDF attendance sheet.
Output: Confirmation of successful upload.
2.2	Data Extraction
The system extracts attendance data from PDF and converts it into a CSV file.
Input: PDF file.
Output: CSV file with extracted data.
2.3	Report Generation
For each subject, generate detailed reports in both PDF and Excel formats, containing attendance totals, attended days, and percentages.
Input: CSV, subject details.
Output: PDF and Excel reports for each subject.
2.4	Error Handling
Validate file formats and handle errors for missing or invalid files.

3.	System Design
Backend: Python (Flask)
Frontend: HTML & CSS
Libraries: `pdfplumber`, `pandas`, `csv`, `reportlab`
Storage: Filesystem for uploads, CSV, and generated reports.
API Framework: Flask with CORS enabled for cross-origin requests.


4.	API Endpoints
4.1	GET /
Welcome and usage instructions.
4.2	POST /upload
Upload a PDF file for processing.
4.3	GET /download/csv
Dowload the generated CSV file.
4.4	GET /download/{filename}
Download a specific PDF or Excel report.
4.5	GET /download/excel/{filename}
Download a specific Excel file
 
5.	Folder Structure
`uploads/`: Stores uploaded PDFs.
`results/{pdf_name}/`: Stores generated PDF reports.
`csv/{pdf_name}/`: Stores generated CSV files.
`excel/{pdf_name}/`: Stores generated Excel files.


6.	Conclusion
The PDF Processing API efficiently handles the extraction of attendance data from PDF files and generates subject-specific reports in PDF and Excel formats.
