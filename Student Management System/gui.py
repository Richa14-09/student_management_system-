import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from database import StudentDatabase
import pandas as pd

class StudentManagementGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management System")
        self.root.geometry("1000x600")
        self.root.configure(bg="#f0f0f0")
        
        self.db = StudentDatabase()
        self.selected_student_id = None
        
        self.setup_ui()
        self.refresh_table()
    
    def setup_ui(self):
        """Setup user interface"""
        
        # Top frame for title
        title_frame = tk.Frame(self.root, bg="#2c3e50", height=60)
        title_frame.pack(fill=tk.X)
        
        title_label = tk.Label(
            title_frame, 
            text="Student Management System",
            font=("Arial", 20, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        title_label.pack(pady=10)
        
        # Input frame
        input_frame = ttk.LabelFrame(self.root, text="Student Information", padding=10)
        input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Input fields
        fields = [
            ("Roll No:", "roll_no"),
            ("Name:", "name"),
            ("Email:", "email"),
            ("Phone:", "phone"),
            ("Age:", "age"),
            ("Grade:", "grade"),
            ("Address:", "address")
        ]
        
        self.entries = {}
        for i, (label, field_name) in enumerate(fields):
            tk.Label(input_frame, text=label).grid(row=i//4, column=(i%4)*2, sticky="w", padx=5, pady=5)
            entry = tk.Entry(input_frame, width=20)
            entry.grid(row=i//4, column=(i%4)*2+1, padx=5, pady=5)
            self.entries[field_name] = entry
        
        # Button frame
        button_frame = tk.Frame(self.root, bg="#f0f0f0")
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        buttons = [
            ("Add Student", self.add_student, "#27ae60"),
            ("Update", self.update_student, "#2980b9"),
            ("Delete", self.delete_student, "#e74c3c"),
            ("Clear", self.clear_fields, "#95a5a6"),
            ("Export to Excel", self.export_to_excel, "#f39c12")
        ]
        
        for btn_text, cmd, color in buttons:
            btn = tk.Button(
                button_frame, 
                text=btn_text, 
                command=cmd,
                bg=color,
                fg="white",
                font=("Arial", 10, "bold"),
                width=15
            )
            btn.pack(side=tk.LEFT, padx=5)
        
        # Search frame
        search_frame = tk.Frame(self.root, bg="#f0f0f0")
        search_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(search_frame, text="Search:", bg="#f0f0f0").pack(side=tk.LEFT, padx=5)
        self.search_var = tk.StringVar()
        self.search_var.trace('w', lambda *args: self.search_student())
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side=tk.LEFT, padx=5)
        
        # Table frame
        table_frame = ttk.Frame(self.root)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview table
        columns = ("ID", "Roll No", "Name", "Email", "Phone", "Age", "Grade", "Address")
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            height=15,
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.tree.yview)
        
        self.tree.column("#0", width=0, stretch=tk.NO)
        for col in columns:
            self.tree.column(col, anchor=tk.W, width=100)
            self.tree.heading(col, text=col, anchor=tk.W)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind('<ButtonRelease-1>', self.on_tree_select)
    
    def add_student(self):
        """Add new student"""
        try:
            roll_no = self.entries['roll_no'].get()
            name = self.entries['name'].get()
            email = self.entries['email'].get()
            phone = self.entries['phone'].get()
            age = int(self.entries['age'].get()) if self.entries['age'].get() else 0
            grade = self.entries['grade'].get()
            address = self.entries['address'].get()
            
            if not all([roll_no, name, email, phone]):
                messagebox.showerror("Error", "Please fill all required fields")
                return
            
            success, message = self.db.add_student(
                roll_no, name, email, phone, age, grade, address
            )
            messagebox.showinfo("Success", message) if success else messagebox.showerror("Error", message)
            
            if success:
                self.clear_fields()
                self.refresh_table()
        except ValueError:
            messagebox.showerror("Error", "Age must be a number")
    
    def update_student(self):
        """Update student"""
        if not self.selected_student_id:
            messagebox.showerror("Error", "Select a student to update")
            return
        
        try:
            roll_no = self.entries['roll_no'].get()
            name = self.entries['name'].get()
            email = self.entries['email'].get()
            phone = self.entries['phone'].get()
            age = int(self.entries['age'].get()) if self.entries['age'].get() else 0
            grade = self.entries['grade'].get()
            address = self.entries['address'].get()
            
            success, message = self.db.update_student(
                self.selected_student_id, roll_no, name, email, phone, age, grade, address
            )
            messagebox.showinfo("Success", message) if success else messagebox.showerror("Error", message)
            
            if success:
                self.clear_fields()
                self.refresh_table()
        except ValueError:
            messagebox.showerror("Error", "Age must be a number")
    
    def delete_student(self):
        """Delete student"""
        if not self.selected_student_id:
            messagebox.showerror("Error", "Select a student to delete")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure?"):
            success, message = self.db.delete_student(self.selected_student_id)
            messagebox.showinfo("Success", message) if success else messagebox.showerror("Error", message)
            
            if success:
                self.clear_fields()
                self.refresh_table()
    
    def clear_fields(self):
        """Clear input fields"""
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.selected_student_id = None
    
    def on_tree_select(self, event):
        """Handle table selection"""
        selection = self.tree.selection()
        if selection:
            item = selection[0]
            values = self.tree.item(item)['values']
            
            self.selected_student_id = values[0]
            self.entries['roll_no'].delete(0, tk.END)
            self.entries['roll_no'].insert(0, values[1])
            self.entries['name'].delete(0, tk.END)
            self.entries['name'].insert(0, values[2])
            self.entries['email'].delete(0, tk.END)
            self.entries['email'].insert(0, values[3])
            self.entries['phone'].delete(0, tk.END)
            self.entries['phone'].insert(0, values[4])
            self.entries['age'].delete(0, tk.END)
            self.entries['age'].insert(0, values[5])
            self.entries['grade'].delete(0, tk.END)
            self.entries['grade'].insert(0, values[6])
            self.entries['address'].delete(0, tk.END)
            self.entries['address'].insert(0, values[7])
    
    def refresh_table(self):
        """Refresh table with all students"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        students = self.db.get_all_students()
        for student in students:
            self.tree.insert('', 'end', values=student)
    
    def search_student(self):
        """Search students"""
        search_term = self.search_var.get()
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if search_term:
            students = self.db.search_student(search_term)
        else:
            students = self.db.get_all_students()
        
        for student in students:
            self.tree.insert('', 'end', values=student)
    
    def export_to_excel(self):
        """Export data to Excel"""
        try:
            students = self.db.get_all_students()
            df = pd.DataFrame(students, columns=[
                'ID', 'Roll No', 'Name', 'Email', 'Phone', 'Age', 'Grade', 'Address', 'Created At'
            ])
            
            file_path = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
            )
            
            if file_path:
                df.to_excel(file_path, index=False)
                messagebox.showinfo("Success", f"Data exported to {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Export failed: {e}")
    
    def on_closing(self):
        """Handle window closing"""
        self.db.close()
        self.root.destroy()