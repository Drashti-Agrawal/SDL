# from flask import Flask, request, jsonify, send_from_directory
# from flask_cors import CORS
# import os
# import csv
# import pdfplumber
# import pandas as pd
# from reportlab.lib.pagesizes import letter
# from reportlab.lib import colors
# from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

# app = Flask(__name__)
# CORS(app)

# UPLOAD_FOLDER = 'uploads'
# RESULTS_BASE_FOLDER = 'results'
# CSV_BASE_FOLDER = 'csv'
# EXCEL_BASE_FOLDER = 'excel'

# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# os.makedirs(RESULTS_BASE_FOLDER, exist_ok=True)
# os.makedirs(CSV_BASE_FOLDER, exist_ok=True)
# os.makedirs(EXCEL_BASE_FOLDER, exist_ok=True)

# def create_folders_for_pdf(pdf_name):
#     # Create a unique folder for each PDF upload
#     base_name = os.path.splitext(pdf_name)[0]
#     results_folder = os.path.join(RESULTS_BASE_FOLDER, base_name)
#     csv_folder = os.path.join(CSV_BASE_FOLDER, base_name)
#     excel_folder = os.path.join(EXCEL_BASE_FOLDER, base_name)
    
#     os.makedirs(results_folder, exist_ok=True)
#     os.makedirs(csv_folder, exist_ok=True)
#     os.makedirs(excel_folder, exist_ok=True)
    
#     return results_folder, csv_folder, excel_folder

# def extract_data_to_csv(pdf_path, csv_folder):
#     csv_path = os.path.join(csv_folder, 'data.csv')
#     with pdfplumber.open(pdf_path) as pdf:
#         with open(csv_path, 'w', newline='') as csv_file:
#             writer = csv.writer(csv_file)
#             for page in pdf.pages:
#                 table = page.extract_table()
#                 if table:
#                     # Skip first 4 rows (header and instructions) and 6th row
#                     table = table[4:6] + table[6:]
#                     writer.writerows(table)
#     return csv_path

# def create_files(df, results_folder, excel_folder):
#     # Extract subject-specific columns
#     subjects = {
#         'Deep Learning': ['Total Classes_DL', 'Total Present_DL', 'Percentage_DL', 'Total Lab_DL', 'Total Present_Lab_DL', 'Percentage_Lab_DL'],
#         'System Operations Lab': ['Total Classes_SOL', 'Total Present_SOL', 'Percentage_SOL'],
#         'Product Development & QA': ['Total Classes_PDQA', 'Total Present_PDQA', 'Percentage_PDQA', 'Total Lab_PDQA', 'Total Present_Lab_PDQA', 'Percentage_Lab_PDQA'],
#     }
    
#     for subject, columns in subjects.items():
#         subject_name = subject.strip()
        
#         # Create PDF path for the subject
#         pdf_path = os.path.join(results_folder, f"{subject_name}_attendance_report.pdf")
#         pdf = SimpleDocTemplate(pdf_path, pagesize=letter)
#         elements = []
#         # Create table header
#         data = [['S.No.', 'Enrollment No.', 'Name'] + columns]

#         # Append relevant data from the dataframe
#         for _, row in df.iterrows():
#             s_no = row['S.No.']
#             enrollment_no = row['Enrollment No.']
#             name = row['Name']
#             subject_data = [row.get(col, 'N/A') for col in columns]
#             data.append([s_no, enrollment_no, name] + subject_data)

#         table = Table(data)
#         table.setStyle(TableStyle([
#             ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
#             ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
#             ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#             ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
#             ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
#             ('BACKGROUND', (0, 1), (-1, -1), colors.white),
#             ('GRID', (0, 0), (-1, -1), 1, colors.black),
#             ('BOX', (0, 0), (-1, -1), 2, colors.black),
#         ]))
#         elements.append(table)
#         pdf.build(elements)

#         # Create Excel path for the subject
#         excel_path = os.path.join(excel_folder, f"{subject_name}_attendance_report.xlsx")
#         subject_df = df[['S.No.', 'Enrollment No.', 'Name'] + columns].copy()
#         subject_df.rename(columns={col: f'{col}' for col in columns}, inplace=True)
#         subject_df.to_excel(excel_path, index=False)

# def process_csv_to_df(csv_path, results_folder, excel_folder):
#     df = pd.read_csv(csv_path)
    
