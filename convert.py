import os
from pdf2image import convert_from_path
from PIL import Image

os.makedirs("slices", exist_ok=True)
os.makedirs("comic_pages", exist_ok=True)

print("Loading PDF with explicit poppler...")
# EXPLICIT POPPLER PATH - fixes "Terminated" crash
images = convert_from_path("webtoon.pdf", dpi=120, 
                          poppler_path='/usr/bin')  # Standard Ubuntu path

print(f"Loaded {len(images)} pages!")
slice_height = 1400
slice_index = 0

# STEP 1 — Slice vertical webtoon pages
for img in images:
    width, height = img.size
    y = 0
    while y < height:
        crop = img.crop((0, y, width, min(y + slice_height, height)))
        crop.save(f"slices/slice_{slice_index}.png")
        slice_index += 1
        y += slice_height
print("Vertical slicing done")

# STEP 2 — Single column (1+2 per page)
# page_width, page_height = 1800, 2600
# cols, rows_per_page = 1, 2  # YOUR REQUEST
# panel_width, panel_height = 850, 850
# h_spacing, v_spacing = 25, 25

# Auto-fit panels to fill page completely
page_width, page_height = 1800, 2600
cols, rows_per_page = 1, 2
panel_width = page_width - 50      # Full width minus tiny margin
panel_height = (page_height - 75) // 2  # Split height evenly
h_spacing = 0
v_spacing = 25


slice_files = sorted(os.listdir("slices"))
page_number = 0

for i in range(0, len(slice_files), cols * rows_per_page):
    page = Image.new("RGB", (page_width, page_height), "white")
    col, row = 0, 0
    
    for j in range(i, min(i + cols * rows_per_page, len(slice_files))):
        file = slice_files[j]
        img = Image.open(f"slices/{file}")
        img_resized = img.resize((panel_width, panel_height), Image.Resampling.LANCZOS)
        x = col * (panel_width + h_spacing)
        y = row * (panel_height + v_spacing)
        page.paste(img_resized, (x, y))
        row += 1
        if row == rows_per_page:
            row = 0
            col += 1
    
    page.save(f"comic_pages/page_{page_number}.png")
    page_number += 1
    print(f"Created page_{page_number}.png")

print("Perfect single-column pages ready!")
