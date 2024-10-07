import sys
import os
import subprocess


def process_dropped_folder(folder_path):
    # Call the main script with the folder path as an argument
    script_path = os.path.join(os.path.dirname(sys.executable), 'oa_processor.py')
    subprocess.run([sys.executable, script_path, folder_path])  # No quotes needed here

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Please drag and drop a folder onto the executable.")
        input("Press Enter to exit...")
        sys.exit(1)
    
    folder_path = sys.argv[1]
    print(f"Received folder path: {folder_path}")  # Debug print
    if not os.path.isdir(folder_path):
        print("The dropped item is not a folder.")
        input("Press Enter to exit...")
        sys.exit(1)
    
    process_dropped_folder(folder_path)
    print("Processing complete.")
    input("Press Enter to exit...")