#     if df.empty:
#         raise ValueError("CSV file is empty or could not be read.")
    
#     # Rename columns based on the attendance format
#     # Assuming that from the 7th row (index 6), column names begin
#     df.columns = ['S.No.', 'Enrollment No.', 'Name', 'Total Classes_DL', 'Total Present_DL', 'Percentage_DL',
#                   'Total Lab_DL', 'Total Present_Lab_DL', 'Percentage_Lab_DL', 'Total Classes_SOL', 
#                   'Total Present_SOL', 'Percentage_SOL', 'Total Classes_PDQA', 'Total Present_PDQA', 
#                   'Percentage_PDQA', 'Total Lab_PDQA', 'Total Present_Lab_PDQA', 'Percentage_Lab_PDQA']
    
#     # Create PDF and Excel files for each subject
#     create_files(df, results_folder, excel_folder)
    
#     return df

# def process_data(pdf_path, pdf_name):
#     # Create folders for the PDF
#     results_folder, csv_folder, excel_folder = create_folders_for_pdf(pdf_name)
    
#     # Extract data to CSV
#     csv_path = extract_data_to_csv(pdf_path, csv_folder)
    
#     # Process CSV to DataFrame and create files
#     df = process_csv_to_df(csv_path, results_folder, excel_folder)
#     return df

# @app.route('/')
# def index():
#     return '''
#     <h1>Welcome to the PDF Processing API</h1>
#     <p>Use the <a href="/upload">/upload</a> endpoint to upload PDF files.</p>
#     <p>Use the <a href="/download/csv">/download/csv</a> endpoint to download the generated CSV file.</p>
#     <p>Use the <a href="/download/filename">/download/filename</a> endpoint to download generated PDF reports.</p>
#     <p>Use the <a href="/download/excel/filename">/download/excel/filename</a> endpoint to download generated Excel reports.</p>
#     '''

# @app.route('/upload', methods=['POST'])
# def upload_file():
#     if 'pdfFile' not in request.files:
#         return jsonify({'error': 'No file part'}), 400
    
#     file = request.files['pdfFile']
#     if file.filename == '':
#         return jsonify({'error': 'No selected file'}), 400
    
#     if file and file.filename.endswith('.pdf'):
#         file_path = os.path.join(UPLOAD_FOLDER, file.filename)
#         file.save(file_path)
        
#         try:
#             df = process_data(file_path, file.filename)
#             csv_file = 'data.csv'
#             base_name = os.path.splitext(file.filename)[0]
#             results_folder = os.path.join(RESULTS_BASE_FOLDER, base_name)
#             excel_folder = os.path.join(EXCEL_BASE_FOLDER, base_name)
#             pdf_files = [f for f in os.listdir(results_folder) if f.endswith('.pdf')]
#             excel_files = [f for f in os.listdir(excel_folder) if f.endswith('.xlsx')]
#             return jsonify({'csv_file': csv_file, 'pdf_files': pdf_files, 'excel_files': excel_files})
#         except ValueError as e:
#             return jsonify({'error': str(e)}), 400
#         except Exception as e:
#             return jsonify({'error': str(e)}), 500
    
#     return jsonify({'error': 'Invalid file format'}), 400

# @app.route('/download/<filename>')
# def download_file(filename):
#     safe_filename = os.path.basename(filename)  # Prevent directory traversal
#     base_name = os.path.splitext(filename)[0]
#     results_folder = os.path.join(RESULTS_BASE_FOLDER, base_name)
#     if filename.endswith('.pdf'):
#         return send_from_directory(results_folder, safe_filename)
#     elif filename.endswith('.xlsx'):
#         excel_folder = os.path.join(EXCEL_BASE_FOLDER, base_name)
#         return send_from_directory(excel_folder, safe_filename)
#     else:
#         return jsonify({'error': 'File not found'}), 404

# @app.route('/download/csv')
# def download_csv():
#     # Assuming the CSV file is in the folder named after the latest uploaded PDF file
#     latest_folder = max([os.path.join(CSV_BASE_FOLDER, d) for d in os.listdir(CSV_BASE_FOLDER)], key=os.path.getctime)
#     csv_path = os.path.join(latest_folder, 'data.csv')
#     if os.path.exists(csv_path):
#         return send_from_directory(latest_folder, 'data.csv')
#     return jsonify({'error': 'CSV file not found'}), 404

