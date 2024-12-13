import os
import zipfile
import glob
import sys

def compress_files(folder_path):
    patterns = ['*.json', '*.ndjson', '*.csv']
    files = []
    for pattern in patterns:
        files.extend(glob.glob(os.path.join(folder_path, pattern)))

    if not files:
        print("No JSON or NDJSON files found.")
        return

    for file in files:
        zip_path = f"{file}.zip"
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(file, os.path.basename(file))
        os.remove(file)
        print(f"Compressed and removed: {file}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python compress_files.py <folder_path>")
    else:
        compress_files(sys.argv[1])
