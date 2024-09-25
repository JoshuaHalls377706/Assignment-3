# Assignment 3

# Group 137
# Mitchell Danks        S320289 
# Joshua Hall           S377706 
# Brooke Stokes         S364762 

# Repositorie Link : https://github.com/JoshuaHalls377706/Assignment-3.git
#---------------------------------------------------------------------------
import csv
from tkinter import *
from tkinter import messagebox, filedialog, ttk
from pathlib import Path
import webbrowser

# -- Functions --

def create_new_csv_file():
    """Makes a new File in a Choosen Location"""
    global CSV_FILE_NAME
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", 
                                               filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
    if file_path:
        CSV_FILE_NAME = Path(file_path)
        with open(CSV_FILE_NAME, mode='w', newline='') as file:
            writer = csv.writer(file)
        messagebox.showinfo("Success", f"New file created: {file_path}")
    
    Update_display()

def load_csv_file():
    """Loads a Existing File"""
    global CSV_FILE_NAME
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
    if file_path:
        CSV_FILE_NAME = Path(file_path)
        Update_display()

def Export_csv_file_search():
    """Exports the Current Displayed Table"""
    try:
        # Open a file dialog to choose the save location and file name
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", 
                                                   filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if not file_path:  # Check if user canceled the dialog
            return
        
        # Read the existing CSV file once and store the data in a dictionary
        lat_long_dict = {}
        with open(CSV_FILE_NAME, mode='r') as csv_file:
            reader = csv.reader(csv_file)
            for csv_row in reader:
                job_name = csv_row[0]
                job_ref = csv_row[1]
                lat_long_dict[(job_name, job_ref)] = (csv_row[2], csv_row[3])
        
        # Open the chosen file for writing
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            # Iterate through the rows in the table
            for row in table.get_children():
                values = table.item(row)['values']
                job_name = values[0]
                job_ref = values[1]
                
                # Get latitude and longitude from the dictionary if available
                lat, long = lat_long_dict.get((job_name, job_ref), (None, None))
                
                # Write each row to the new CSV file in the desired order
                writer.writerow([job_name, job_ref, lat, long, values[2], values[3]])
        
        # Notify user of success
        messagebox.showinfo("Success", f"Data exported successfully to {file_path}")
        
    except Exception as e:
        messagebox.showerror("File Error", f"Could not export data: {e}")

def export_entire_csv_file():
    """Exports the Whole File seen on and off table"""
    try:
        # Open a file dialog to choose the save location and file name
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", 
                                                   filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if not file_path:  # Check if user canceled the dialog
            return
        
        # Read the existing CSV file and store the data
        with open(CSV_FILE_NAME, mode='r') as csv_file:
            reader = csv.reader(csv_file)
            all_rows = list(reader)

        # Open the chosen file for writing
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(all_rows)  # Write all rows to the new CSV file
        
        # Notify user of success
        messagebox.showinfo("Success", f"Data exported successfully to {file_path}")
        
    except Exception as e:
        messagebox.showerror("File Error", f"Could not export data: {e}")

def load_data_from_csv(file_name, job):
    """Finds an Entry from the csv file"""
    with open(file_name, mode='r') as file:
        reader = csv.reader(file)
        found = False
        updated_data = []
        for row in reader:
            if row[0] == job and not found:
                found = True  # Skip the first occurrence
                continue
            updated_data.append(row)
    return updated_data

