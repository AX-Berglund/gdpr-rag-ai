import os
import re
import sys
from PyPDF2 import PdfReader # accurate in layout, bad in language extraction
from pdfminer.high_level import extract_text # accurate in language, bad in layout extraction
from itertools import zip_longest


def extract_text_pypdf2(pdf_path, output_txt_path):
    """
    Extracts text from a PDF file using PyPDF2 and saves it to a .txt file.

    :param pdf_path: Path to the PDF file
    :param output_txt_path: Path to save the extracted text
    """
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()

    with open(output_txt_path, "w", encoding="utf-8") as txt_file:
        txt_file.write(text)

    print(f"Text extracted from PDF using PyPDF2 and saved to {output_txt_path}")



def extract_text_pdfminer(pdf_path, output_txt_path):
    """
    Extracts text from a PDF file using pdfminer.six, filters out empty lines, and saves it to a .txt file.

    :param pdf_path: Path to the PDF file
    :param output_txt_path: Path to save the extracted text
    """
    # Extract text using pdfminer.six
    text = extract_text(pdf_path)

    # Filter out empty lines
    filtered_text = "\n".join([line for line in text.splitlines() if line.strip()])

    # Write the filtered text to a .txt file
    with open(output_txt_path, "w", encoding="utf-8") as txt_file:
        txt_file.write(filtered_text)

    print(f"Text extracted from PDF using pdfminer and saved to {output_txt_path}")

def remove_spaces_from_file(input_file_path, output_file_path):
    """
    Reads a .txt file, removes all spaces, and writes the modified content to a new file.

    :param input_file_path: Path to the input .txt file
    :param output_file_path: Path to save the output .txt file without spaces
    """
    try:
        with open(input_file_path, 'r') as file:
            # Read the entire file content
            content = file.read()

        # Remove all spaces
        content_without_spaces = content.replace(' ', '')

        with open(output_file_path, 'w') as file:
            # Write the content without spaces to the new file
            file.write(content_without_spaces)

        print(f"Successfully removed spaces from: {input_file_path} Output saved to: {output_file_path}")

    except FileNotFoundError:
        print(f"Error: The file '{input_file_path}' does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")


def fix_lines_algorithm(file1, file2, file3, file4, output_file):
    """
    Reads four input files, performs line matching and updates lines based on matches, 
    then writes the result to an output file.

    :param file1: Path to the first input file
    :param file2: Path to the second input file
    :param file3: Path to the third input file
    :param file4: Path to the fourth input file
    :param output_file: Path to the output file
    """
    # Read all files
    with open(file1, 'r') as f1, open(file2, 'r') as f2, open(file3, 'r') as f3, open(file4, 'r') as f4:
        lines1 = f1.readlines()
        lines2 = f2.readlines()
        lines3 = f3.readlines()
        lines4 = f4.readlines()

    # Build a lookup dictionary for lines2 and lines4 for fast matching
    lines2_dict = {line: idx for idx, line in enumerate(lines2)}

    max_len = max(len(lines1), len(lines2), len(lines3), len(lines4))
    result_lines = []

    for i, (line1, line3) in enumerate(zip_longest(lines1, lines3, fillvalue='')):
        updated_line = line3
        if line1 in lines2_dict:  # Exact match
            updated_line = lines4[lines2_dict[line1]]
        else:  # Perform partial matches
            prefix_match = None
            suffix_match = None
            for idx, line2 in enumerate(lines2):
                if line1[3:] == line2:
                    suffix_match = idx
                elif line1[:20] == line2[:20]:
                    prefix_match = idx
                # Break early if both matches found
                if suffix_match and prefix_match:
                    break

            if suffix_match is not None:
                updated_line = line1[:3] + "   " + lines4[suffix_match]
            elif prefix_match is not None:
                updated_line = lines4[prefix_match]

        result_lines.append(updated_line)

    # Write output
    with open(output_file, 'w') as f_out:
        f_out.writelines(result_lines)

    print(f"Successfully fixed lines and saved to: {output_file}")

