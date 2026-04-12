import os
import shutil
import zipfile
DATASET_DIR = 'dataset'
KAGGLE_DATASET = 'techsash/waste-classification-data'
DOWNLOAD_DIR = 'kaggle_download'
CLASS_MAPPING = {'PLASTIC': 'Plastic', 'PAPER': 'Paper', 'METAL': 'Metal'}

def check_kaggle():
    try:
        import kaggle
    except ImportError:
        print("ERROR: 'kaggle' package not found.")
        print('Install it with:  pip install kaggle')
        return False
    kaggle_json = os.path.expanduser('~/.kaggle/kaggle.json')
    if not os.path.exists(kaggle_json):
        print('ERROR: Kaggle API credentials not found.')
        print(f'Expected at: {kaggle_json}')
        print('\nTo fix:')
        print('  1. Go to https://www.kaggle.com → Account → Create API Token')
        print('  2. Download kaggle.json')
        print(f'  3. Move it to: {kaggle_json}')
        print('  4. Run:  chmod 600 ~/.kaggle/kaggle.json   (Mac/Linux)')
        return False
    return True

def download_and_extract():
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    print(f"[download] Downloading '{KAGGLE_DATASET}' from Kaggle...")
    import kaggle
    kaggle.api.authenticate()
    kaggle.api.dataset_download_files(KAGGLE_DATASET, path=DOWNLOAD_DIR, unzip=True)
    print(f"[download] Downloaded and extracted to '{DOWNLOAD_DIR}/'")

def reorganise_into_dataset():
    print(f"\n[reorganise] Organising into '{DATASET_DIR}/' ...")
    for dest_folder in CLASS_MAPPING.values():
        os.makedirs(os.path.join(DATASET_DIR, dest_folder), exist_ok=True)
    counts = {v: 0 for v in CLASS_MAPPING.values()}
    for root, dirs, files in os.walk(DOWNLOAD_DIR):
        for filename in files:
            if not filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                continue
            upper_root = root.upper()
            matched_class = None
            for kaggle_name, our_name in CLASS_MAPPING.items():
                if kaggle_name in upper_root:
                    matched_class = our_name
                    break
            if matched_class is None:
                continue
            src = os.path.join(root, filename)
            dest = os.path.join(DATASET_DIR, matched_class, filename)
            if os.path.exists(dest):
                base, ext = os.path.splitext(filename)
                dest = os.path.join(DATASET_DIR, matched_class, f'{base}_{counts[matched_class]}{ext}')
            shutil.copy2(src, dest)
            counts[matched_class] += 1
    return counts

def cleanup():
    if os.path.exists(DOWNLOAD_DIR):
        shutil.rmtree(DOWNLOAD_DIR)
        print(f"[cleanup] Removed temporary folder '{DOWNLOAD_DIR}/'")

def main():
    print('=' * 55)
    print('  Real Waste Dataset Downloader (Kaggle)')
    print('=' * 55)
    if not check_kaggle():
        return
    download_and_extract()
    counts = reorganise_into_dataset()
    cleanup()
    print(f"\n{'=' * 55}")
    print('  Dataset Ready!')
    print(f"  Folder: '{DATASET_DIR}/'")
    for class_name, count in counts.items():
        print(f'  ├── {class_name}/  ({count} images)')
    print(f'\n  Now run: python train.py')
    print('=' * 55)
if __name__ == '__main__':
    main()