# @app.route('/download/excel/<filename>')
# def download_excel(filename):
#     safe_filename = os.path.basename(filename)  # Prevent directory traversal
#     base_name = os.path.splitext(filename)[0]
#     excel_folder = os.path.join(EXCEL_BASE_FOLDER, base_name)
#     return send_from_directory(excel_folder, safe_filename)

# if __name__ == '__main__':
#     app.run(debug=True)


# from flask import Flask, request, jsonify, send_from_directory
# from flask_cors import CORS
# import os
# import csv
# import pdfplumber
# import pandas as pd
# from reportlab.lib.pagesizes import letter
# from reportlab.lib import colors
# from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

# app = Flask(__name__)
# CORS(app)

# UPLOAD_FOLDER = 'uploads'
# RESULTS_BASE_FOLDER = 'results'
# CSV_BASE_FOLDER = 'csv'
# EXCEL_BASE_FOLDER = 'excel'

# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# os.makedirs(RESULTS_BASE_FOLDER, exist_ok=True)
# os.makedirs(CSV_BASE_FOLDER, exist_ok=True)
# os.makedirs(EXCEL_BASE_FOLDER, exist_ok=True)

# def create_folders_for_pdf(pdf_name):
#     base_name = os.path.splitext(pdf_name)[0]
#     results_folder = os.path.join(RESULTS_BASE_FOLDER, base_name)
#     csv_folder = os.path.join(CSV_BASE_FOLDER, base_name)
#     excel_folder = os.path.join(EXCEL_BASE_FOLDER, base_name)
    
#     os.makedirs(results_folder, exist_ok=True)
#     os.makedirs(csv_folder, exist_ok=True)
#     os.makedirs(excel_folder, exist_ok=True)
    
#     return results_folder, csv_folder, excel_folder

# def extract_data_to_csv(pdf_path, csv_folder):
#     csv_path = os.path.join(csv_folder, 'data.csv')
#     with pdfplumber.open(pdf_path) as pdf:
#         with open(csv_path, 'w', newline='') as csv_file:
#             writer = csv.writer(csv_file)
#             for page in pdf.pages:
#                 table = page.extract_table()
#                 if table:
#                     # Skip first 4 rows (header and instructions) and 6th row for subject names
#                     table = table[4:6] + table[6:]
#                     writer.writerows(table)
#     return csv_path

# def create_files(df, results_folder, excel_folder, subjects):
#     for subject, columns in subjects.items():
#         subject_name = subject.strip()

#         # Create PDF path for the subject
#         pdf_path = os.path.join(results_folder, f"{subject_name}_attendance_report.pdf")
#         pdf = SimpleDocTemplate(pdf_path, pagesize=letter)
#         elements = []

#         # Create table header
#         data = [['S.No.', 'Enrollment No.', 'Name'] + columns]

#         # Append relevant data from the dataframe
#         for _, row in df.iterrows():
#             s_no = row['S.No.']
#             enrollment_no = row['Enrollment No.']
#             name = row['Name']
#             subject_data = [row.get(col, 'N/A') for col in columns]
#             data.append([s_no, enrollment_no, name] + subject_data)

#         table = Table(data)
#         table.setStyle(TableStyle([
#             ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
#             ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
#             ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#             ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
#             ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
#             ('BACKGROUND', (0, 1), (-1, -1), colors.white),
#             ('GRID', (0, 0), (-1, -1), 1, colors.black),
#             ('BOX', (0, 0), (-1, -1), 2, colors.black),
#         ]))
#         elements.append(table)
#         pdf.build(elements)

#         # Create Excel path for the subject
#         excel_path = os.path.join(excel_folder, f"{subject_name}_attendance_report.xlsx")
#         subject_df = df[['S.No.', 'Enrollment No.', 'Name'] + columns].copy()
#         subject_df.rename(columns={col: f'{col}' for col in columns}, inplace=True)
#         subject_df.to_excel(excel_path, index=False)

# def process_csv_to_df(csv_path, results_folder, excel_folder):
#     df = pd.read_csv(csv_path)
    
#     if df.empty:
#         raise ValueError("CSV file is empty or could not be read.")

