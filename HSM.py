import tkinter as tk
from tkinter import ttk, messagebox
import json
import os


class HospitalManagementSystemApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hospital Management System")
        self.root.geometry("900x600")
        self.primary_color = "#E82561"
        self.secondary_color = "#4DA1A9"
        self.root.configure(bg=self.secondary_color)

        self.doctors = []  
        self.patients = []  
        self.waiting_list = []  

        self.load_data()
        self.reset_doctor_status()
        self.setup_interface()

    def load_data(self):
        """Load doctors and patients data from JSON files."""
        try:
            if os.path.exists("doctors.json"):
                with open("doctors.json", "r") as file:
                    self.doctors = json.load(file)
            else:
                raise FileNotFoundError
        except (FileNotFoundError, json.JSONDecodeError):
            self.doctors = [
                {"ID": "D001", "Name": "Dr. John Doe", "Specialization": "Cardiology", "Status": "Available"},
                {"ID": "D002", "Name": "Dr. Jane Smith", "Specialization": "Neurology", "Status": "Available"},
                {"ID": "D003", "Name": "Dr. Mark Johnson", "Specialization": "Orthopedics", "Status": "Available"},
            ]

        try:
            if os.path.exists("patients.json"):
                with open("patients.json", "r") as file:
                    self.patients = json.load(file)
            else:
                raise FileNotFoundError
        except (FileNotFoundError, json.JSONDecodeError):
            self.patients = []

    def save_data(self):
        """Save doctors and patients data to JSON files."""
        with open("doctors.json", "w") as file:
            json.dump(self.doctors, file, indent=4)
        with open("patients.json", "w") as file:
            json.dump(self.patients, file, indent=4)

    def reset_doctor_status(self):
        """Reset all doctors' statuses to 'Available'."""
        for doctor in self.doctors:
            doctor["Status"] = "Available"

    def setup_interface(self):
        heading_frame = tk.Frame(self.root, bg=self.secondary_color, pady=10)
        heading_frame.pack(fill="x")
        heading_label = tk.Label(
            heading_frame,
            text="Hospital Management System",
            font=("Arial", 24, "bold"),
            bg=self.secondary_color,
            fg=self.primary_color,
        )
        heading_label.pack()

        self.tab_control = ttk.Notebook(self.root)

        self.patient_tab = ttk.Frame(self.tab_control)
        self.doctor_tab = ttk.Frame(self.tab_control)

        self.tab_control.add(self.patient_tab, text="Manage Patients")
        self.tab_control.add(self.doctor_tab, text="Manage Doctors")
        self.tab_control.pack(expand=1, fill="both")

        self.setup_patient_tab()
        self.setup_doctor_tab()

    def setup_patient_tab(self):
        form_frame = ttk.Frame(self.patient_tab, padding=10)
        form_frame.pack(fill="x", pady=5)

        ttk.Label(form_frame, text="Patient ID:", foreground=self.primary_color).grid(row=0, column=0, padx=5, pady=5)
        self.patient_id_entry = ttk.Entry(form_frame)
        self.patient_id_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Name:", foreground=self.primary_color).grid(row=1, column=0, padx=5, pady=5)
        self.patient_name_entry = ttk.Entry(form_frame)
        self.patient_name_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Age:", foreground=self.primary_color).grid(row=2, column=0, padx=5, pady=5)
        self.patient_age_entry = ttk.Entry(form_frame)
        self.patient_age_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Ailment:", foreground=self.primary_color).grid(row=3, column=0, padx=5, pady=5)
        self.patient_ailment_entry = ttk.Entry(form_frame)
        self.patient_ailment_entry.grid(row=3, column=1, padx=5, pady=5)

        add_patient_button = ttk.Button(form_frame, text="Add Patient", command=self.add_patient)
        add_patient_button.grid(row=4, column=0, pady=10)

        edit_patient_button = ttk.Button(form_frame, text="Edit Patient", command=self.edit_selected_patient)
        edit_patient_button.grid(row=4, column=1, pady=10)

        delete_patient_button = ttk.Button(form_frame, text="Delete Patient", command=self.delete_selected_patient)
        delete_patient_button.grid(row=4, column=2, pady=10)

        self.patient_table = ttk.Treeview(
            self.patient_tab,
            columns=("ID", "Name", "Age", "Ailment", "Doctor"),
            show="headings",
            height=12,
        )
        self.patient_table.heading("ID", text="ID")
        self.patient_table.heading("Name", text="Name")
        self.patient_table.heading("Age", text="Age")
        self.patient_table.heading("Ailment", text="Ailment")
        self.patient_table.heading("Doctor", text="Assigned Doctor")
        self.patient_table.pack(expand=1, fill="both", pady=10)

        self.update_patient_table()

    def setup_doctor_tab(self):
        form_frame = ttk.Frame(self.doctor_tab, padding=10)
        form_frame.pack(fill="x", pady=5)

        ttk.Label(form_frame, text="Doctor ID:", foreground=self.primary_color).grid(row=0, column=0, padx=5, pady=5)
        self.doctor_id_entry = ttk.Entry(form_frame)
        self.doctor_id_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Name:", foreground=self.primary_color).grid(row=1, column=0, padx=5, pady=5)
        self.doctor_name_entry = ttk.Entry(form_frame)
        self.doctor_name_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Specialization:", foreground=self.primary_color).grid(row=2, column=0, padx=5, pady=5)
        self.doctor_specialization_entry = ttk.Entry(form_frame)
        self.doctor_specialization_entry.grid(row=2, column=1, padx=5, pady=5)

        add_doctor_button = ttk.Button(form_frame, text="Add Doctor", command=self.add_doctor)
        add_doctor_button.grid(row=3, column=0, pady=10)

        self.doctor_table = ttk.Treeview(
            self.doctor_tab,
            columns=("ID", "Name", "Specialization", "Status"),
            show="headings",
            height=12,
        )
        self.doctor_table.heading("ID", text="ID")
        self.doctor_table.heading("Name", text="Name")
        self.doctor_table.heading("Specialization", text="Specialization")
        self.doctor_table.heading("Status", text="Status")
        self.doctor_table.pack(expand=1, fill="both", pady=10)

        self.update_doctor_table()



    def add_patient(self):
        patient_id = self.patient_id_entry.get()
        patient_name = self.patient_name_entry.get()
        patient_age = self.patient_age_entry.get()
        patient_ailment = self.patient_ailment_entry.get()

        if patient_id and patient_name and patient_age and patient_ailment:
            assigned_doctor = None
            for doctor in self.doctors:
                if doctor["Status"] == "Available" and doctor["Specialization"].lower() in patient_ailment.lower():
                    assigned_doctor = doctor["Name"]
                    doctor["Status"] = "Assigned"
                    break

            if not assigned_doctor:
                self.waiting_list.append({
                    "ID": patient_id,
                    "Name": patient_name,
                    "Age": patient_age,
                    "Ailment": patient_ailment,
                })
                messagebox.showinfo("Waiting List", f"Patient {patient_name} added to waiting list.")
                assigned_doctor = "Waiting List"

            self.patients.append({
                "ID": patient_id,
                "Name": patient_name,
                "Age": patient_age,
                "Ailment": patient_ailment,
                "Doctor": assigned_doctor,
            })
            self.update_patient_table()
            self.update_doctor_table()
            self.save_data()

            self.patient_id_entry.delete(0, "end")
            self.patient_name_entry.delete(0, "end")
            self.patient_age_entry.delete(0, "end")
            self.patient_ailment_entry.delete(0, "end")
        else:
            messagebox.showwarning("Input Error", "Please fill all fields!")

    def add_doctor(self):
        doctor_id = self.doctor_id_entry.get()
        doctor_name = self.doctor_name_entry.get()
        doctor_specialization = self.doctor_specialization_entry.get()

        if doctor_id and doctor_name and doctor_specialization:
            self.doctors.append({
                "ID": doctor_id,
                "Name": doctor_name,
                "Specialization": doctor_specialization,
                "Status": "Available",
            })
            self.update_doctor_table()
            self.save_data()

            self.doctor_id_entry.delete(0, "end")
            self.doctor_name_entry.delete(0, "end")
            self.doctor_specialization_entry.delete(0, "end")
        else:
            messagebox.showwarning("Input Error", "Please fill all fields!")

    def edit_selected_patient(self):
        selected = self.patient_table.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a patient to edit.")
            return

        patient_id = self.patient_table.item(selected, "values")[0]
        for patient in self.patients:
            if patient["ID"] == patient_id:
                patient["Name"] = self.patient_name_entry.get()
                patient["Age"] = self.patient_age_entry.get()
                patient["Ailment"] = self.patient_ailment_entry.get()
                self.update_patient_table()
                self.save_data()
                messagebox.showinfo("Success", "Patient details updated.")
                return
        messagebox.showwarning("Not Found", "Selected patient not found.")

    def delete_selected_patient(self):
        selected = self.patient_table.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a patient to delete.")
            return

        patient_id = self.patient_table.item(selected, "values")[0]
        self.patients = [p for p in self.patients if p["ID"] != patient_id]
        self.update_patient_table()
        self.save_data()
        messagebox.showinfo("Success", "Patient deleted successfully.")

    def update_patient_table(self):
        for row in self.patient_table.get_children():
            self.patient_table.delete(row)
        for patient in self.patients:
            self.patient_table.insert(
                "", "end", values=(patient["ID"], patient["Name"], patient["Age"], patient["Ailment"], patient["Doctor"])
            )

    def update_doctor_table(self):
        for row in self.doctor_table.get_children():
            self.doctor_table.delete(row)
        for doctor in self.doctors:
            self.doctor_table.insert("", "end", values=(doctor["ID"], doctor["Name"], doctor["Specialization"], doctor["Status"]))


if __name__ == "__main__":
    root = tk.Tk()
    app = HospitalManagementSystemApp(root)
    root.mainloop()
