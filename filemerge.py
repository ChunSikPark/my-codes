import tkinter as tk
from tkinter import ttk
from tkinterdnd2 import DND_FILES, TkinterDnD
import os
import string

class FileDropApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Drag and Drop File Uploader")

        self.frame = ttk.Frame(root, padding=10)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.option_counter = 0
        self.listboxes = []
        self.result = None  # Store result to return later

        self.add_option_box()

        # Add buttons
        btn_frame = ttk.Frame(self.frame)
        btn_frame.pack(pady=10)

        add_btn = ttk.Button(btn_frame, text="Add Option Box", command=self.add_option_box)
        add_btn.pack(side=tk.LEFT, padx=5)

        finish_btn = ttk.Button(btn_frame, text="Finish Upload", command=self.handle_finish_upload)
        finish_btn.pack(side=tk.LEFT, padx=5)

    def add_option_box(self):
        title = f"Option {string.ascii_uppercase[self.option_counter]}"
        self.option_counter += 1

        label = ttk.Label(self.frame, text=title)
        label.pack(anchor=tk.W)

        listbox = tk.Listbox(self.frame, selectmode=tk.MULTIPLE, width=80, height=5)
        listbox.pack(pady=5, fill=tk.X)

        listbox.drop_target_register(DND_FILES)
        listbox.dnd_bind('<<Drop>>', lambda e, lb=listbox: self.on_drop(e, lb))

        self.listboxes.append((title, listbox))

    def on_drop(self, event, listbox):
        files = self.root.tk.splitlist(event.data)
        for file in files:
            if os.path.isfile(file) and file not in listbox.get(0, tk.END):
                listbox.insert(tk.END, file)

    def handle_finish_upload(self):
        result = []
        for title, lb in self.listboxes:
            file_list = [lb.get(i) for i in range(lb.size())]
            result.append((title, file_list))

        self.result = result
        self.root.quit()  # Close the Tkinter loop but keep the app object

def run_app():
    root = TkinterDnD.Tk()
    app = FileDropApp(root)
    root.mainloop()
    root.destroy()  # Fully close window
    return app.result  # Return the result

# Example of calling the app and using the result
if __name__ == "__main__":
    uploaded_files = run_app()
    print("\nReturned Data Structure:")
    for option, files in uploaded_files:
        print(f"{option}:")
        for f in files:
            print(f"  {f}")
        if not files:
            print("  [No files uploaded]")
    
    print(uploaded_files[0][0],uploaded_files[0][1])
