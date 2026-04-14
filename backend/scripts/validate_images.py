import os
import sys

EXERCISE_ROOT = r"C:\Users\cruci\Coding projects\Exercise data\exercises"

def validate_image_folders():
    print("=== VALIDATING EXERCISE IMAGE FOLDERS ===\n")

    errors_found = False

    for folder_name in os.listdir(EXERCISE_ROOT):
        folder_path = os.path.join(EXERCISE_ROOT, folder_name)
        images_path = os.path.join(folder_path, "images")

        # Skip if no images folder
        if not os.path.isdir(images_path):
            print(f"[ERROR] {folder_name}: missing images/ folder")
            errors_found = True
            continue

        files = os.listdir(images_path)
        jpg_files = [f for f in files if f.lower().endswith(".jpg")]

        # Rule 1: Must have exactly 2 JPGs
        if len(jpg_files) != 2:
            print(f"[ERROR] {folder_name}: expected 2 images, found {len(jpg_files)} → {jpg_files}")
            errors_found = True
            continue

        # Rule 2: Must contain 0.jpg and 1.jpg
        if "0.jpg" not in jpg_files or "1.jpg" not in jpg_files:
            print(f"[ERROR] {folder_name}: missing required 0.jpg or 1.jpg → {jpg_files}")
            errors_found = True
            continue

        print(f"[OK] {folder_name}: valid image set")

    print("\n=== VALIDATION COMPLETE ===")

    if errors_found:
        print("\n❌ Errors detected — ingestion should NOT run.")
        sys.exit(1)
    else:
        print("\n✅ All folders valid — safe to run ingestion.")

if __name__ == "__main__":
    validate_image_folders()