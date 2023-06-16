import tkinter as tk
from tkinter import messagebox, filedialog
def asker(file):
    def close_app():
        root.destroy()

    def save_file():
        result = messagebox.askquestion("Save File", "You have a file, do you want to save it?")
        if result == 'yes':
            folder_path = filedialog.askdirectory()
            try:
                file.save(folder_path+'/'+file.filename)
            except Exception as err:
                messagebox.showerror('An error in saving the file', str(err))
            else:
                messagebox.showinfo('file saved', 'file saved sucessfully!')
            

    root = tk.Tk()
    root.title("Save File")
    root.geometry("400x200")
    root.config(bg="#202020")

    label = tk.Label(root, text="Click the button to save a file", fg="#fff", bg="#202020", font=("Arial", 14))
    label.pack(pady=20)

    button = tk.Button(root, text="Save File", command=save_file, bg="#555", fg="#fff", font=("Arial", 12), padx=10, pady=5, borderwidth=0)
    button.pack(pady=10)

    root.mainloop()