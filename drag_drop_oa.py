import sys
import os
import subprocess


def process_dropped_folder(folder_path):
    # Call the main script with the folder path as an argument
    script_path = os.path.join(os.path.dirname(sys.executable), 'oa_processor.py')
    print(f"Calling script: {script_path} with argument: {folder_path}")  # Debug print
    result = subprocess.run([sys.executable, script_path, folder_path])
    
    if result.returncode != 0:
        print(f"Script exited with error code: {result.returncode}")  # Print error code
    else:
        print("Script executed successfully.")


if __name__ == "__main__":
    print("Drag and drop a folder onto the executable.")
    
    # No input prompt here; directly check command-line arguments
    print(f"Arguments received: {sys.argv}")  # Debug print
    if len(sys.argv) < 2:
        print("Please drag and drop a folder onto the executable.")
        input("Press Enter to exit...")
        sys.exit(1)

    # Join the arguments if there are multiple parts (in case of spaces)
    folder_path = ' '.join(sys.argv[1:])  
    print(f"Received folder path: {folder_path}")  # Debug print
    if not os.path.isdir(folder_path):
        print("The dropped item is not a folder.")
        input("Press Enter to exit...")
        sys.exit(1)
    
    process_dropped_folder(folder_path)
    print("Processing complete.")
    input("Press Enter to exit...")