#     # Assuming the subject names are in specific columns like in your image
#     subjects = {
#         'Deep Learning': ['Total Classes', 'Total Present', 'Percentage', 'Total Lab', 'Total Present Lab', 'Percentage Lab'],
#         'System Operations Lab': ['Total Classes', 'Total Present', 'Percentage'],
#         'Product Development & QA Workshop': ['Total Classes', 'Total Present', 'Percentage', 'Total Lecture', 'Total Attended', 'Total Percentage'],
#     }
    
#     # Rename columns based on the attendance format in the screenshot
#     df.columns = ['S.No.', 'Enrollment No.', 'Name', 'Total Classes_DL', 'Total Present_DL', 'Percentage_DL',
#                   'Total Lab_DL', 'Total Present_Lab_DL', 'Percentage_Lab_DL', 'Total Classes_SOL', 
#                   'Total Present_SOL', 'Percentage_SOL', 'Total Classes_PDQA', 'Total Present_PDQA', 
#                   'Percentage_PDQA', 'Total Lecture_PDQA', 'Total Attended_PDQA', 'Total Percentage_PDQA']
    
#     # Create PDF and Excel files for each subject
#     create_files(df, results_folder, excel_folder, subjects)
    
#     return df

# def process_data(pdf_path, pdf_name):
#     # Create folders for the PDF
#     results_folder, csv_folder, excel_folder = create_folders_for_pdf(pdf_name)
    
#     # Extract data to CSV
#     csv_path = extract_data_to_csv(pdf_path, csv_folder)
    
#     # Process CSV to DataFrame and create files
#     df = process_csv_to_df(csv_path, results_folder, excel_folder)
#     return df

# @app.route('/')
# def index():
#     return '''
#     <h1>Welcome to the PDF Processing API</h1>
#     <p>Use the <a href="/upload">/upload</a> endpoint to upload PDF files.</p>
#     <p>Use the <a href="/download/csv">/download/csv</a> endpoint to download the generated CSV file.</p>
#     <p>Use the <a href="/download/filename">/download/filename</a> endpoint to download generated PDF reports.</p>
#     <p>Use the <a href="/download/excel/filename">/download/excel/filename</a> endpoint to download generated Excel reports.</p>
#     '''

# @app.route('/upload', methods=['POST'])
# def upload_file():
#     if 'pdfFile' not in request.files:
#         return jsonify({'error': 'No file part'}), 400
    
#     file = request.files['pdfFile']
#     if file.filename == '':
#         return jsonify({'error': 'No selected file'}), 400
    
#     if file and file.filename.endswith('.pdf'):
#         file_path = os.path.join(UPLOAD_FOLDER, file.filename)
#         file.save(file_path)
        
#         try:
#             df = process_data(file_path, file.filename)
#             csv_file = 'data.csv'
#             base_name = os.path.splitext(file.filename)[0]
#             results_folder = os.path.join(RESULTS_BASE_FOLDER, base_name)
#             excel_folder = os.path.join(EXCEL_BASE_FOLDER, base_name)
#             pdf_files = [f for f in os.listdir(results_folder) if f.endswith('.pdf')]
#             excel_files = [f for f in os.listdir(excel_folder) if f.endswith('.xlsx')]
#             return jsonify({'csv_file': csv_file, 'pdf_files': pdf_files, 'excel_files': excel_files})
#         except ValueError as e:
#             return jsonify({'error': str(e)}), 400
#         except Exception as e:
#             return jsonify({'error': str(e)}), 500
    
#     return jsonify({'error': 'Invalid file format'}), 400

# @app.route('/download/<filename>')
# def download_file(filename):
#     safe_filename = os.path.basename(filename)  # Prevent directory traversal
#     base_name = os.path.splitext(filename)[0]
#     results_folder = os.path.join(RESULTS_BASE_FOLDER, base_name)
#     if filename.endswith('.pdf'):
#         return send_from_directory(results_folder, safe_filename)
#     elif filename.endswith('.xlsx'):
#         excel_folder = os.path.join(EXCEL_BASE_FOLDER, base_name)
#         return send_from_directory(excel_folder, safe_filename)
#     else:
#         return jsonify({'error': 'File not found'}), 404

