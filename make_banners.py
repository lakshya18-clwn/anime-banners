import os
import zipfile
from PIL import Image

# 1024x1024 HD Shield Canvas (16x Vanilla Resolution)
# Front face position: (32, 32), Size: (160, 320)
HD_CANVAS_SIZE = (1024, 1024)
HD_FRONT_POS = (32, 32)
HD_FACE_SIZE = (160, 320)

# Your exact mappings
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

def process_hd_shield(image_path):
    canvas = Image.new("RGBA", HD_CANVAS_SIZE, (0, 0, 0, 0))
    if os.path.exists(image_path):
        img = Image.open(image_path).convert("RGBA")
        
        # 1. Crop to shield ratio (160x320 -> 1:2)
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

        # 2. HD Lanczos Resampling
        front_img = img.resize(HD_FACE_SIZE, Image.Resampling.LANCZOS)

        # 3. Paste onto shield front face UV region
        canvas.paste(front_img, HD_FRONT_POS)
    else:
        print(f"Warning: File missing '{image_path}' — skipping.")
        
    return canvas

def generate_pack():
    pack_name = "AnimeShieldsPack"
    
    # Paths for Shield CIT
    cit_dir = os.path.join(pack_name, "assets", "minecraft", "optifine", "cit", "shields")
    os.makedirs(cit_dir, exist_ok=True)

    # 1. pack.mcmeta
    mcmeta = '''{
  "pack": {
    "pack_format": 34,
    "description": "HD Anime Shields for Minecraft 1.21"
  }
}'''
    with open(os.path.join(pack_name, "pack.mcmeta"), "w") as f:
        f.write(mcmeta)

    # 2. Process default shield_base.png (using black/karuizawa as default base)
    entity_dir = os.path.join(pack_name, "assets", "minecraft", "textures", "entity")
    os.makedirs(entity_dir, exist_ok=True)
    
    default_shield = process_hd_shield(BANNER_MAPPINGS["black"])
    default_shield.save(os.path.join(entity_dir, "shield_base.png"), "PNG")

    # 3. Generate CIT properties + textures for each character
    for color, filename in BANNER_MAPPINGS.items():
        if os.path.exists(filename):
            hd_shield = process_hd_shield(filename)
            tex_name = f"{color}_shield.png"
            hd_shield.save(os.path.join(cit_dir, tex_name), "PNG")

            # Create OptiFine / CIT Resewn properties file
            prop_content = f"type=item\nmatchItems=shield\ntexture={tex_name}\nnbt.display.Name=ippu:{color.capitalize()} Shield\n"
            with open(os.path.join(cit_dir, f"{color}_shield.properties"), "w") as f:
                f.write(prop_content)

    # 4. ZIP creation
    zip_filename = "AnimeShields_1.21.zip"
    with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(pack_name):
            for file in files:
                abs_path = os.path.join(root, file)
                rel_path = os.path.relpath(abs_path, pack_name)
                zipf.write(abs_path, rel_path)

    print(f"\nDone! Put '{zip_filename}' inside your resourcepacks folder.")

if __name__ == "__main__":
    generate_pack()
