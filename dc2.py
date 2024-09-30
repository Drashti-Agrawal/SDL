# import os
# import csv
# import pdfplumber
# import pandas as pd
# from flask import Flask, request, jsonify, send_from_directory
# from flask_cors import CORS
# from reportlab.lib.pagesizes import letter
# from reportlab.lib import colors
# from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

# app = Flask(__name__)
# CORS(app)  # Enable CORS for all routes

# UPLOAD_FOLDER = 'uploads'
# RESULTS_BASE_FOLDER = 'results'
# CSV_BASE_FOLDER = 'csv'
# EXCEL_BASE_FOLDER = 'excel'

# # Create necessary folders for results
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
#                     for i, row in enumerate(table):
#                         # Ignore header and note rows (1st to 4th rows), only process from row 5 onwards
#                         if i >= 4:
#                             writer.writerow(row)
#     return csv_path

# def create_files(df, results_folder, excel_folder):
#     if 'S.No.' not in df.columns:
#         df.insert(0, 'S.No.', range(1, len(df) + 1))  # Add serial number starting from 1
    
#     subject_groups = {}
#     base_columns = ['S.No.', 'Enrollment No.', 'Name']
    
#     for col in df.columns:
#         if col not in base_columns:
#             subject_name = col.split(' ')[0]
#             if subject_name not in subject_groups:
#                 subject_groups[subject_name] = base_columns.copy()
#             subject_groups[subject_name].append(col)
    
#     for subject, columns in subject_groups.items():
#         subject_name = subject.strip()
        
#         subject_df = df[columns].copy()
        
#         # Create PDF file for the subject
#         pdf_path = os.path.join(results_folder, f"{subject_name}_attendance_report.pdf")
#         pdf = SimpleDocTemplate(pdf_path, pagesize=letter)
#         elements = []
        
#         data = [columns]
#         for _, row in subject_df.iterrows():
#             data.append(list(row.values))
            
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

#         # Create Excel file for the subject
#         excel_path = os.path.join(excel_folder, f"{subject_name}_attendance_report.xlsx")
#         subject_df.to_excel(excel_path, index=False)

# def process_csv_to_df(csv_path, results_folder, excel_folder):
#     df = pd.read_csv(csv_path)
    
#     if df.empty:
#         raise ValueError("CSV file is empty or could not be read.")
    
#     columns = df.columns
#     name_col = None
#     enroll_col = None
    
#     for col in columns:
#         if 'Name' in col:
#             name_col = col
#         if 'Enrollment' in col or 'Roll' in col:
#             enroll_col = col
    
#     if not name_col or not enroll_col:
#         raise ValueError("Required columns (Name, Enrollment No./Roll No.) not found in the CSV.")
    
#     df.rename(columns={name_col: 'Name', enroll_col: 'Enrollment No.'}, inplace=True)
    
#     if 'S.No.' not in df.columns:
#         df.insert(0, 'S.No.', range(1, len(df) + 1))
    
#     create_files(df, results_folder, excel_folder)
    
#     return df

# def process_data(pdf_path, pdf_name):
#     results_folder, csv_folder, excel_folder = create_folders_for_pdf(pdf_name)
#     csv_path = extract_data_to_csv(pdf_path, csv_folder)
#     df = process_csv_to_df(csv_path, results_folder, excel_folder)
#     return df

# @app.route('/')
# def index():
#     return '''
#     <h1>Welcome to the PDF Attendance Processing API</h1>
#     <p>Use the <a href="/upload">/upload</a> endpoint to upload PDF files.</p>
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
#             base_name = os.path.splitext(file.filename)[0]
#             results_folder = os.path.join(RESULTS_BASE_FOLDER, base_name)
#             excel_folder = os.path.join(EXCEL_BASE_FOLDER, base_name)
            
#             pdf_files = [f for f in os.listdir(results_folder) if f.endswith('.pdf')]
#             excel_files = [f for f in os.listdir(excel_folder) if f.endswith('.xlsx')]

#             return jsonify({'pdf_files': pdf_files, 'excel_files': excel_files})
#         except ValueError as e:
#             return jsonify({'error': str(e)}), 400
#         except Exception as e:
#             return jsonify({'error': str(e)}), 500
    
#     return jsonify({'error': 'Invalid file format'}), 400

# if __name__ == '_main_':
#     app.run(debug=True)

# from flask import Flask, request, jsonify, send_from_directory
# from flask_cors import CORS
# import os
# import pdfplumber
# import pandas as pd
# from reportlab.lib.pagesizes import letter
# from reportlab.lib import colors
# from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