# @app.route('/download/csv')
# def download_csv():
#     # Assuming the CSV file is in the folder named after the latest uploaded PDF file
#     latest_folder = max([os.path.join(CSV_BASE_FOLDER, d) for d in os.listdir(CSV_BASE_FOLDER)], key=os.path.getctime)
#     csv_path = os.path.join(latest_folder, 'data.csv')
#     if os.path.exists(csv_path):
#         return send_from_directory(latest_folder, 'data.csv')
#     return jsonify({'error': 'CSV file not found'}), 404

# @app.route('/download/excel/<filename>')
# def download_excel(filename):
#     safe_filename = os.path.basename(filename)  # Prevent directory traversal
#     base_name = os.path.splitext(filename)[0]
#     excel_folder = os.path.join(EXCEL_BASE_FOLDER, base_name)
#     return send_from_directory(excel_folder, safe_filename)

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import csv
import pdfplumber
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
RESULTS_BASE_FOLDER = 'results'
CSV_BASE_FOLDER = 'csv'
EXCEL_BASE_FOLDER = 'excel'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_BASE_FOLDER, exist_ok=True)
os.makedirs(CSV_BASE_FOLDER, exist_ok=True)
os.makedirs(EXCEL_BASE_FOLDER, exist_ok=True)

def create_folders_for_pdf(pdf_name):
    base_name = os.path.splitext(pdf_name)[0]
    results_folder = os.path.join(RESULTS_BASE_FOLDER, base_name)
    csv_folder = os.path.join(CSV_BASE_FOLDER, base_name)
    excel_folder = os.path.join(EXCEL_BASE_FOLDER, base_name)
    
    os.makedirs(results_folder, exist_ok=True)
    os.makedirs(csv_folder, exist_ok=True)
    os.makedirs(excel_folder, exist_ok=True)
    
    return results_folder, csv_folder, excel_folder

def extract_data_to_csv(pdf_path, csv_folder):
    csv_path = os.path.join(csv_folder, 'data.csv')
    with pdfplumber.open(pdf_path) as pdf:
        with open(csv_path, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            for page in pdf.pages:
                table = page.extract_table()
                if table:
                    # Skip first 4 rows (header and instructions)
                    table = table[4:]
                    
                    # Row 5 is rotated/mirrored, handle it here
                    row_5 = table[0]  # Enrollment and Name data (currently mirrored)
                    row_5_fixed = fix_mirrored_row(row_5)
                    
                    # Row 6 should be ignored, so we skip it
                    row_7 = table[2]  # Subject data, which replaces row 5

                    # Now swap row 5 and row 7 (subjects)
                    table[0], table[2] = row_7, row_5_fixed
                    
                    writer.writerows(table)
    return csv_path

def fix_mirrored_row(row):
    # Add logic to correct mirrored text here (for enrollment data)
    # This would likely involve checking for patterns in how the text appears mirrored
    corrected_row = []
    for cell in row:
        if cell:  # if there is content in the cell
            corrected_row.append(reverse_text_if_mirrored(cell))
        else:
            corrected_row.append('')
    return corrected_row

def reverse_text_if_mirrored(text):
    # This function checks if the text is mirrored and reverses it
    return text[::-1]  # Basic reversal; might need enhancement for more complex mirroring

def create_files(df, results_folder, excel_folder, subjects):
    for subject, columns in subjects.items():
        subject_name = subject.strip()

        # Create PDF path for the subject
        pdf_path = os.path.join(results_folder, f"{subject_name}_attendance_report.pdf")
        pdf = SimpleDocTemplate(pdf_path, pagesize=letter)
        elements = []

        # Create table header
        data = [['S.No.', 'Enrollment No.', 'Name'] + columns]

        # Append relevant data from the dataframe
        for _, row in df.iterrows():
            s_no = row['S.No.']
            enrollment_no = row['Enrollment No.']
            name = row['Name']
            subject_data = [row.get(col, 'N/A') for col in columns]
            data.append([s_no, enrollment_no, name] + subject_data)

        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BOX', (0, 0), (-1, -1), 2, colors.black),
        ]))
        elements.append(table)
        pdf.build(elements)

        # Create Excel path for the subject
        excel_path = os.path.join(excel_folder, f"{subject_name}_attendance_report.xlsx")
        subject_df = df[['S.No.', 'Enrollment No.', 'Name'] + columns].copy()
        subject_df.rename(columns={col: f'{col}' for col in columns}, inplace=True)
        subject_df.to_excel(excel_path, index=False)

