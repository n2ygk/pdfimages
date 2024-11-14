#!/usr/bin/env python3
import fitz  # PyMuPDF
import os
import argparse

def extract_images_from_pdf(pdf_path, output_folder="extracted_images"):
    """Extracts images from a single PDF and saves them to the specified folder."""
    # Get the base name of the PDF file without extension for prefixing
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
    pdf_document = fitz.open(pdf_path)
    image_count = 0

    # Loop through each page
    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]
        
        # Get the images on each page
        images = page.get_images(full=True)
        
        for image_index, img in enumerate(images):
            # Get the image XREF
            xref = img[0]
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]

            # Define the output image file path with the PDF name as a prefix
            image_filename = f"{output_folder}/{pdf_name}_page_{page_num+1}_image_{image_index+1}.{image_ext}"
            
            # Write the image bytes to file
            with open(image_filename, "wb") as image_file:
                image_file.write(image_bytes)
            
            print(f"Extracted image: {image_filename}")
            image_count += 1

    pdf_document.close()
    print(f"Total images extracted from {pdf_path}: {image_count}")

def main(pdf_paths):
    # Create the output folder if it doesn't exist
    output_folder = "extracted_images"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Process each PDF file in the list
    for pdf_path in pdf_paths:
        extract_images_from_pdf(pdf_path, output_folder=output_folder)

if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Extract images from multiple PDF files.")
    parser.add_argument("pdf_paths", nargs="+", help="Paths to the PDF files from which to extract images")
    args = parser.parse_args()
    
    # Extract images from the provided PDF paths
    main(args.pdf_paths)