# app = Flask(__name__)
# CORS(app)
# UPLOAD_FOLDER = 'uploads'
# RESULTS_FOLDER = 'results'
# CSV_FOLDER = 'csv'
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# os.makedirs(RESULTS_FOLDER, exist_ok=True)
# os.makedirs(CSV_FOLDER, exist_ok=True)

# def extract_data_to_csv(pdf_path):
#     csv_path = os.path.join(CSV_FOLDER, 'data.csv')
#     with pdfplumber.open(pdf_path) as pdf:
#         with open(csv_path, 'w', newline='') as csv_file:
#             for page in pdf.pages:
#                 table = page.extract_table()
#                 if table:
#                     writer = csv.writer(csv_file)
#                     for row in table:
#                         writer.writerow(row)
#     return csv_path

# def process_csv_to_df(csv_path):
#     df = pd.read_csv(csv_path)
    
#     if df.empty:
#         raise ValueError("CSV file is empty or could not be read.")
    
#     # Extract the columns
#     df.columns = ['S.No.', 'Enrollment No.', 'Name'] + [f'Subject {i+1}' for i in range(len(df.columns) - 3)]
#     create_pdfs(df)
#     return df

# def create_pdfs(df):
#     # Assume columns are: S.No., Enrollment No., Name, and then subjects
#     subject_columns = df.columns[3:]  # Starting from the 4th column (index 3)
    
#     for subject in subject_columns:
#         output_path = os.path.join(RESULTS_FOLDER, f"{subject}_report.pdf")
#         pdf = SimpleDocTemplate(output_path, pagesize=letter)
#         elements = []
#         data = [['S.No.', 'Enrollment No.', 'Name', 'Marks of ' + subject]]
        
#         for _, row in df.iterrows():
#             s_no = row['S.No.']
#             enrollment_no = row['Enrollment No.']
#             name = row['Name']
#             marks = row.get(subject, 'N/A')
#             data.append([s_no, enrollment_no, name, marks])
        
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

# # @app.route('/')
# # def index():
# #     return '''
# #     <h1>Welcome to the PDF Processing API</h1>
# #     <p>Use the <a href="/upload">/upload</a> endpoint to upload PDF files.</p>
# #     <p>Use the <a href="/download/filename">/download/filename</a> endpoint to download generated PDF reports.</p>
# #     <p>Use the <a href="/download/csv">/download/csv</a> endpoint to download the generated CSV file.</p>
# #     '''

# # @cross_origin()
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
#             csv_path = extract_data_to_csv(file_path)
#             df = process_csv_to_df(csv_path)
#             files = [f for f in os.listdir(RESULTS_FOLDER) if f.endswith('.pdf')]
#             return jsonify({'files': files})
#         except ValueError as e:
#             return jsonify({'error': str(e)}), 400
#         except Exception as e:
#             return jsonify({'error': str(e)}), 500
    
#     return jsonify({'error': 'Invalid file format'}), 400

# @app.route('/download/<filename>')
# def download_file(filename):
#     safe_filename = os.path.basename(filename)  # Prevent directory traversal
#     return send_from_directory(RESULTS_FOLDER, safe_filename)

# @app.route('/download/csv')
# def download_csv():
#     csv_path = os.path.join(CSV_FOLDER, 'data.csv')
#     if os.path.exists(csv_path):
#         return send_from_directory(CSV_FOLDER, 'data.csv')
#     return jsonify({'error': 'CSV file not found'}), 404

# if __name__ == '__main__':
#     app.run(debug=True)

# from flask import Flask, request, jsonify, send_from_directory, render_template, redirect, url_for
# from flask_cors import CORS
# import os
# import csv
# import pdfplumber
# import pandas as pd
# from reportlab.lib.pagesizes import letter
# from reportlab.lib import colors
# from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

# app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')  # Set your desired upload folder path

# CORS(app)
# os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

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
#                     # Process table to filter out headers and construct proper rows
#                     processed_rows = process_table_rows(table)
#                     writer.writerows(processed_rows)
#     return csv_path

# def process_table_rows(table):
#     processed_rows = []
#     headers = []
#     subjects = []
    
#     for row in table:
#         # Remove rows with single column or empty leading cells
#         if len(row) == 1 or all(cell == '' for cell in row):
#             continue

#         # Check if the row can be a header
#         if any(cell.lower() in ['total classes', 'percentage', 'total present'] for cell in row):
#             headers = row
#             continue

#         # If we have headers, collect subject information
#         if headers and any(cell for cell in row):  # Row contains some data
#             subject_name = row[0]  # Assuming subject name is in the first column
#             subjects.append((subject_name, headers))
#             processed_rows.append(row)
    
