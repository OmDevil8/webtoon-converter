import cv2
import numpy as np
from pdf2image import convert_from_path
from PIL import Image
import os

os.makedirs("pages", exist_ok=True)
os.makedirs("panels", exist_ok=True)
os.makedirs("comic_pages", exist_ok=True)

images = convert_from_path("webtoon.pdf")

for i, img in enumerate(images):
    img.save(f"pages/page_{i}.png")

panel_count = 0

for file in os.listdir("pages"):
    img = cv2.imread("pages/" + file)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    thresh = cv2.threshold(gray,240,255,cv2.THRESH_BINARY)[1]

    projection = np.sum(thresh,axis=1)

    cuts=[]
    for i in range(len(projection)):
        if projection[i] > 0.95*max(projection):
            cuts.append(i)

    start=0

    for cut in cuts:
        panel = img[start:cut,:]

        if panel.shape[0] > 150:
            cv2.imwrite(f"panels/panel_{panel_count}.png",panel)
            panel_count +=1

        start=cut

panel_files = sorted(os.listdir("panels"))

page_width=1600
page_height=2400

x=0
y=0
row_height=0

page = Image.new("RGB",(page_width,page_height),"white")
page_number=0

for panel_file in panel_files:

    panel = Image.open("panels/"+panel_file)
    panel.thumbnail((800,800))

    if x+panel.width > page_width:
        x=0
        y += row_height + 20
        row_height=0

    if y+panel.height > page_height:
        page.save(f"comic_pages/page_{page_number}.png")
        page_number +=1
        page = Image.new("RGB",(page_width,page_height),"white")
        x=0
        y=0

    page.paste(panel,(x,y))

    x += panel.width + 20
    row_height = max(row_height,panel.height)

page.save(f"comic_pages/page_{page_number}.png")

print("Finished!")