import tkinter as tk
from tkinter import filedialog
import subprocess
import time

class CppViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("C++ File Viewer")

        # Set default theme
        self.theme = "light"
        self.root.configure(bg="#F5F5F5")

        # Create left and right frames
        left_frame = tk.Frame(root, width=400, height=400)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        right_frame = tk.Frame(root, width=400, height=400)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Create text widget for left frame
        self.text_widget = tk.Text(left_frame, wrap=tk.WORD)
        self.text_widget.configure(bg="white", fg="black")
        self.text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create scrollbar for left frame
        scrollbar = tk.Scrollbar(left_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Link scrollbar to text widget
        self.text_widget.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.text_widget.yview)

        # Create menu bar
        menu_bar = tk.Menu(root)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Open C++ File", command=self.open_file)
        menu_bar.add_cascade(label="File", menu=file_menu)

        run_menu = tk.Menu(menu_bar, tearoff=0)
        run_menu.add_command(label="Run Code", command=self.run_code)
        menu_bar.add_cascade(label="Run", menu=run_menu)


        theme_menu = tk.Menu(menu_bar, tearoff=0)
        theme_menu.add_command(label="Toggle Theme", command=self.toggle_theme)
        menu_bar.add_cascade(label="Theme", menu=theme_menu)
        root.config(menu=menu_bar)

        # Create button to run code
        self.run_button = tk.Button(right_frame, text="Run Code", command=self.run_code)
        self.run_button.pack(side=tk.LEFT)

        




        # Create button to stop code
        #self.stop_button = tk.Button(right_frame, text="Stop Code", command=self.stop_code, state=tk.DISABLED)
        #self.stop_button.pack(side=tk.LEFT)

        # Create text widget for right frame
        self.output_widget = tk.Text(right_frame, wrap=tk.WORD)
        self.output_widget.configure(bg="white", fg="black")
        self.output_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create scrollbar for right frame
        scrollbar = tk.Scrollbar(right_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Link scrollbar to text widget
        self.output_widget.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.output_widget.yview)

        self.process = None

    def toggle_theme(self):
        if self.theme == "light":
            self.theme = "dark"
            self.root.configure(bg="#1E1E1E")
            self.text_widget.configure(bg="#1E1E1E", fg="#F5F5F5")
            self.output_widget.configure(bg="#1E1E1E", fg="#F5F5F5")
        else:
            self.theme = "light"
            self.root.configure(bg="#F5F5F5")
            self.text_widget.configure(bg="white", fg="black")
            self.output_widget.configure(bg="white", fg="black")

    def open_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, "r") as file:
                file_contents = file.read()
                self.text_widget.delete("1.0", tk.END)
                self.text_widget.insert(tk.END, file_contents)

    def run_code(self):
        
        self.run_button.config(state=tk.DISABLED)
        #self.stop_button.config(state=tk.NORMAL)
        self.output_widget.delete("1.0", tk.END)

        code = self.text_widget.get("1.0", tk.END)
        try:
            compile_process = subprocess.Popen(["g++", "-x", "c++", "-", "-o", "output.exe"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = compile_process.communicate(input=code.encode())
            if not stderr:
                run_process = subprocess.Popen(["./output.exe"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                start_time = time.time()
                stdout, stderr = run_process.communicate()
                end_time = time.time()
                self.output_widget.insert(tk.END, stdout.decode())

                # Calculate and display execution time in red color
                execution_time = f"\n\nExecution time: {(end_time - start_time)*1000:.2f} ms"
                self.output_widget.insert(tk.END, execution_time, "red")
                self.output_widget.tag_config("red", foreground="red")

            else:
                self.output_widget.insert(tk.END, stderr.decode())
            #self.stop_code()
        except subprocess.CalledProcessError as e:
            self.output_widget.insert(tk.END, e.output.decode())

        self.run_button.config(state=tk.NORMAL)    

    

if __name__ == '__main__':
    root = tk.Tk()
    app = CppViewer(root)
    root.mainloop()