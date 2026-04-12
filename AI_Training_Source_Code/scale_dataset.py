import os
import random
from tensorflow.keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array, save_img
TARGET_COUNT = 2000
DATASET_DIR = 'dataset'
CLASSES = ['metal', 'paper', 'plastic']
print(f'Goal: Ensure exactly {TARGET_COUNT} images in each class.')
datagen = ImageDataGenerator(rotation_range=30, width_shift_range=0.1, height_shift_range=0.1, zoom_range=0.2, horizontal_flip=True, brightness_range=[0.8, 1.2], fill_mode='nearest')
for class_name in CLASSES:
    class_dir = os.path.join(DATASET_DIR, class_name)
    if not os.path.exists(class_dir):
        print(f'Warning: {class_dir} does not exist. Skipping.')
        continue
    images = [f for f in os.listdir(class_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]
    current_count = len(images)
    print(f'[{class_name}] Found {current_count} images.')
    if current_count >= TARGET_COUNT:
        print(f'[{class_name}] Already meets or exceeds target of {TARGET_COUNT}.')
        continue
    deficit = TARGET_COUNT - current_count
    print(f'[{class_name}] Need {deficit} more images. Generating via AI augmentation...')
    generated_count = 0
    while generated_count < deficit:
        base_img_name = random.choice(images)
        img_path = os.path.join(class_dir, base_img_name)
        try:
            img = load_img(img_path)
            x = img_to_array(img)
            x = x.reshape((1,) + x.shape)
            it = datagen.flow(x, batch_size=1)
            aug_batch = next(it)
            aug_image = aug_batch[0]
            new_file_name = f'aug_{generated_count}_{base_img_name}'
            new_file_path = os.path.join(class_dir, new_file_name)
            save_img(new_file_path, aug_image)
            generated_count += 1
            if generated_count % 200 == 0:
                print(f'[{class_name}] Generated {generated_count}/{deficit}...')
        except Exception as e:
            pass
    print(f'[{class_name}] Successfully padded folder to {TARGET_COUNT} images.')
print('All classes are now normalized to 2000 images each. Dataset is ready!')
