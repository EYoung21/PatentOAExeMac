#ask Yoni:
#provide more (20-50) example pdfs
#ask how I could figure out the type of an OA


import fitz  # PyMuPDF
from PIL import Image
import pytesseract
import io
from pdf2docx import Converter
import docx
import os
from docx import Document
import re
from pypdf import PdfReader
import pypandoc
import csv
import openai
from dotenv import load_dotenv
from openai import OpenAI
from tkinter import Tk
from tkinter.filedialog import askdirectory  # for folder selection
import tkinter
from cx_Freeze import setup, Executable
import sys

class Solution():

    def __init__(self):
        pass

    # def defineUserInput(self):
    #     self.user_input = input("Which file would you like to examine? ")
    #     return self.user_input


    def extract_text_from_pdf(self, PDFPath):
        
        pdf_document = fitz.open(PDFPath)

        extracted_text = ""
        
        for page_num in range(len(pdf_document)):
            page = pdf_document[page_num]
            # Extract text
            text = page.get_text()
            extracted_text += text
            
            # If no text found, look for images
            if not text.strip():  # No text found
                # print(f"No text found on page {page_num + 1}. Now searching for images.")
                image_list = page.get_images(full=True)

                if image_list:
                    for img_index, img in enumerate(image_list, start=1):
                        # Extract the image bytes
                        base_image = pdf_document.extract_image(img[0])
                        image_bytes = base_image["image"]

                        # Convert to a PIL Image
                        image = Image.open(io.BytesIO(image_bytes))

                        # Apply OCR to the image
                        ocr_text = pytesseract.image_to_string(image)
                        extracted_text += ocr_text
                        # print(f"Text extracted from image {img_index} on page {page_num + 1}.")

        return extracted_text
    
    def defineREGEX(self, stringInput):
        # Normalize the text, preserving newlines
        normalized_text = re.sub(r'[^\S\n]+', ' ', stringInput)

        # Define patterns
        application_id_pattern = r"\d{2}/\d{3},\d{3}"
        reference_number_pattern = r"\d{4}-[A-Za-z0-9]+"
        due_date_pattern = r"\d{2}/\d{2}/\d{4}"
        examiner_name_pattern = r"[A-Z]+,\s*[A-Z]+(?:\s[A-Z]\.?)?"

        # Updated telephone pattern to handle line breaks
        updated_telephone_pattern = r"whose\s+telephone\s+number\s+is\s*(?:\(?\d{3}\)?[-.\s]?\n?){2}\d{4}"

        # Find patterns
        application_id = re.findall(application_id_pattern, normalized_text)
        phones = re.findall(updated_telephone_pattern, normalized_text, re.DOTALL)
        refMatches = re.findall(reference_number_pattern, normalized_text)
        dateMatches = re.findall(due_date_pattern, normalized_text)
        examiner_name_match = re.findall(examiner_name_pattern, stringInput)

        # Assign values
        self.applicationID = application_id[0] if application_id else None
        self.refrenceNumber = refMatches[1] if len(refMatches) > 1 else None
        self.dueDate = dateMatches[1] if len(dateMatches) > 1 else None
        self.examinerName = examiner_name_match[0] if examiner_name_match else None
        self.phone_numbers = [re.sub(r'\s+', '', phone) for phone in phones]  # Clean up extracted phone numbers
        self.total_refs = refMatches


#   /Users/eliyoung/Desktop/PatentOAs/1535-111CIP2_WB-201703-008-1-US1_Final Office Action 4.pdf   #didnt pickup phone #
#   /Users/eliyoung/Desktop/PatentOAs/1535-727_WB-202105-023-1_Final Office Action2.pdf
#   /Users/eliyoung/Desktop/PatentOAs/1535-740_WB-202107-012-1_Final Office Action2.pdf
#   /Users/eliyoung/Desktop/PatentOAs/1535-755_WB-202108-020-1_Final Office Action 2.pdf
#   /Users/eliyoung/Desktop/PatentOAs/1535-757 WB-202109-017-1 Office Action.pdf
#   /Users/eliyoung/Desktop/PatentOAs/1535-806 WB-202202-012-1 Office Action.pdf



# Specify the directory name with a full or relative path
# import os

#/Users/eliyoung/Yoni\ Patent\ Project/.venv/bin/python3 -m <msg>

#run rye run pyinstaller --onefile --windowed --hidden-import=scipy.special._cdflib OAScript
# or pyinstaller --onefile --windowed --hidden-import=scipy.special._cdflib OAScript
#to create exe

