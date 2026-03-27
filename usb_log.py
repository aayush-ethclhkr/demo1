import tkinter as tk
from tkinter import filedialog, messagebox
import re
from datetime import datetime


def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.log"), ("All files", "*.*")])
    if file_path:
        file_name.set(file_path)
        analyze_log(file_path)
def analyze_log(file_path):
    try:
        with open(file_path, 'r') as f:
            logs = f.readlines()

        error_count = 0
        warning_count = 0
        info_count = 0
        filtered_logs = []
        internet_detected = False
        usb_detected = False
        keyword = keyword_entry.get().strip()

        for log in logs:
            timestamp = log.split(" ")[0]

            # Count log types
            if "ERROR" in log:
                error_count += 1
                filtered_logs.append(f"{timestamp} - {log.strip()}")
            elif "WARNING" in log:
                warning_count += 1
                filtered_logs.append(f"{timestamp} - {log.strip()}")
            elif "INFO" in log:
                info_count += 1
                filtered_logs.append(f"{timestamp} - {log.strip()}")

            # Keyword search
            if keyword and keyword.lower() in log.lower():
                filtered_logs.append(f"[Keyword Found] {log.strip()}")

            # Internet detection keywords
            if re.search(r"(connected to internet|gateway|dns|network connected|ip address)", log, re.IGNORECASE):
                internet_detected = True
                filtered_logs.append(f"[ Internet Detected] {log.strip()}")

            # USB detection keywords
            if re.search(r"(usb device|removable|drive letter|new device)", log, re.IGNORECASE):
                usb_detected = True
                filtered_logs.append(f"[ USB Detected] {log.strip()}")

        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END," ".join(filtered_logs))

        summary = f"Errors: {error_count}, Warnings: {warning_count}, Info: {info_count}"
        if internet_detected:
            summary += " |  System connected to Internet!"
        if usb_detected:
            summary += " |  USB connection detected!"
        summary_label.config(text=summary)

    except Exception as e:
        messagebox.showerror("Error", f"Log analysis failed: {str(e)}")

root = tk.Tk()
root.title(" Offline Log Analyzer Tool")
root.geometry("700x500")

file_name = tk.StringVar()
tk.Label(root, text="Log File:").pack(pady=5)
tk.Entry(root, textvariable=file_name, width=50, state='readonly').pack(pady=5)
tk.Button(root, text="Browse Log File", command=open_file).pack(pady=10)

tk.Label(root, text="Search for Keyword:").pack(pady=5)
keyword_entry = tk.Entry(root, width=50)
keyword_entry.pack(pady=5)

tk.Label(root, text="Log Analysis Results:").pack(pady=5)
result_text = tk.Text(root, height=15, width=80)
result_text.pack(pady=5)

summary_label = tk.Label(root, text="Errors: 0, Warnings: 0, Info: 0")
summary_label.pack(pady=5)


tk.Button(root, text="Analyze Logs", command=lambda: analyze_log(file_name.get())).pack(pady=10)

root.mainloop()
