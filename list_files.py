import os
import platform

def list_files(start_path):
    """Recursively list all files, including hidden files, starting from start_path."""
    files = []
    for dirpath, dirnames, filenames in os.walk(start_path):
        # Filter out hidden files/folders on Unix-based systems (macOS/Linux)
        if platform.system() in ["Darwin", "Linux"]:
            dirnames[:] = [d for d in dirnames if not d.startswith('.')]  # Exclude hidden directories
        
        for filename in filenames:
            # Get the full path of the file
            file_path = os.path.join(dirpath, filename)
            files.append(file_path)

    return files

def save_files_to_log(files, output_file="files_list.txt"):
    """Write the list of files to a log file."""
    with open(output_file, 'w') as f:
        for file in files:
            f.write(file + "\n")
    print(f"File list saved to {output_file}")

def main():
    # Get the root directory depending on the OS
    if platform.system() == "Windows":
        start_path = "C:\\"
    else:
        start_path = "/"  # Root directory for macOS/Linux

    print(f"Listing all files starting from: {start_path}")
    files = list_files(start_path)
    save_files_to_log(files)

if __name__ == "__main__":
    main()