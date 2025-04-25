import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import filedialog, messagebox
import subprocess
import os

# main window
root = tk.Tk()
root.title("moskov")
root.geometry("800x800")  # width and height in pixels

# Code editor with a scrollable text area
fontchoice = "courier"
code_editor = ScrolledText(root, wrap=tk.WORD, font=(fontchoice, 14), undo=True)
sidebar = tk.Frame(root, width=100, bg="lightgray", height=600, padx=5, pady=5)
sidebar.pack(side="left", fill="y")
code_editor.pack(fill=tk.BOTH, expand=True)

file_path = None

# Function to auto-close brackets
def auto_close(event):
    char = event.char
    if char == '(':
        code_editor.insert(tk.INSERT, ')')
        code_editor.mark_set(tk.INSERT, code_editor.index(tk.INSERT) + " - 1 chars")
    elif char == '{':
        code_editor.insert(tk.INSERT, '}')
        code_editor.mark_set(tk.INSERT, code_editor.index(tk.INSERT) + " - 1 chars")
    elif char == '[':
        code_editor.insert(tk.INSERT, ']')
        code_editor.mark_set(tk.INSERT, code_editor.index(tk.INSERT) + " - 1 chars")
    elif char == '"':
        code_editor.insert(tk.INSERT, '"')
        code_editor.mark_set(tk.INSERT, code_editor.index(tk.INSERT) + " - 1 chars")
    elif char == "'":
        code_editor.insert(tk.INSERT, "'")
        code_editor.mark_set(tk.INSERT, code_editor.index(tk.INSERT) + " - 1 chars")

# Function to save the code as a new file
def change_typefont():
    global fontchoice
    if fontchoice == "courier":
        fontchoice = "Consolas"
    else:
        fontchoice = "courier"
    code_editor.config(font=(fontchoice, 14))

def save_as_file(event=None):
    global file_path
    code = code_editor.get("1.0", tk.END)  # Get text from the editor
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text Files", "*.txt"), 
                                                      ("Python Files", "*.py"), 
                                                      ("All Files", "*.*")])
    if file_path:
        with open(file_path, "w") as file:
            file.write(code)  # Write code to the file

# Function to save the file if it's already saved
def save_file(event=None):
    global file_path
    if file_path:
        code = code_editor.get("1.0", tk.END)
        with open(file_path, "w") as file:
            file.write(code)
    else:
        save_as_file()

# Function to open a file and load its content into the editor
def open_file(event=None):
    global file_path
    file_path = filedialog.askopenfilename(defaultextension=".txt",
                                           filetypes=[("Text Files", "*.txt"),
                                                    ("Python Files", "*.py"),
                                                    (" Files", "*.c"),
                                                    ("All Files", "*.*")])
    if file_path:
        with open(file_path, "r") as file:
            code = file.read()
            code_editor.delete("1.0", tk.END)  # Clear existing content in the editor
            code_editor.insert("1.0", code)  # Insert file content at the start

# Function to open a terminal window and compile/execute code
def open_terminal():
    # Create a new top-level window (terminal)
    new_terminal = tk.Toplevel(root)
    new_terminal.title("Terminal")
    new_terminal.geometry("700x700")  # Set size for the new window

    # Create a text widget to display terminal output
    terminal_output = tk.Text(new_terminal, wrap=tk.WORD, height=25)
    terminal_output.pack(fill=tk.BOTH, expand=True)

    # Compile and execute the code from the editor
    code = code_editor.get("1.0", tk.END).strip()
    if code == "":
        terminal_output.insert(tk.END, "No code to compile.\n")
        return

    # Save the code to a temporary file (for compiling)
    temp_file = "temp_code.c"
    with open(temp_file, "w") as file:
        file.write(code)

    # Set the GCC command (adjust path to your GCC compiler if necessary)
    compile_command = ["gcc", temp_file, "-o", "output.exe"]
    
    try:
        # Compile the code
        process = subprocess.Popen(compile_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        # Decode and output the compilation result in the terminal window
        if stdout:
            terminal_output.insert(tk.END, stdout.decode())
        if stderr:
            # Ensure errors are properly captured and displayed
            terminal_output.insert(tk.END, f"Compilation errors:\n{stderr.decode()}\n")

        # Execute the compiled program if successful
        if process.returncode == 0:
            terminal_output.insert(tk.END, "\nCompilation successful. Running the compiled program...\n")
            run_process = subprocess.Popen(["./output.exe"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            run_stdout, run_stderr = run_process.communicate()
            if run_stdout:
                terminal_output.insert(tk.END, run_stdout.decode())
            if run_stderr:
                terminal_output.insert(tk.END, f"Execution errors:\n{run_stderr.decode()}\n")
        else:
            terminal_output.insert(tk.END, "Compilation failed.\n")
    except Exception as e:
        terminal_output.insert(tk.END, f"Error occurred: {str(e)}\n")
    finally:
        # Clean up temporary file
        if os.path.exists(temp_file):
            os.remove(temp_file)


#color night tracker
night=False
def night_mode():
    global night
    if night==False:
     code_editor.config(bg="#2e2e2e",fg="#dcdcdc",insertbackground="white")
     night=True

    else:
         code_editor.config(bg="white",fg="black")
         night=False
        

# Save button
root.bind("<Control-s>", save_file)  # Ctrl+S to save
root.bind("<Control-S>", save_as_file)  # Ctrl+Shift+S to Save As
root.bind("<Control-o>", open_file)  # Ctrl+O to open file
code_editor.bind("<KeyPress>", auto_close)  # Auto-close brackets

# Sidebar buttons
saveas_button = tk.Button(sidebar, text="Save As", command=save_as_file)
save_button = tk.Button(sidebar, text="Save", command=save_file)
open_button = tk.Button(sidebar, text="Open", command=open_file)
bold_textbutton = tk.Button(sidebar, text="beautiful text/for your eyes", command=change_typefont)
compile_button = tk.Button(sidebar, text="Compile/Execute", command=open_terminal)
night_button=tk.Button(sidebar,text="night mode(*recommended)",command=night_mode)
save = tk.Label(sidebar, text="Save : C-s")
save.pack()

saveas = tk.Label(sidebar, text="Save As : C-shift-s")
saveas.pack()

open_label = tk.Label(sidebar, text="Open : C-o")
open_label.pack()

saveas_button.pack()
open_button.pack()
save_button.pack()
bold_textbutton.pack()
compile_button.pack()
night_button.pack()

root.mainloop()
