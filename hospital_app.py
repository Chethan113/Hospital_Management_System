import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
import csv

class HospitalManagementSystemApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hospital Management System")
        self.root.geometry("1000x600")
        self.primary_color = "#E82561"
        self.secondary_color = "#f0f0f0"
        self.root.configure(bg=self.secondary_color)

        self.doctors = []
        self.patients = []
        self.waiting_list = []

        self.load_data()
        self.reset_doctor_status()
        self.setup_interface()

        # Save data on close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def load_data(self):
        try:
            if os.path.exists("doctors.json"):
                with open("doctors.json", "r") as f:
                    self.doctors = json.load(f)
        except:
            self.doctors = []

        try:
            if os.path.exists("patients.json"):
                with open("patients.json", "r") as f:
                    self.patients = json.load(f)
        except:
            self.patients = []

    def save_data(self):
        with open("doctors.json", "w") as f:
            json.dump(self.doctors, f, indent=4)
        with open("patients.json", "w") as f:
            json.dump(self.patients, f, indent=4)

    def reset_doctor_status(self):
        for doctor in self.doctors:
            doctor["Status"] = "Available"

    def setup_interface(self):
        # Heading
        heading = tk.Label(self.root, text="🏥 Hospital Management System",
                           font=("Arial", 20, "bold"), bg=self.secondary_color, fg=self.primary_color)
        heading.pack(pady=10)

        # Tabs
        self.tab_control = ttk.Notebook(self.root)
        self.patient_tab = ttk.Frame(self.tab_control)
        self.doctor_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.patient_tab, text="Manage Patients")
        self.tab_control.add(self.doctor_tab, text="Manage Doctors")
        self.tab_control.pack(expand=1, fill="both")

        self.status_label = tk.Label(self.root, text="", bg=self.secondary_color, fg="green", anchor="w")
        self.status_label.pack(fill="x")

        self.setup_patient_tab()
        self.setup_doctor_tab()

    def setup_patient_tab(self):
        form = ttk.Frame(self.patient_tab, padding=10)
        form.pack(fill="x")

        labels = ["ID", "Name", "Age", "Ailment"]
        self.patient_entries = {}
        for i, label in enumerate(labels):
            ttk.Label(form, text=label).grid(row=i, column=0, padx=5, pady=5)
            entry = ttk.Entry(form)
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.patient_entries[label.lower()] = entry

        ttk.Button(form, text="Add", command=self.add_patient).grid(row=0, column=2)
        ttk.Button(form, text="Edit", command=self.edit_selected_patient).grid(row=1, column=2)
        ttk.Button(form, text="Delete", command=self.delete_selected_patient).grid(row=2, column=2)
        ttk.Button(form, text="Export CSV", command=self.export_patients).grid(row=3, column=2)

        self.patient_table = ttk.Treeview(self.patient_tab, columns=("ID", "Name", "Age", "Ailment", "Doctor"), show="headings")
        for col in self.patient_table["columns"]:
            self.patient_table.heading(col, text=col)
        self.patient_table.pack(expand=1, fill="both", pady=10)
        self.update_patient_table()

    def setup_doctor_tab(self):
        form = ttk.Frame(self.doctor_tab, padding=10)
        form.pack(fill="x")

        labels = ["ID", "Name", "Specialization"]
        self.doctor_entries = {}
        for i, label in enumerate(labels):
            ttk.Label(form, text=label).grid(row=i, column=0, padx=5, pady=5)
            entry = ttk.Entry(form)
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.doctor_entries[label.lower()] = entry

        ttk.Button(form, text="Add", command=self.add_doctor).grid(row=0, column=2)
        ttk.Button(form, text="Edit", command=self.edit_selected_doctor).grid(row=1, column=2)
        ttk.Button(form, text="Delete", command=self.delete_selected_doctor).grid(row=2, column=2)
        ttk.Button(form, text="Reassign Waiting", command=self.reassign_waiting_list).grid(row=3, column=2)

        self.doctor_table = ttk.Treeview(self.doctor_tab, columns=("ID", "Name", "Specialization", "Status"), show="headings")
        for col in self.doctor_table["columns"]:
            self.doctor_table.heading(col, text=col)
        self.doctor_table.pack(expand=1, fill="both", pady=10)
        self.update_doctor_table()

    # Core Patient Logic
    def add_patient(self):
        pid = self.patient_entries["id"].get()
        name = self.patient_entries["name"].get()
        age = self.patient_entries["age"].get()
        ailment = self.patient_entries["ailment"].get()

        if not (pid and name and age and ailment):
            self.status_label.config(text="Please fill all patient fields", fg="red")
            return

        for p in self.patients:
            if p["ID"] == pid:
                self.status_label.config(text="Duplicate Patient ID", fg="red")
                return

        assigned = None
        for doc in self.doctors:
            if doc["Status"] == "Available" and doc["Specialization"].lower() in ailment.lower():
                assigned = doc["Name"]
                doc["Status"] = "Assigned"
                break

        if not assigned:
            assigned = "Waiting List"
            self.waiting_list.append({"ID": pid, "Name": name, "Age": age, "Ailment": ailment})

        self.patients.append({
            "ID": pid, "Name": name, "Age": age, "Ailment": ailment, "Doctor": assigned
        })
        self.update_patient_table()
        self.update_doctor_table()
        self.save_data()
        self.status_label.config(text="Patient added successfully", fg="green")
        for entry in self.patient_entries.values():
            entry.delete(0, "end")

    def edit_selected_patient(self):
        selected = self.patient_table.selection()
        if not selected:
            self.status_label.config(text="Select a patient to edit", fg="red")
            return

        pid = self.patient_table.item(selected)["values"][0]
        for patient in self.patients:
            if patient["ID"] == pid:
                patient["Name"] = self.patient_entries["name"].get()
                patient["Age"] = self.patient_entries["age"].get()
                patient["Ailment"] = self.patient_entries["ailment"].get()
                break
        self.update_patient_table()
        self.save_data()
        self.status_label.config(text="Patient edited", fg="green")

    def delete_selected_patient(self):
        selected = self.patient_table.selection()
        if not selected:
            self.status_label.config(text="Select a patient to delete", fg="red")
            return
        pid = self.patient_table.item(selected)["values"][0]
        self.patients = [p for p in self.patients if p["ID"] != pid]
        self.update_patient_table()
        self.save_data()
        self.status_label.config(text="Patient deleted", fg="green")

    def export_patients(self):
        path = filedialog.asksaveasfilename(defaultextension=".csv")
        if path:
            with open(path, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["ID", "Name", "Age", "Ailment", "Doctor"])
                for p in self.patients:
                    writer.writerow([p["ID"], p["Name"], p["Age"], p["Ailment"], p["Doctor"]])
            self.status_label.config(text="Patients exported to CSV", fg="green")

    # Doctor Logic
    def add_doctor(self):
        did = self.doctor_entries["id"].get()
        name = self.doctor_entries["name"].get()
        spec = self.doctor_entries["specialization"].get()

        if not (did and name and spec):
            self.status_label.config(text="Fill all doctor fields", fg="red")
            return
        for d in self.doctors:
            if d["ID"] == did:
                self.status_label.config(text="Duplicate Doctor ID", fg="red")
                return
        self.doctors.append({"ID": did, "Name": name, "Specialization": spec, "Status": "Available"})
        self.update_doctor_table()
        self.save_data()
        self.status_label.config(text="Doctor added", fg="green")
        for entry in self.doctor_entries.values():
            entry.delete(0, "end")

    def edit_selected_doctor(self):
        selected = self.doctor_table.selection()
        if not selected:
            self.status_label.config(text="Select a doctor to edit", fg="red")
            return
        did = self.doctor_table.item(selected)["values"][0]
        for doc in self.doctors:
            if doc["ID"] == did:
                doc["Name"] = self.doctor_entries["name"].get()
                doc["Specialization"] = self.doctor_entries["specialization"].get()
                break
        self.update_doctor_table()
        self.save_data()
        self.status_label.config(text="Doctor edited", fg="green")

    def delete_selected_doctor(self):
        selected = self.doctor_table.selection()
        if not selected:
            self.status_label.config(text="Select a doctor to delete", fg="red")
            return
        did = self.doctor_table.item(selected)["values"][0]
        self.doctors = [d for d in self.doctors if d["ID"] != did]
        self.update_doctor_table()
        self.save_data()
        self.status_label.config(text="Doctor deleted", fg="green")

    def reassign_waiting_list(self):
        reassigned = []
        for patient in self.waiting_list[:]:
            for doc in self.doctors:
                if doc["Status"] == "Available" and doc["Specialization"].lower() in patient["Ailment"].lower():
                    doc["Status"] = "Assigned"
                    patient["Doctor"] = doc["Name"]
                    self.patients.append(patient)
                    reassigned.append(patient)
                    self.waiting_list.remove(patient)
                    break
        if reassigned:
            self.status_label.config(text=f"{len(reassigned)} patient(s) reassigned", fg="green")
            self.update_patient_table()
            self.update_doctor_table()
            self.save_data()
        else:
            self.status_label.config(text="No reassignment possible", fg="orange")

    def update_patient_table(self):
        self.patient_table.delete(*self.patient_table.get_children())
        for p in self.patients:
            self.patient_table.insert("", "end", values=(p["ID"], p["Name"], p["Age"], p["Ailment"], p["Doctor"]))

    def update_doctor_table(self):
        self.doctor_table.delete(*self.doctor_table.get_children())
        for d in self.doctors:
            self.doctor_table.insert("", "end", values=(d["ID"], d["Name"], d["Specialization"], d["Status"]))

    def on_closing(self):
        self.save_data()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = HospitalManagementSystemApp(root)
    root.mainloop()

