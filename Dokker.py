import webbrowser
from urllib.parse import quote
import tkinter as tk


# Create the main window
root = tk.Tk()
root.title("Web Search Tool")

# Set up the main layout
main_frame = tk.Frame(root, padx=10, pady=10)
main_frame.pack()

allintext_var = tk.BooleanVar()
allintext_checkbox = tk.Checkbutton(main_frame, text='allintext:', variable=allintext_var)
allintext_checkbox.grid(row=0, column=2)

def on_search_button_click():
    query_text = query_entry.get()
    operators = [(op.get(), text_entry.get()) for op, text_entry in additional_inputs]
    if allintext_var.get():
        query_text = "allintext:" + query_text
        #operators = [(op, "allintext:" + text) for op, text in operators]
    query = build_query(query_text, operators)
    url = f"https://www.google.com/search?q={query}"
    if site_checkbox_var.get():
        url += f" site:{url_entry.get()}"
    webbrowser.open(url)


query_label = tk.Label(main_frame, text="Enter your search query:")
query_label.grid(row=0, column=0)



query_entry = tk.Entry(main_frame)
query_entry.grid(row=0, column=1)

additional_inputs = []
row_index = 0
def on_add_button_click():
    global additional_inputs_frame, row_index
    # create a new row to add to the frame
    new_row = tk.Frame(additional_inputs_frame)
    new_row.grid(row=row_index, column=0, columnspan=4, pady=5)

    # create the dropdown menu for the operator
    operator = tk.StringVar(root)
    operator.set("AND")
    tk.OptionMenu(new_row, operator, "AND", "OR", "NOT").grid(row=0, column=0)

    # create the text entry field for the search term
    text_entry = tk.Entry(new_row)
    text_entry.grid(row=0, column=1)

    # create the remove button and callback
    remove_button = tk.Button(new_row, text="X", command=lambda row=new_row: on_remove_button_click(row))
    remove_button.grid(row=0, column=2)

    # add the new row's operator and text entry fields to the additional_inputs list
    additional_inputs.append((operator, text_entry))

    # increment the row index
    row_index += 1
    
def on_remove_button_click(row):
    global additional_inputs_frame, row_index
    
    # remove the row from the frame
    row.destroy()
    
    # remove the corresponding operator and text entry fields from the additional_inputs list
    for item in additional_inputs:
        if item[1].winfo_parent() == row.winfo_id():
            additional_inputs.remove(item)
    
    # decrement the row index if there are additional rows
    if row_index > 0:
        row_index -= 1
    


url_label = tk.Label(main_frame, text="Enter a website URL to search within (optional):")
url_label.grid(row=3, column=0)
url_entry = tk.Entry(main_frame)
url_entry.grid(row=3, column=1)
site_checkbox_var = tk.BooleanVar()
site_checkbox = tk.Checkbutton(main_frame, text='Search only within this website', variable=site_checkbox_var)
site_checkbox.grid(row=3, column=2)

additional_inputs_frame = tk.Frame(main_frame)
additional_inputs_frame.grid(row=1, column=0, columnspan=2)
add_button = tk.Button(main_frame, text="+", command=on_add_button_click)
add_button.grid(row=0, column=3)

search_button = tk.Button(main_frame, text="Search", command=on_search_button_click)
search_button.grid(row=5, column=0, columnspan=3)

file_types = ["txt","pdf", "ppt", "xls", "csv", "log", "doc", "docx", "pptx", "xlsx"]
file_type_vars = {}
# Set up the file types frame
file_types_frame = tk.Frame(main_frame)
file_types_frame.grid(row=2, column=0, columnspan=1, sticky='w')
tk.Label(file_types_frame, text="Choose file types to search for:").grid(row=0, column=0)

file_type_vars = {}
for i, file_type in enumerate(file_types):
    file_type_var = tk.IntVar()
    tk.Checkbutton(file_types_frame, text=f"{file_type}", variable=file_type_var).grid(row=i//4+1, column=i%4)
    file_type_vars[file_type] = file_type_var

def build_query(query_text, operators, allintext=False):
    operators_dict = {"AND": "+", "OR": "|", "NOT": "-"}
    joined_query = "allintext:" if allintext else ""
    joined_query += query_text
    for operator, text in operators:
        joined_query += f" {operators_dict[operator]} {text}"
    
    selected_file_types = []
    for file_type, var in file_type_vars.items():
        if var.get() == 1:
            selected_file_types.append(file_type)
    
    if selected_file_types:
        file_type_query = " OR ".join([f"filetype:{file_type}" for file_type in selected_file_types])
        joined_query += f" {file_type_query}"
    
    return quote(joined_query)
# Initialize the additional input fields
additional_inputs = []
row_index = 0

root.mainloop()