#NEW RUN FILE
#rye run pyinstaller oa_processor.spec  

def main(directory):

    home_directory = os.path.expanduser("~")

    # Construct the Desktop path
    desktop_path = os.path.join(home_directory, "Desktop")

    # Specify the directory name
    directory_name = os.path.join(desktop_path, "OAInfoParentFolder")

    # Create the directory
    try:
        os.makedirs(directory_name)  # Use os.mkdir(directory_name) for a single directory
        print(f"Directory '{directory_name}' created successfully on Desktop.")
    except FileExistsError:
        print(f"Directory '{directory_name}' already exists.")
    except Exception as e:
        print(f"An error occurred: {e}")


    # Define the CSV file path
    csv_file_path = os.path.join(directory_name, "data.csv")
    # Define the header and rows
    header = ["Appl. No", "Ref. No.", "Due Date", "Due Date", "IHC", "G", "Examiner's Name", "Examiner's Phone Number"]  # Example column names
    rows = [
        # ["Row1-Value1", "Row1-Value2", "Row1-Value3"],
        # ["Row2-Value1", "Row2-Value2", "Row2-Value3"],
        # ["Row3-Value1", "Row3-Value2", "Row3-Value3"],
    ]

    # directory = input("Paste the path to the folder of OA PDFs you're looking at: ")
    #gets input

    #loops through input directory
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f):

            # Define the parent folder name
            parent_folder = "PatentOAs"

            # Get the absolute path
            absolute_path = os.path.abspath(f)

            # Split the path into components
            path_parts = absolute_path.split(os.path.sep)

            # Find the index of the parent folder
            if parent_folder in path_parts:
                parent_index = path_parts.index(parent_folder)
                # Get the last segment after the parent folder
                if parent_index + 1 < len(path_parts):
                    subfolder_name = path_parts[-1]  # This is the last part of the path
                else:
                    subfolder_name = ""
            else:
                subfolder_name = ""


            subfolder_name = str("MATERIALS FOR " + str(subfolder_name))
            subfolder_path = os.path.join(directory_name, subfolder_name)
            try:
                os.makedirs(subfolder_path)  # Use os.mkdir(directory_name) for a single directory
                print(f"Directory '{subfolder_path}' created successfully on Desktop.")
            except FileExistsError:
                print(f"Directory '{subfolder_path}' already exists.")
            except Exception as e:
                print(f"An error occurred: {e}")

            

            #f is pdfname
            obj = Solution()

            text = obj.extract_text_from_pdf(f)

            #here generate summary and put in subfolder_path

            prompt = f"Summarize this patent office action in a short paragraph:\n\n{text}"


            load_dotenv()

            client = OpenAI(
                # This is the default and can be omitted
                # api_key=os.environ.get("OPENAI_API_KEY"),
                api_key = os.getenv("OPENAI_API_KEY")
            )

            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": "Say this is a test",
                    }
                ],
                model="gpt-3.5-turbo",
            )

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            # {
                            #     "type": "image_url",
                            #     "image_url": {"url": f"{img_url}"},
                            # },
                        ],
                    }
                ],
            )

            
            # print(response)

            with open(subfolder_path + '/summary.txt', 'w') as summary_file:
                summary_file.write(response)


            obj.defineREGEX(text)

            print("ID: " + str(obj.applicationID))
            print("Refrence #: " + str(obj.refrenceNumber))
            print("DueDate: " + str(obj.dueDate))

            if obj.examinerName:
                arr = obj.examinerName.split(",")
                examinerRealName = ""
                examinerRealName += arr[1]
                examinerRealName += " "
                examinerRealName += arr[0]
            print("Examiner name: " + examinerRealName)

            # print("All refrences: " + str(obj.total_refs))
            # print("Phone #s: " + str(obj.phone_numbers))

            if obj.phone_numbers:
                examinerNumber = str(obj.phone_numbers)[24:-2]
                print("Examiner #: " + examinerNumber)

            rows.append([obj.applicationID, obj.refrenceNumber, "", obj.dueDate, "", "", examinerRealName, examinerNumber])

    # Create the CSV file and write the header and rows
    try:
        with open(csv_file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)  # Write the header
            writer.writerows(rows)    # Write the rows
        print(f"CSV file '{csv_file_path}' created successfully with header and rows.")
    except Exception as e:
        print(f"An error occurred while creating the CSV file: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python oa_processor.py <directory_path>")
        sys.exit(1)
    
    directory = sys.argv[1]
    main(directory)