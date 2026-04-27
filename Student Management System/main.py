import tkinter as tk
from gui import StudentManagementGUI

def main():
    root = tk.Tk()
    app = StudentManagementGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()