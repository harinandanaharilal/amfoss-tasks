import os
import glob
import re
import cv2
import numpy as np
from PIL import Image

def extract_row_number(filename):
    """Sorts row-1, row-2 ... row-10 in exact numerical order."""
    match = re.search(r'row-(\d+)', filename)
    return int(match.group(1)) if match else 0

def load_fragmented_images(image_folder):
    """Loads all fragment images from the target directory in correct numerical order."""
    file_pattern = os.path.join(image_folder, "*.jpg")
    filepaths = glob.glob(file_pattern)

    if not filepaths:
        file_pattern = os.path.join(image_folder, "*.jpeg")
        filepaths = glob.glob(file_pattern)

    
    filepaths = sorted(filepaths, key=extract_row_number)
    
    images = []
    for fp in filepaths:
        img = cv2.imread(fp)
        if img is not None:
            images.append(img)
            
    print(f"[Imperial Intelligence] Loaded {len(images)} fragment(s) from {image_folder}.")
    return images

def reassemble_imperial_transmission(fragment_folder, output_path):
    print("=" * 65)
    print("GALACTIC EMPIRE FLEET COMMAND — REINHARD VON LOHENGRAMM")
    print("OBJECTIVE: Decrypt and stitch split transmission fragments.")
    print("=" * 65)

    fragments = load_fragmented_images(fragment_folder)

    if not fragments:
        print("[Error] No transmission fragments detected.")
        return

    
    canvas_np = np.vstack(fragments)

    
    canvas_rgb = cv2.cvtColor(canvas_np, cv2.COLOR_BGR2RGB)
    reconstructed_img = Image.fromarray(canvas_rgb)

    
    reconstructed_img.save(output_path)
    print(f"\n[Success] Reconstruction complete! Output saved as: {output_path}")

if __name__ == "__main__":
    
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    OUTPUT_FILE = os.path.join(SCRIPT_DIR, "secret_imperial_message.jpg")
    
    reassemble_imperial_transmission(SCRIPT_DIR, OUTPUT_FILE)