#     return processed_rows

# def create_files(df, results_folder, excel_folder):
#     # Create a PDF and Excel file for each subject
#     subjects = df['Subject'].unique()
    
#     for subject in subjects:
#         subject_df = df[df['Subject'] == subject]
        
#         if subject_df.empty:
#             continue
        
#         # Create PDF path for the subject
#         pdf_path = os.path.join(results_folder, f"{subject}_attendance_report.pdf")
#         pdf = SimpleDocTemplate(pdf_path, pagesize=letter)
#         elements = []
        
#         # Create table data
#         data = [list(subject_df.columns)]
#         for index, row in subject_df.iterrows():
#             data.append(row.tolist())

#         # Create table
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
#         excel_path = os.path.join(excel_folder, f"{subject}_attendance_report.xlsx")
#         subject_df.to_excel(excel_path, index=False)

# def process_csv_to_df(csv_path, results_folder, excel_folder):
#     df = pd.read_csv(csv_path)
    
#     if df.empty:
#         raise ValueError("CSV file is empty or could not be read.")

#     # Assume the first column holds the subject names
#     df['Subject'] = df.iloc[:, 0]  # Adjust as necessary to match your data structure
#     create_files(df, results_folder, excel_folder)

#     return df

# def process_data(pdf_path, pdf_name):
#     results_folder, csv_folder, excel_folder = create_folders_for_pdf(pdf_name)
    
#     csv_path = extract_data_to_csv(pdf_path, csv_folder)
    
#     df = process_csv_to_df(csv_path, results_folder, excel_folder)
#     return df

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/upload', methods=['POST'])
# def upload_file():
#     if 'pdfFile' not in request.files:
#         return "No file part", 400  # Specify HTTP status code
    
#     file = request.files['pdfFile']  # Make sure this matches the input name
    
#     if file.filename == '':
#         return "No selected file", 400  # Specify HTTP status code
    
#     if file and file.filename.endswith('.pdf'):
#         file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
#         file.save(file_path)  # Save the file to the specified upload folder
#         return redirect(url_for('index'))  # Redirect back to the index page
    
#     return "Invalid file type", 400  # Specify HTTP status code

    
# # @app.route('/upload', methods=['POST'])
# # def upload_file():
# #     if 'pdf_file' not in request.files:
# #         print("No file part")
# #         return redirect(request.url)

# #     file = request.files['pdf_file']
    
# #     if file.filename == '':
# #         print("No selected file")
# #         return redirect(request.url)

# #     if file and file.filename.endswith('.pdf'):
# #         file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
# #         file.save(file_path)
# #         print(f"File saved at: {file_path}")
        
# #         # Call the function to process the PDF
# #         csv_file_path = extract_data_to_csv(file_path, 'csv')
# #         print(f"CSV file created at: {csv_file_path}")
        
# #         # Redirect or return success message
# #         return redirect(url_for('success'))

# #     return "Invalid file type"
# # @app.route('/success')
# # def success():
# #     return "File uploaded and processed successfully!"

# @app.route('/download/<filename>')
# def download_file(filename):
#     safe_filename = os.path.basename(filename)
#     base_name = os.path.splitext(filename)[0]
#     results_folder = os.path.join(RESULTS_BASE_FOLDER, base_name)
#     if filename.endswith('.pdf'):
#         return send_from_directory(results_folder, safe_filename)
#     elif filename.endswith('.xlsx'):
#         excel_folder = os.path.join(EXCEL_BASE_FOLDER, base_name)
#         return send_from_directory(excel_folder, safe_filename)
#     return jsonify({'error': 'Invalid file type'}), 400

# @app.route('/download/csv')
# def download_csv():
#     latest_folder = max([os.path.join(CSV_BASE_FOLDER, d) for d in os.listdir(CSV_BASE_FOLDER)], key=os.path.getctime)
#     csv_path = os.path.join(latest_folder, 'data.csv')
#     if os.path.exists(csv_path):
#         return send_from_directory(latest_folder, 'data.csv')
#     return jsonify({'error': 'CSV file not found'}), 404

# @app.route('/download/excel/<filename>')
# def download_excel(filename):
#     safe_filename = os.path.basename(filename)
#     base_name = os.path.splitext(filename)[0]
#     excel_folder = os.path.join(EXCEL_BASE_FOLDER, base_name)
#     return send_from_directory(excel_folder, safe_filename)

# if __name__ == '__main__':
#     app.run(debug=True)
