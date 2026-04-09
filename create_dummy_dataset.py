import os
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
DATASET_DIR = 'dataset'
IMAGES_PER_CLASS = 100
IMG_SIZE = (224, 224)
CLASS_CONFIG = {'Plastic': {'colors': [(30, 120, 220), (220, 50, 50), (50, 200, 80), (255, 200, 0), (180, 80, 200)], 'description': 'Colorful solid-colored images (simulating plastic bottles/bags)'}, 'Paper': {'colors': [(240, 230, 215), (210, 195, 170), (250, 240, 220), (200, 185, 160), (235, 225, 210)], 'description': 'Light beige/cream images (simulating paper/cardboard)'}, 'Metal': {'colors': [(150, 155, 160), (120, 125, 130), (170, 175, 180), (140, 145, 140), (160, 160, 170)], 'description': 'Grey-toned images (simulating metal cans/foil)'}}

def create_plastic_image(color, size):
    img = Image.new('RGB', size, color)
    draw = ImageDraw.Draw(img)
    for _ in range(random.randint(3, 8)):
        x1 = random.randint(0, size[0] - 40)
        y1 = random.randint(0, size[1] - 40)
        x2 = x1 + random.randint(20, 80)
        y2 = y1 + random.randint(20, 80)
        darker = tuple((max(0, c - random.randint(20, 50)) for c in color))
        draw.ellipse([x1, y1, x2, y2], fill=darker, outline=None)
    img = img.filter(ImageFilter.GaussianBlur(radius=1))
    return img

def create_paper_image(color, size):
    base = np.full((size[1], size[0], 3), color, dtype=np.uint8)
    noise = np.random.randint(-15, 15, base.shape, dtype=np.int16)
    base = np.clip(base.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    img = Image.fromarray(base)
    draw = ImageDraw.Draw(img)
    for y in range(0, size[1], random.randint(15, 25)):
        line_color = tuple((max(0, c - random.randint(5, 20)) for c in color))
        draw.line([(0, y), (size[0], y)], fill=line_color, width=1)
    img = img.filter(ImageFilter.SMOOTH)
    return img

def create_metal_image(color, size):
    base = np.zeros((size[1], size[0], 3), dtype=np.uint8)
    for y in range(size[1]):
        brightness = int(255 * (y / size[1]) * 0.3)
        row_color = tuple((min(255, c + brightness) for c in color))
        base[y, :] = row_color
    img = Image.fromarray(base)
    draw = ImageDraw.Draw(img)
    for _ in range(random.randint(5, 15)):
        x1 = random.randint(0, size[0])
        x2 = random.randint(0, size[0])
        y1 = random.randint(0, size[1])
        y2 = random.randint(0, size[1])
        scratch_color = tuple((min(255, c + random.randint(30, 70)) for c in color))
        draw.line([(x1, y1), (x2, y2)], fill=scratch_color, width=random.randint(1, 2))
    img = img.filter(ImageFilter.SMOOTH_MORE)
    return img
GENERATORS = {'Plastic': create_plastic_image, 'Paper': create_paper_image, 'Metal': create_metal_image}

def generate_dataset():
    print('=' * 50)
    print('  Generating Synthetic Dummy Dataset')
    print('=' * 50)
    total = 0
    for class_name, config in CLASS_CONFIG.items():
        class_dir = os.path.join(DATASET_DIR, class_name)
        os.makedirs(class_dir, exist_ok=True)
        generator = GENERATORS[class_name]
        print(f'\n[{class_name}] Generating {IMAGES_PER_CLASS} images...')
        print(f"  → {config['description']}")
        for i in range(IMAGES_PER_CLASS):
            color = random.choice(config['colors'])
            color = tuple((min(255, max(0, c + random.randint(-20, 20))) for c in color))
            img = generator(color, IMG_SIZE)
            filename = f'{class_name.lower()}_{i + 1:04d}.jpg'
            filepath = os.path.join(class_dir, filename)
            img.save(filepath, 'JPEG', quality=90)
            total += 1
        print(f"  ✔ {IMAGES_PER_CLASS} images saved to '{class_dir}/'")
    print(f"\n{'=' * 50}")
    print(f'  Dataset Ready! Total images: {total}')
    print(f"  Folder: '{DATASET_DIR}/'")
    print(f'  ├── Plastic/  ({IMAGES_PER_CLASS} images)')
    print(f'  ├── Paper/    ({IMAGES_PER_CLASS} images)')
    print(f'  └── Metal/    ({IMAGES_PER_CLASS} images)')
    print(f'\n  Now run: python train.py')
    print('=' * 50)
if __name__ == '__main__':
    generate_dataset()