def process_csv_to_df(csv_path, results_folder, excel_folder):
    df = pd.read_csv(csv_path)
    
    if df.empty:
        raise ValueError("CSV file is empty or could not be read.")

    # Dynamically detect the subjects from row 7
    subjects_row = df.iloc[0]  # This should now be row 7 after swapping

    # Map subjects dynamically based on what's found in the row
    subjects = {}
    subject_columns = [col for col in df.columns if col.startswith('Subject')]  # Dynamically detected columns
    
    for subject_name in subjects_row:
        # Subject column logic can be dynamic here
        if 'Deep Learning' in subject_name:
            subjects[subject_name] = ['Total Classes_DL', 'Total Present_DL', 'Percentage_DL', 'Total Lab_DL', 'Total Present_Lab_DL', 'Percentage_Lab_DL']
        elif 'System Operations Lab' in subject_name:
            subjects[subject_name] = ['Total Classes_SOL', 'Total Present_SOL', 'Percentage_SOL']
        elif 'Product Development' in subject_name:
            subjects[subject_name] = ['Total Classes_PDQA', 'Total Present_PDQA', 'Percentage_PDQA', 'Total Lecture_PDQA', 'Total Attended_PDQA', 'Total Percentage_PDQA']
        # Add logic to dynamically map columns if subject names change

    # Rename columns based on the updated attendance format
    df.columns = ['S.No.', 'Enrollment No.', 'Name'] + subject_columns
    
    # Generate files for each subject
    create_files(df, results_folder, excel_folder, subjects)

    return df

def process_data(pdf_path, pdf_name):
    # Create folders for the PDF
    results_folder, csv_folder, excel_folder = create_folders_for_pdf(pdf_name)
    
    # Extract data to CSV
    csv_path = extract_data_to_csv(pdf_path, csv_folder)
    
    # Process CSV to DataFrame and create files
    df = process_csv_to_df(csv_path, results_folder, excel_folder)
    return df

@app.route('/')
def index():
    return '''
    <h1>Welcome to the PDF Processing API</h1>
    <p>Use the <a href="/upload">/upload</a> endpoint to upload PDF files.</p>
    <p>Use the <a href="/download/csv">/download/csv</a> endpoint to download the generated CSV file.</p>
    <p>Use the <a href="/download/filename">/download/filename</a> endpoint to download generated PDF reports.</p>
    <p>Use the <a href="/download/excel/filename">/download/excel/filename</a> endpoint to download generated Excel reports.</p>
    '''

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'pdfFile' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['pdfFile']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and file.filename.endswith('.pdf'):
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        
        try:
            df = process_data(file_path, file.filename)
            csv_file = 'data.csv'
            base_name = os.path.splitext(file.filename)[0]
            results_folder = os.path.join(RESULTS_BASE_FOLDER, base_name)
            excel_folder = os.path.join(EXCEL_BASE_FOLDER, base_name)
            pdf_files = [f for f in os.listdir(results_folder) if f.endswith('.pdf')]
            excel_files = [f for f in os.listdir(excel_folder) if f.endswith('.xlsx')]
            return jsonify({'csv_file': csv_file, 'pdf_files': pdf_files, 'excel_files': excel_files})
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return jsonify({'error': 'Invalid file format'}), 400

@app.route('/download/<filename>')
def download_file(filename):
    safe_filename = os.path.basename(filename)  # Prevent directory traversal
    base_name = os.path.splitext(filename)[0]
    results_folder = os.path.join(RESULTS_BASE_FOLDER, base_name)
    if filename.endswith('.pdf'):
        return send_from_directory(results_folder, safe_filename)
    elif filename.endswith('.xlsx'):
        excel_folder = os.path.join(EXCEL_BASE_FOLDER, base_name)
        return send_from_directory(excel_folder, safe_filename)
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/download/csv/<filename>')
def download_csv(filename):
    safe_filename = os.path.basename(filename)  # Prevent directory traversal
    base_name = os.path.splitext(filename)[0]
    csv_folder = os.path.join(CSV_BASE_FOLDER, base_name)

    # Check if the requested CSV file exists
    if filename.endswith('.csv'):
        return send_from_directory(csv_folder, safe_filename)
    
    return jsonify({'error': 'Invalid file type'}), 400


if __name__ == '__main__':
    app.run(debug=True)

