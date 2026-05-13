""" Merges a set of PDF files. """
import sys
import glob

from pypdf import PdfWriter

def find_pdf_files(args):
    """ finds files with the pattern """
    if len(args) == 1 and args[0].endswith('_'):
        pattern = args[0]
        return sorted(glob.glob(pattern + '*.pdf'))
    return args

def merge_pdfs(files, output_path="merged.pdf"):
    """ Merges a list of files. """
    if not files:
        raise ValueError("No PDF files provided.")
    writer = PdfWriter()
    for file in files:
        writer.append(file)
    writer.write(output_path)
    return output_path

def main():
    """ Collects arguments and makes the calls. """
    if len(sys.argv) < 2:
        print("Usage: python joinpdf.py <pattern e.g. file_ for file_01.pdf, "
              "file_02.pdf> or <file1> <file2> ...")
        return

    args = sys.argv[1:]
    files = find_pdf_files(args)
    print(files)
    if not files:
        print("No PDF files found.")
        return

    try:
        merge_pdfs(files, "merged.pdf")
    except FileNotFoundError as e:
        print(f"Error processing {e.filename}: {e}")
        return

    print("Merged PDF saved as merged.pdf")


if __name__ == "__main__":
    main()
