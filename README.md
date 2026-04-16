                                                    :PDF Report Generator:

A professional GUI application to generate PDF reports for student and company data with formatted tables and professional layout.

> What is this project?

This is a Python-based desktop application that allows users to create professional PDF reports from student or employee data. Users can add records manually, load data from CSV or JSON files, and generate beautifully formatted PDF reports with tables, headers, timestamps, and summaries. The application features a modern  graphical interface built with CustomTkinter and uses ReportLab for PDF generation.

> Key Features

- Data Management
Users can add student or employee records through an easy-to-use form. For students, the application collects name, ID, email, course, marks, attendance percentage, and performance rating. For employees, it collects name, ID, email, role, department, performance rating from 1 to 5, and additional details. All added records are displayed in a table view where users can delete individual records or clear all data at once.

- File Import
The application supports loading data from CSV and JSON files. This is useful when users already have data in spreadsheets or other formats. The system automatically detects whether the data is student or company records based on the column names.

- PDF Report Generation
Users can generate three types of reports: Student Report (only student data), Company Report (only employee data), or Complete Report (all data combined). Each PDF report includes a professional title, generation date and time, total record count, a formatted table with all data, and a footer. The tables have colored headers, grid lines, and proper alignment for a polished look.

> Technical Requirements

- Python 3.7 or higher
- CustomTkinter library for GUI
- ReportLab library for PDF generation

> Installation

Install the required libraries using these commands:

pip install customtkinter
pip install reportlab