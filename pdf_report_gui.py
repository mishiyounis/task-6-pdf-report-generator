import customtkinter as ctk
from tkinter import filedialog, messagebox, ttk
import os
import csv
import json
from datetime import datetime
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.units import inch

# Set appearance
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

REPORTS_FOLDER = "reports"

class PDFReportGenerator:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("PDF Report Generator - HK Academy")
        self.root.geometry("1100x700")
        self.root.minsize(900, 550)
        
        # Create reports folder
        if not os.path.exists(REPORTS_FOLDER):
            os.makedirs(REPORTS_FOLDER)
        
        # Data storage
        self.data = []
        
        self.setup_ui()
        self.root.mainloop()
    
    def setup_ui(self):
        # Colors
        bg_color = "#f3f3f3"
        accent_color = "#0078d4"
        
        self.root.configure(fg_color=bg_color)
        
        # Main container
        main = ctk.CTkFrame(self.root, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Two columns
        left = ctk.CTkFrame(main, corner_radius=12, fg_color="white")
        left.pack(side="left", fill="both", expand=True, padx=(0, 8))
        
        right = ctk.CTkFrame(main, corner_radius=12, fg_color="white", width=450)
        right.pack(side="right", fill="both", padx=(8, 0))
        right.pack_propagate(False)
        
        # ===== LEFT PANEL - FORM =====
        left_scroll = ctk.CTkScrollableFrame(left, fg_color="transparent")
        left_scroll.pack(fill="both", expand=True)
        
        # Header
        header = ctk.CTkLabel(left_scroll, text="Add New Record", 
                               font=ctk.CTkFont(size=20, weight="bold"),
                               text_color="#202124")
        header.pack(anchor="w", padx=25, pady=(20, 10))
        
        # Report type selector
        type_frame = ctk.CTkFrame(left_scroll, fg_color="transparent")
        type_frame.pack(fill="x", padx=25, pady=10)
        
        ctk.CTkLabel(type_frame, text="Report Type:", font=ctk.CTkFont(size=12)).pack(side="left")
        self.report_type = ctk.CTkComboBox(type_frame, values=["Student Report", "Company Report"],
                                            width=200, corner_radius=8)
        self.report_type.pack(side="left", padx=(20, 0))
        self.report_type.set("Student Report")
        self.report_type.configure(command=self.switch_form)
        
        # Form frame (dynamic)
        self.form_frame = ctk.CTkFrame(left_scroll, fg_color="transparent")
        self.form_frame.pack(fill="both", expand=True, padx=25, pady=10)
        
        # Create initial form
        self.create_student_form()
        
        # Add button
        self.add_btn = ctk.CTkButton(left_scroll, text="+ Add Record", corner_radius=8,
                                      height=40, font=ctk.CTkFont(size=13, weight="bold"),
                                      fg_color="#0078d4", command=self.add_record)
        self.add_btn.pack(fill="x", padx=25, pady=(10, 20))
        
        # ===== RIGHT PANEL - DATA & REPORTS =====
        tab_view = ctk.CTkTabview(right, corner_radius=12)
        tab_view.pack(fill="both", expand=True, padx=12, pady=12)
        
        # Tab 1: Data List
        data_tab = tab_view.add("📋 Data List")
        self.setup_data_tab(data_tab)
        
        # Tab 2: Generate Report
        report_tab = tab_view.add("📄 Generate Report")
        self.setup_report_tab(report_tab)
    
    def switch_form(self, choice):
        # Clear form frame
        for widget in self.form_frame.winfo_children():
            widget.destroy()
        
        if choice == "Student Report":
            self.create_student_form()
        else:
            self.create_company_form()
    
    def create_student_form(self):
        # Student fields
        fields = [
            ("Student Name:", "name_entry"),
            ("Student ID:", "id_entry"),
            ("Email:", "email_entry"),
            ("Course/Department:", "course_entry"),
            ("Marks (e.g., 85/100):", "marks_entry"),
            ("Attendance (%):", "attendance_entry"),
            ("Performance:", "performance_entry")
        ]
        
        self.entries = {}
        
        for i, (label, key) in enumerate(fields):
            row = ctk.CTkFrame(self.form_frame, fg_color="transparent")
            row.pack(fill="x", pady=5)
            
            ctk.CTkLabel(row, text=label, width=140, font=ctk.CTkFont(size=12)).pack(side="left")
            
            if key == "performance_entry":
                entry = ctk.CTkComboBox(row, values=["Excellent", "Good", "Average", "Poor"],
                                         width=250, corner_radius=8)
            else:
                entry = ctk.CTkEntry(row, width=250, corner_radius=8)
            
            entry.pack(side="left", padx=(10, 0))
            self.entries[key] = entry
    
    def create_company_form(self):
        # Company/Employee fields
        fields = [
            ("Employee Name:", "name_entry"),
            ("Employee ID:", "id_entry"),
            ("Email:", "email_entry"),
            ("Role/Designation:", "role_entry"),
            ("Department:", "dept_entry"),
            ("Performance Rating (1-5):", "rating_entry"),
            ("Additional Details:", "details_entry")
        ]
        
        self.entries = {}
        
        for i, (label, key) in enumerate(fields):
            row = ctk.CTkFrame(self.form_frame, fg_color="transparent")
            row.pack(fill="x", pady=5)
            
            ctk.CTkLabel(row, text=label, width=140, font=ctk.CTkFont(size=12)).pack(side="left")
            
            if key == "rating_entry":
                entry = ctk.CTkComboBox(row, values=["1", "2", "3", "4", "5"],
                                         width=250, corner_radius=8)
            else:
                entry = ctk.CTkEntry(row, width=250, corner_radius=8)
            
            entry.pack(side="left", padx=(10, 0))
            self.entries[key] = entry
    
    def add_record(self):
        report_type = self.report_type.get()
        
        if report_type == "Student Report":
            record = {
                'type': 'student',
                'name': self.entries['name_entry'].get(),
                'id': self.entries['id_entry'].get(),
                'email': self.entries['email_entry'].get(),
                'course': self.entries['course_entry'].get(),
                'marks': self.entries['marks_entry'].get(),
                'attendance': self.entries['attendance_entry'].get(),
                'performance': self.entries['performance_entry'].get()
            }
        else:
            record = {
                'type': 'company',
                'name': self.entries['name_entry'].get(),
                'id': self.entries['id_entry'].get(),
                'email': self.entries['email_entry'].get(),
                'role': self.entries['role_entry'].get(),
                'department': self.entries['dept_entry'].get(),
                'performance': self.entries['rating_entry'].get(),
                'details': self.entries['details_entry'].get()
            }
        
        # Validate
        if not record['name'] or not record['id']:
            messagebox.showwarning("Warning", "Name and ID are required!")
            return
        
        self.data.append(record)
        self.update_data_list()
        self.clear_form()
        messagebox.showinfo("Success", f"Record added! Total: {len(self.data)}")
    
    def clear_form(self):
        for key, entry in self.entries.items():
            if isinstance(entry, ctk.CTkEntry):
                entry.delete(0, "end")
            elif isinstance(entry, ctk.CTkComboBox):
                entry.set("")
    
    def setup_data_tab(self, parent):
        # Buttons
        btn_frame = ctk.CTkFrame(parent, fg_color="transparent")
        btn_frame.pack(fill="x", pady=(10, 10))
        
        ctk.CTkButton(btn_frame, text="Load CSV", corner_radius=6, height=32,
                      command=self.load_csv).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Load JSON", corner_radius=6, height=32,
                      command=self.load_json).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Delete Selected", corner_radius=6, height=32,
                      fg_color="#d13438", command=self.delete_record).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Clear All", corner_radius=6, height=32,
                      fg_color="#d13438", command=self.clear_all).pack(side="left", padx=5)
        
        # Treeview
        columns = ("#", "Type", "Name", "ID", "Email", "Details")
        self.data_tree = ttk.Treeview(parent, columns=columns, show="headings", height=14)
        
        for col in columns:
            self.data_tree.heading(col, text=col)
            self.data_tree.column(col, width=80)
        
        self.data_tree.column("#", width=40)
        self.data_tree.column("Type", width=80)
        self.data_tree.column("Name", width=100)
        self.data_tree.column("ID", width=80)
        self.data_tree.column("Email", width=120)
        self.data_tree.column("Details", width=100)
        
        self.data_tree.pack(fill="both", expand=True, pady=(0, 10))
        
        # Scrollbar
        scroll = ttk.Scrollbar(parent, orient="vertical", command=self.data_tree.yview)
        scroll.pack(side="right", fill="y")
        self.data_tree.configure(yscrollcommand=scroll.set)
        
        self.data_count = ctk.CTkLabel(parent, text="0 records", text_color="#5f6368")
        self.data_count.pack(pady=(0, 10))
    
    def setup_report_tab(self, parent):
        # Report type selection
        type_frame = ctk.CTkFrame(parent, fg_color="transparent")
        type_frame.pack(fill="x", pady=(15, 10), padx=10)
        
        ctk.CTkLabel(type_frame, text="Report Type:", font=ctk.CTkFont(size=13)).pack(side="left")
        self.report_type_select = ctk.CTkComboBox(type_frame, 
                                                   values=["Student Report", "Company Report", "All Data"],
                                                   width=200, corner_radius=8)
        self.report_type_select.pack(side="left", padx=(15, 0))
        self.report_type_select.set("Student Report")
        
        # Generate button
        self.generate_btn = ctk.CTkButton(parent, text="Generate PDF Report", corner_radius=8,
                                           height=45, font=ctk.CTkFont(size=14, weight="bold"),
                                           fg_color="#0078d4", command=self.generate_report)
        self.generate_btn.pack(pady=(20, 10), padx=20, fill="x")
        
        # Status
        self.report_status = ctk.CTkLabel(parent, text="Ready to generate report", text_color="#5f6368")
        self.report_status.pack(pady=10)
    
    def update_data_list(self):
        for item in self.data_tree.get_children():
            self.data_tree.delete(item)
        
        for i, record in enumerate(self.data, 1):
            if record.get('type') == 'student':
                details = f"{record.get('course', '')} | {record.get('marks', '')}"
            else:
                details = f"{record.get('role', '')} | {record.get('department', '')}"
            
            self.data_tree.insert("", "end", values=(
                i, 
                "Student" if record.get('type') == 'student' else "Employee",
                record.get('name', ''),
                record.get('id', ''),
                record.get('email', ''),
                details[:30]
            ))
        
        self.data_count.configure(text=f"{len(self.data)} records")
    
    def delete_record(self):
        selected = self.data_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a record to delete")
            return
        
        if messagebox.askyesno("Confirm", "Delete selected record?"):
            indices = [int(self.data_tree.item(item, 'values')[0]) - 1 for item in selected]
            indices.sort(reverse=True)
            for idx in indices:
                if 0 <= idx < len(self.data):
                    self.data.pop(idx)
            self.update_data_list()
            messagebox.showinfo("Success", "Record deleted")
    
    def clear_all(self):
        if self.data and messagebox.askyesno("Confirm", "Delete ALL records?"):
            self.data = []
            self.update_data_list()
            messagebox.showinfo("Success", "All records cleared")
    
    def load_csv(self):
        filename = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not filename:
            return
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Detect type based on columns
                    if 'course' in row or 'marks' in row:
                        row['type'] = 'student'
                    else:
                        row['type'] = 'company'
                    self.data.append(row)
            self.update_data_list()
            messagebox.showinfo("Success", f"Loaded {len(self.data)} records")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def load_json(self):
        filename = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if not filename:
            return
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                loaded = json.load(f)
                self.data.extend(loaded)
            self.update_data_list()
            messagebox.showinfo("Success", f"Loaded {len(self.data)} records")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def generate_report(self):
        if not self.data:
            messagebox.showwarning("Warning", "No data to generate report")
            return
        
        report_type = self.report_type_select.get()
        
        # Filter data
        if report_type == "Student Report":
            filtered = [d for d in self.data if d.get('type') == 'student']
            title = "Student Performance Report"
        elif report_type == "Company Report":
            filtered = [d for d in self.data if d.get('type') == 'company']
            title = "Employee Performance Report"
        else:
            filtered = self.data
            title = "Complete Data Report"
        
        if not filtered:
            messagebox.showwarning("Warning", f"No {report_type} data found")
            return
        
        self.report_status.configure(text="Generating PDF...", text_color="#ff9800")
        self.root.update()
        
        # Create PDF
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{REPORTS_FOLDER}/report_{timestamp}.pdf"
        
        doc = SimpleDocTemplate(filename, pagesize=A4,
                                rightMargin=50, leftMargin=50,
                                topMargin=50, bottomMargin=50)
        
        styles = getSampleStyleSheet()
        story = []
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2c3e50'),
            alignment=1,
            spaceAfter=30
        )
        story.append(Paragraph(title, title_style))
        
        # Date
        date_style = ParagraphStyle(
            'DateStyle',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#7f8c8d'),
            alignment=2,
            spaceAfter=20
        )
        story.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", date_style))
        
        # Summary
        summary_style = ParagraphStyle(
            'SummaryStyle',
            parent=styles['Normal'],
            fontSize=12,
            textColor=colors.HexColor('#34495e'),
            spaceAfter=15
        )
        story.append(Paragraph(f"Total Records: {len(filtered)}", summary_style))
        story.append(Spacer(1, 10))
        
        # Create table data
        if report_type == "Student Report":
            table_data = [["#", "Name", "ID", "Course", "Marks", "Attendance", "Performance"]]
            for i, record in enumerate(filtered, 1):
                table_data.append([
                    str(i),
                    record.get('name', ''),
                    record.get('id', ''),
                    record.get('course', ''),
                    record.get('marks', ''),
                    record.get('attendance', ''),
                    record.get('performance', '')
                ])
        else:
            table_data = [["#", "Name", "ID", "Role", "Department", "Rating", "Details"]]
            for i, record in enumerate(filtered, 1):
                table_data.append([
                    str(i),
                    record.get('name', ''),
                    record.get('id', ''),
                    record.get('role', ''),
                    record.get('department', ''),
                    record.get('performance', ''),
                    record.get('details', '')[:30]
                ])
        
        # Create table
        table = Table(table_data, repeatRows=1)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
        ]))
        
        story.append(table)
        story.append(Spacer(1, 30))
        
        # Footer
        footer_style = ParagraphStyle(
            'FooterStyle',
            parent=styles['Normal'],
            fontSize=9,
            textColor=colors.HexColor('#95a5a6'),
            alignment=1
        )
        story.append(Paragraph("Generated by HK Academy PDF Report Generator", footer_style))
        
        # Build PDF
        doc.build(story)
        
        self.report_status.configure(text=f"PDF saved: {filename}", text_color="#4caf50")
        messagebox.showinfo("Success", f"PDF Report saved to\n{REPORTS_FOLDER}/report_{timestamp}.pdf")
        
        # Open folder
        os.startfile(REPORTS_FOLDER)

if __name__ == "__main__":
    app = PDFReportGenerator()