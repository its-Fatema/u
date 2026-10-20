from pathlib import Path
from PIL import Image, ImageDraw
import math

root = Path("pixel-crawler/Pixel Crawler - Free Pack")
out = Path("contact_sheets")
out.mkdir(exist_ok=True)

files = sorted(
    p for p in root.rglob("*.png")
    if p.is_file()
)

print(f"Found {len(files)} PNG files")

batch_size = 48
cell_w, cell_h = 180, 150
cols = 6

for start in range(0, len(files), batch_size):
    batch = files[start:start + batch_size]
    rows = math.ceil(len(batch) / cols)
    sheet = Image.new(
        "RGB", (cols * cell_w, rows * cell_h), "#333333"
    )
    draw = ImageDraw.Draw(sheet)

    for i, path in enumerate(batch):
        im = Image.open(path).convert("RGBA")
        original_size = im.size
        im.thumbnail((cell_w - 12, 100), Image.Resampling.NEAREST)

        x = (i % cols) * cell_w
        y = (i // cols) * cell_h

        draw.rectangle(
            (x + 3, y + 3, x + cell_w - 4, y + 108),
            fill="#555555"
        )
        sheet.paste(
            im,
            (x + (cell_w - im.width) // 2,
             y + 5 + (100 - im.height) // 2),
            im
        )

        relative = str(path.relative_to(root))
        label = relative[-42:]
        draw.text((x + 5, y + 111), label, fill="white")
        draw.text(
            (x + 5, y + 130),
            f"{original_size[0]} x {original_size[1]}",
            fill="#cccccc"
        )

    name = f"sheet-{start // batch_size + 1:03}.jpg"
    sheet.save(out / name, quality=90)
    print(f"Created {out / name}")

print("Done. Contact sheets are in contact_sheets/")
