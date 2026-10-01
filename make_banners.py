import os
import zipfile
from PIL import Image

HD_CANVAS_SIZE = (512, 512)
HD_FRONT_POS = (16, 16)
HD_BACK_POS = (176, 16)
HD_BANNER_SIZE = (160, 320)

BANNER_MAPPINGS = {
    "light_gray": "cha hae in banner 2.jpg",
    "gray": "makima red_banner.jpg",
    "black": "karuizawa1.jpg",
    "red": "makima black_banner.jpg",
    "white": "ichinose.jpg",
    "brown": "nobara.jpg",
    "green": "ichinose2.jpg",
    "magenta": "hancock.jpg",
    "orange": "nami2.jpg",
    "yellow": "cha hae in banner 3.jpg",
    "lime": "marin_kitagawa_banner.jpg",
    "light_blue": "shoko.jpg",
    "blue": "robin1.jpg",
    "purple": "reze.jpg",
    "cyan": "chahaein.jpg",
    "pink": "marin1.jpg"
}

def process_hd_banner(image_path):
    canvas = Image.new("RGBA", HD_CANVAS_SIZE, (0, 0, 0, 0))
    if os.path.exists(image_path):
        img = Image.open(image_path).convert("RGBA")
        w, h = img.size
        target_ratio = 160 / 320
        img_ratio = w / h

        if img_ratio > target_ratio:
            new_w = int(h * target_ratio)
            left = (w - new_w) // 2
            img = img.crop((left, 0, left + new_w, h))
        else:
            new_h = int(w / target_ratio)
            top = (h - new_h) // 2
            img = img.crop((0, top, w, top + new_h))

        front_img = img.resize(HD_BANNER_SIZE, Image.Resampling.LANCZOS)
        back_img = front_img.transpose(Image.FLIP_LEFT_RIGHT)

        canvas.paste(front_img, HD_FRONT_POS)
        canvas.paste(back_img, HD_BACK_POS)
    return canvas

def generate_pack():
    pack_name = "AnimeBannersPack"
    banner_dir = os.path.join(pack_name, "assets", "minecraft", "textures", "entity", "banner")
    os.makedirs(banner_dir, exist_ok=True)

    mcmeta = '''{
  "pack": {
    "pack_format": 34,
    "description": "HD Anime Banners for Minecraft 1.21"
  }
}'''
    with open(os.path.join(pack_name, "pack.mcmeta"), "w") as f:
        f.write(mcmeta)

    for color, filename in BANNER_MAPPINGS.items():
        hd_banner = process_hd_banner(filename)
        output_path = os.path.join(banner_dir, f"{color}.png")
        hd_banner.save(output_path, "PNG")

    zip_filename = "AnimeBanners_1.21.zip"
    with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(pack_name):
            for file in files:
                abs_path = os.path.join(root, file)
                rel_path = os.path.relpath(abs_path, pack_name)
                zipf.write(abs_path, rel_path)

if __name__ == "__main__":
    generate_pack()