# Removes footnotes and headers from the dropped spaces text file
def remove_repeating_strings(input_file, output_file):
    """
    Removes all instances of the string pattern '4.5.2016L119/xOfficialJournaloftheEuropeanUnionEN'
    where 'x' iterates from 1 to 119, and replaces them with an empty string.
    Args:
        input_file (str): Path to the input .txt file.
        output_file (str): Path to save the modified .txt file.
    """
    # Regex pattern to match '4.5.2016L119/xOfficialJournaloftheEuropeanUnionEN' where x is 1-119
    pattern = re.compile(r"4\.5\.2016L119/\d{1,3}OfficialJournaloftheEuropeanUnionEN")
    
    with open(input_file, "r", encoding="utf-8") as file:
        content = file.read()

    # Replace all matches with an empty string
    modified_content = re.sub(pattern, "", content)

    # Write the modified content to the output file
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(modified_content)
    
    print(f"All matching patterns removed. Output saved to {output_file}")




def split_txt_by_articles(input_file, output_dir):
    """
    Splits a text file into separate files, one per article, based on the occurrence of 'Article x' followed by a newline.
    Args:
        input_file (str): Path to the input .txt file.
        output_dir (str): Directory to save the output files.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)  # Create the output directory if it doesn't exist

    with open(input_file, "r", encoding="utf-8") as file:
        lines = file.readlines()
    
    article_pattern = re.compile(r"^Article\s+(\d+)\s*\n", re.IGNORECASE)
    current_article = None
    content = []
    article_count = 0

    for line in lines:
        match = article_pattern.match(line)
        if match:
            # Save the previous article to a file
            if current_article is not None:
                output_file = os.path.join(output_dir, f"gdpr_article_{current_article}.txt")
                with open(output_file, "w", encoding="utf-8") as out_file:
                    out_file.writelines(content)
                article_count += 1
                # Update the console line
                sys.stdout.write(f"\rSaved articles: {article_count}")
                sys.stdout.flush()
            
            # Start a new article
            current_article = match.group(1)
            content = [line]
        else:
            content.append(line)
    
    # Save the last article
    if current_article is not None:
        output_file = os.path.join(output_dir, f"gdpr_article_{current_article}.txt")
        with open(output_file, "w", encoding="utf-8") as out_file:
            out_file.writelines(content)
        article_count += 1
        # Final update to the console line
        sys.stdout.write(f"\rSaved articles: {article_count}\n")
        sys.stdout.flush()
    sys.stdout.write(f"\rSaved articles: {article_count}\n")
    sys.stdout.flush()





def pdf_to_txt(pdf_path):
    pypdf2_text_path = "../../data/text/pypdf2.txt"
    pdfminer_text_path = "../../data/text/pdfminer.txt"

    extract_text_pypdf2(pdf_path, pypdf2_text_path) 
    extract_text_pdfminer(pdf_path, pdfminer_text_path)

    return pypdf2_text_path, pdfminer_text_path



def preprocess_raw_textfiles(pypdf2_text_path, pdfminer_text_path):
    # Step 2: Remove spaces from extracted text files
    pypdf2_spaceDrop = "../../data/text/pypdf2_dropped_spaces.txt"
    pdfminer_spaceDrop = "../../data/text/pdfminer_dropped_spaces.txt"

    remove_spaces_from_file(pypdf2_text_path, pypdf2_spaceDrop)
    remove_spaces_from_file(pdfminer_text_path, pdfminer_spaceDrop)

    # Step 3: Remove repeating strings from the cleaned PyPDF2 text
    pypdf2_spaceDrop_cleaned = "../../data/text/pypdf2_dropped_spaces_cleaned.txt"
    remove_repeating_strings(pypdf2_spaceDrop, pypdf2_spaceDrop_cleaned)

    # Step 4: Fix line inconsistencies and combine cleaned outputs
    # This function combines the best from both PyPDF2 and PDFMiner extracts
    # Combine layout from PyPDF2 and language from PDFMiner
    final_output_path = '../../data/text/gdpr_2016.txt'
    fix_lines_algorithm(
        pypdf2_spaceDrop_cleaned,
        pdfminer_spaceDrop,
        pypdf2_text_path,
        pdfminer_text_path,
        final_output_path
    )

    return final_output_path


    

def main():
    # Define file paths
    pdf_path = "../../data/pdf/gdpr_2016.pdf"
    

    # Step 1: Extract text from the PDF file (in 2 different ways)
    txt1_path, txt2_path = pdf_to_txt(pdf_path)

    # Step 2: Preprocess the extracted text files
    txt_path = preprocess_raw_textfiles(txt1_path, txt2_path) # see file "gdpr_2016.txt"

    # Step 5: Split the final cleaned text into articles files
    split_output_dir = '../../data/text/split_articles'
    split_txt_by_articles(txt_path, split_output_dir)




if __name__ == "__main__":
    main()

