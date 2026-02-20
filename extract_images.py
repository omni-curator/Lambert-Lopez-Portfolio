#!/usr/bin/env python3
"""
Extract images from LambertLopez_Portfolio.pdf and optimize them.
"""

import os
import sys
from pathlib import Path

try:
    import fitz  # PyMuPDF
    from PIL import Image
    import io
except ImportError as e:
    print(f"❌ Missing required library: {e}")
    print("Installing dependencies...")
    os.system("pip install PyMuPDF Pillow")
    import fitz
    from PIL import Image
    import io

def extract_and_optimize_images(pdf_path, output_dir):
    """Extract images from PDF and optimize them."""
    
    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Image naming map based on typical portfolio content
    naming_map = {
        0: "lambert-graphic-design-cover",
        1: "digital-portrait-hijab",
        2: "casino-banners",
        3: "posters-labour-day",
        4: "posters-pi-mai-lao",
        5: "tshirt-wiz-khalifa",
        6: "family-portrait-vector",
        7: "embroidery-ai-mockup",
        8: "embroidery-ps-mockup",
        9: "ornament-3d",
        10: "creatives-iron-mindset",
    }
    
    try:
        # Open PDF document
        pdf_doc = fitz.open(pdf_path)
        print(f"📄 Opened PDF: {pdf_path}")
        print(f"📖 Total pages: {len(pdf_doc)}")
        
        image_count = 0
        extracted_images = []
        
        # Iterate through all pages
        for page_num in range(len(pdf_doc)):
            page = pdf_doc[page_num]
            
            # Get all images on this page
            image_list = page.get_images()
            
            if image_list:
                print(f"\n📍 Page {page_num + 1}: Found {len(image_list)} image(s)")
            
            for img_index, img in enumerate(image_list):
                try:
                    # Extract image
                    xref = img[0]
                    pix = fitz.Pixmap(pdf_doc, xref)
                    
                    # Convert CMYK to RGB if needed
                    if pix.n - pix.alpha < 4:  # RGB or Grayscale
                        img_data = pix.tobytes("ppm")
                    else:  # CMYK
                        pix = fitz.Pixmap(fitz.csRGB, pix)
                        img_data = pix.tobytes("ppm")
                    
                    # Load image with PIL
                    img_pil = Image.open(io.BytesIO(img_data))
                    
                    # Get filename
                    if image_count in naming_map:
                        base_name = naming_map[image_count]
                    else:
                        base_name = f"portfolio-image-{image_count}"
                    
                    filename = f"{base_name}.jpg"
                    filepath = os.path.join(output_dir, filename)
                    
                    # Get original size
                    original_size = img_pil.size
                    
                    # Resize if needed (max 1200px on longest side)
                    max_size = 1200
                    if max(original_size) > max_size:
                        ratio = max_size / max(original_size)
                        new_size = (int(original_size[0] * ratio), int(original_size[1] * ratio))
                        img_pil = img_pil.resize(new_size, Image.Resampling.LANCZOS)
                        print(f"  ✓ {filename}: Resized from {original_size} to {new_size}")
                    else:
                        print(f"  ✓ {filename}: {original_size} (original size)")
                    
                    # Save as JPEG with 85% quality
                    img_pil.convert('RGB').save(filepath, 'JPEG', quality=85, optimize=True)
                    
                    extracted_images.append({
                        'name': filename,
                        'path': filepath,
                        'size': os.path.getsize(filepath)
                    })
                    
                    image_count += 1
                    
                except Exception as e:
                    print(f"  ❌ Error processing image {img_index} on page {page_num + 1}: {e}")
        
        pdf_doc.close()
        
        # Print summary
        print(f"\n{'=' * 60}")
        print(f"✅ IMAGE EXTRACTION COMPLETE")
        print(f"{'=' * 60}")
        print(f"📊 Total images extracted: {image_count}")
        print(f"📁 Output directory: {output_dir}\n")
        
        for i, img in enumerate(extracted_images, 1):
            size_kb = img['size'] / 1024
            print(f"{i:2d}. {img['name']:<40s} {size_kb:7.1f} KB")
        
        return extracted_images
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return []

if __name__ == "__main__":
    # Set paths
    pdf_path = r"c:\Users\TRACEWORK\OneDrive\Documents\Tracework_Developing_Apps\Portfolio\assets\portfolio\LambertLopez_Portfolio.pdf"
    output_dir = r"c:\Users\TRACEWORK\OneDrive\Documents\Tracework_Developing_Apps\Portfolio\assets\portfolio"
    
    # Extract and optimize images
    extract_and_optimize_images(pdf_path, output_dir)