def write_data_to_csv(file_name, data):
    """Writes an Entry to the csv"""
    with open(file_name, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

def add_item():
    """Adds an Entry to the CSV File"""
    Name = job_name_entry.get()
    Job_Num = job_ref_entry.get()
    lat = lat_entry.get()
    long = long_entry.get()
    Class = classification_entry.get()
    date = completion_date_entry.get()

    if not validate_required_fields(Name, Job_Num, lat, long):
        return

    if not validate_coordinates(lat, long):
        return

    data = [Name, Job_Num, lat, long, Class, date]

    try:
        with open(CSV_FILE_NAME, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(data)
            messagebox.showinfo("Success", "Item added successfully.")
            Update_display()
    except Exception as e:
        messagebox.showerror("File Error", f"Could not write to file: {e}")

    Update_display()
    clear_entries()

def delete_item():
    """Deletes an Enrty from the CSV File"""
    selected_items = table.selection()
    if not selected_items:
        messagebox.showwarning("Selection Error", "Please select an item to delete.")
        return

    job_to_delete = table.item(selected_items[0])['values'][0]  # Get the first selected item

    if messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete '{job_to_delete}'?"):
        try:
            updated_data = load_data_from_csv(CSV_FILE_NAME, job_to_delete)
            write_data_to_csv(CSV_FILE_NAME, updated_data)

            table.delete(selected_items[0])  # Only delete the first selected item
            
            messagebox.showinfo("Success", "Selected item deleted successfully.")
        except Exception as e:
            messagebox.showerror("File Error", f"Could not update the file: {e}")

        Update_display()
        clear_entries()

def update_selected():
    """Replace the enrty with the new Entry"""
    selected_items = table.selection()
    if not selected_items:
        messagebox.showwarning("Selection Error", "Please select an item to update.")
        return
    
    # Get updated data from entry fields
    Name = job_name_entry.get()
    Job_Num = job_ref_entry.get()
    lat = lat_entry.get()
    long = long_entry.get()
    Class = classification_entry.get()
    date = completion_date_entry.get()

    if not validate_required_fields(Name, Job_Num, lat, long):
        return

    if not validate_coordinates(lat, long):
        return

    updated_data = [Name, Job_Num, lat, long, Class, date]
    job_to_update = table.item(selected_items[0])['values'][0]  # Get the job name to identify which to update

    if messagebox.askyesno("Confirm Update", f"Are you sure you want to update '{job_to_update}'?"):
        try:
            data = load_data_from_csv(CSV_FILE_NAME, job_to_update)
            data.append(updated_data)  # Add the new data
            write_data_to_csv(CSV_FILE_NAME, data)

            table.delete(selected_items[0])  # Remove old row from the display
            table.insert(parent='', index=END, values=[Name, Job_Num, Class, date])  # Insert updated row

            messagebox.showinfo("Success", "Item updated successfully.")
        except Exception as e:
            messagebox.showerror("File Error", f"Could not update the file: {e}")

        clear_entries()
  
def validate_required_fields(*args):
    """Checks if all required fields are filled."""
    if any(not arg for arg in args):
        messagebox.showwarning("Input Error", "Please fill in all required fields.")
        return False
    return True

def validate_coordinates(lat, long):
    """Validates latitude and longitude values."""
    try:
        lat_float = float(lat)
        long_float = float(long)
        if not (-90 <= lat_float <= 90):
            raise ValueError("Latitude must be between -90 and 90.")
        if not (-180 <= long_float <= 180):
            raise ValueError("Longitude must be between -180 and 180.")
    except ValueError as ve:
        messagebox.showwarning("Input Error", str(ve))
        return False
    return True

def Update_display():
    """Update the table display to show search results"""
    if CSV_FILE_NAME is None:
        return
    
    search_term = Search_entry.get().strip().lower()
    table.delete(*table.get_children())
    
    with open(CSV_FILE_NAME, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            should_display = False
            # Check filters and search term
            if filter_job_name_var.get() and search_term in row[0].lower():
                should_display = True
            if filter_job_ref_var.get() and search_term in row[1].lower():
                should_display = True
            if filter_classification_var.get() and search_term in row[4].lower():
                should_display = True
            if filter_date_var.get() and search_term in row[5].lower():
                should_display = True

            if should_display:
                selected_items = [row[0], row[1], row[4], row[5]]
                table.insert(parent='', index=END, values=selected_items)
    
    if not table.get_children():
        messagebox.showinfo("Search Result", "No items found matching the search term.")

def clear_entries():
    """Clears all input fields."""
    job_name_entry.delete(0, END)
    job_ref_entry.delete(0, END)
    classification_entry.delete(0, END)
    completion_date_entry.delete(0, END)
    lat_entry.delete(0, END)
    long_entry.delete(0, END)

def clear_Search():
    """Clears Search Entry and resets the table to show all entries."""
    Search_entry.delete(0, END)
    filter_job_name_var.set(1)
    filter_job_ref_var.set(1)
    filter_classification_var.set(1)
    filter_date_var.set(1)
    Update_display()  # Refresh to show all entries

def Pull_selected():
    """Pull an entry and fill all inputs"""
    selected_items = table.selection()
    if not selected_items:
        messagebox.showwarning("Selection Error", "Please select an item to update.")
        return
    
    # Get the selected row's job name, job reference, classification, and date
    selected_values = table.item(selected_items[0])['values']
    job_name_to_find = selected_values[0]
    job_ref_to_find = selected_values[1]
    classification_to_find = selected_values[2]
    date_to_find = selected_values[3]
    
    try:
        with open(CSV_FILE_NAME, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                # Match job name, job reference, classification, and date
                if (row[0] == job_name_to_find and 
                    row[1] == job_ref_to_find and 
                    row[4] == classification_to_find and 
                    row[5] == date_to_find):
                    
                    # Populate the entry fields with the found row's data
                    job_name_entry.delete(0, END)
                    job_name_entry.insert(0, row[0])
                    
                    job_ref_entry.delete(0, END)
                    job_ref_entry.insert(0, row[1])
                    
                    lat_entry.delete(0, END)
                    lat_entry.insert(0, row[2])
                    
                    long_entry.delete(0, END)
                    long_entry.insert(0, row[3])
                    
                    classification_entry.delete(0, END)
                    classification_entry.insert(0, row[4])
                    
                    completion_date_entry.delete(0, END)
                    completion_date_entry.insert(0, row[5])
                    
                    break
    except Exception as e:
        messagebox.showerror("File Error", f"Could not read from file: {e}")

def Pull_Silent_selected():
    """Pull Results without filling Inputs"""
    selected_items = table.selection()
    if not selected_items:
        messagebox.showwarning("Selection Error", "Please select an item to update.")
        return
    
    # Get the selected row's job name, job reference, classification, and date
    selected_values = table.item(selected_items[0])['values']
    job_name_to_find = selected_values[0]
    job_ref_to_find = selected_values[1]
    classification_to_find = selected_values[2]
    date_to_find = selected_values[3]
    
    try:
        with open(CSV_FILE_NAME, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                # Match job name, job reference, classification, and date
                if (row[0] == job_name_to_find and 
                    row[1] == job_ref_to_find and 
                    row[4] == classification_to_find and 
                    row[5] == date_to_find):
                    # Populate the entry fields with the found row's data
                    job_name_data = row[0]; job_ref_data = row[1]; lat_data = row[2]
                    long_data = row[3]; classification_data = row[4]; completion_date_data = row[5]
                    Data = [job_name_data, job_ref_data, lat_data, long_data, classification_data, completion_date_data]

                    return Data
    except Exception as e:
        messagebox.showerror("File Error", f"Could not read from file: {e}")

def Open_Google_Maps():
    """Display the location on Google Maps"""
    data = Pull_Silent_selected()
    latitude = data[2]
    longitude = data[3]
    print(latitude, longitude)
    # URL to drop a pin at the specified coordinates
    url = f"https://www.google.com/maps?q={latitude},{longitude}"
    webbrowser.open(url)

# -- Actual Code --
CSV_FILE_NAME = None
COLUMN_HEADERS = ["Job Name", "Job Reference", "Lat", "Long", "Classification", "Date of Completion"]

# -- Main Frames --
window = Tk()
window.geometry('850x550')
window.title("Ground Investigation Database")

# -- menus --
menu = Menu(window)
window.config(menu=menu)

subMenu = Menu(menu)
menu.add_cascade(label="File", menu=subMenu)
subMenu.add_command(label="New File", command=create_new_csv_file)
subMenu.add_command(label="Open File", command=load_csv_file)
subMenu.add_command(label="Save File", command=export_entire_csv_file)
subMenu.add_separator()
subMenu.add_command(label="Export Current", command=Export_csv_file_search)

# -- entry fields --
entry_frame = Frame(window, width=100, height=50)
entry_frame.pack(side='top', padx=10, pady=5)

# Create labels and place them in the frame
Input_Label = Label(entry_frame, text="-- Inputs --", fg="green", font=("Arial", 12, "bold"))
Input_Label.grid(row=0, column=0, columnspan=6, pady=(0, 10))

job_name_label = Label(entry_frame, text="Job Name")
job_name_label.grid(row=1, column=0, sticky=E, padx=5, pady=5)

job_ref_label = Label(entry_frame, text="Job Reference")
job_ref_label.grid(row=1, column=2, sticky=E, padx=5, pady=5)

completion_date_label = Label(entry_frame, text="Completion Date")
completion_date_label.grid(row=1, column=4, sticky=E, padx=5, pady=5)

classification_label = Label(entry_frame, text="Classification")
classification_label.grid(row=2, column=0, sticky=E, padx=5, pady=5)

lat_label = Label(entry_frame, text="Latitude")
lat_label.grid(row=2, column=2, sticky=E, padx=5, pady=5)

long_label = Label(entry_frame, text="Longitude")
long_label.grid(row=2, column=4, sticky=E, padx=5, pady=5)

# Create entry fields and place them in the frame
job_name_entry = Entry(entry_frame, width=15)
job_name_entry.grid(row=1, column=1, padx=5, pady=5)

job_ref_entry = Entry(entry_frame, width=15)
job_ref_entry.grid(row=1, column=3, padx=5, pady=5)

completion_date_entry = Entry(entry_frame, width=15)
completion_date_entry.grid(row=1, column=5, padx=5, pady=5)

classification_entry = Entry(entry_frame, width=15)
classification_entry.grid(row=2, column=1, padx=5, pady=5)

lat_entry = Entry(entry_frame, width=15)
lat_entry.grid(row=2, column=3, padx=5, pady=5)

long_entry = Entry(entry_frame, width=15)
long_entry.grid(row=2, column=5, padx=5, pady=5)

# -- Buttons Frame --
Button_frame = Frame(window, width=100, height=50)
Button_frame.pack(side='top', padx=10, pady=5)
# Create Buttons
save_button = Button(Button_frame, text="  Add  ", command=add_item)
save_button.grid(row=3, column=0, padx=5, pady=5)

Delete_button = Button(Button_frame, text="  Remove  ", command=delete_item)
Delete_button.grid(row=3, column=1, padx=5, pady=5)

Update_button = Button(Button_frame, text="Update", command=update_selected)
Update_button.grid(row=3, column=2, padx=5, pady=5)

Pull_button = Button(Button_frame, text="Pull Data", command=Pull_selected)
Pull_button.grid(row=3, column=3, padx=5, pady=5)

Clear_button = Button(Button_frame, text="Clear Inputs", command=clear_entries)
Clear_button.grid(row=3, column=4, padx=5, pady=5)

# -- Table fields --
Table_frame = Frame(window, width=300, height=5000)
Table_frame.pack(side='top', padx=20, pady=5)

# Make Table
table = ttk.Treeview(Table_frame, columns=('Name', 'Reference', 'Class', 'Date'), show='headings')
table.heading('Name', text='Job Name')
table.heading('Reference', text='Job Reference')
table.heading('Class', text='Classification')
table.heading('Date', text='Completion Date')
table.pack(side='top', fill='both', expand=True)

# -- Search and Filter Frames --
search_frame = Frame(window)
search_frame.pack(side='left', padx=20, pady=20)
# Create Lable
search_Label = Label(search_frame, text="-- Search Input --", fg="green", font=("Arial", 12, "bold"))
search_Label.grid(row=0, column=0, columnspan=2, pady=(0, 10))

# Create Entry
Search_entry = Entry(search_frame, width=30)
Search_entry.grid(row=1, column=0, columnspan=2, pady=(0, 10))

# Create Buttons
Search_button = Button(search_frame, text="Search", command=Update_display)
Search_button.grid(row=2, column=0, pady=5)

Search_Clear_button = Button(search_frame, text="Clear Search", command=clear_Search)
Search_Clear_button.grid(row=2, column=1, pady=5)

# Filter Frame
filter_frame = Frame(window)
filter_frame.pack(side='left', padx=20, pady=20)

# Create checkboxes
filter_job_name_var = IntVar(value=1)
filter_job_ref_var = IntVar(value=1)
filter_classification_var = IntVar(value=1)
filter_date_var = IntVar(value=1)

filter_job_name_checkbox = Checkbutton(filter_frame, text="Job Name", variable=filter_job_name_var)
filter_job_name_checkbox.grid(row=0, column=0, sticky=W)

filter_job_ref_checkbox = Checkbutton(filter_frame, text="Job Reference", variable=filter_job_ref_var)
filter_job_ref_checkbox.grid(row=1, column=0, sticky=W)

filter_classification_checkbox = Checkbutton(filter_frame, text="Classification", variable=filter_classification_var)
filter_classification_checkbox.grid(row=2, column=0, sticky=W)

filter_date_checkbox = Checkbutton(filter_frame, text="Completion Date", variable=filter_date_var)
filter_date_checkbox.grid(row=3, column=0, sticky=W)

# -- Extra Functions --
Extra_Functions_Frame = Frame(window)
Extra_Functions_Frame.pack(side='left', padx=20, pady=20)

#Label
Function_Label = Label(Extra_Functions_Frame, text="-- Functions --", fg="green", font=("Arial", 12, "bold"))
Function_Label.grid(row=0, column=0, columnspan=2,)

# Button
Google_Maps_Button = Button(Extra_Functions_Frame, text="Google Maps", command=Open_Google_Maps)
Google_Maps_Button.grid(row=1, column=0, padx=10, pady=10)

Export_Button = Button(Extra_Functions_Frame, text="Export Current", command=Export_csv_file_search)
Export_Button.grid(row=1, column=1, padx=10, pady=10)

# --- Run loop ---

# Initial update to display contents if the file exists
Update_display()

window.mainloop()
