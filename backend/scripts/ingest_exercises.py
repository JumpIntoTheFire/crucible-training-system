import os
import json
import shutil
from sqlalchemy.orm import Session
from backend.models import SessionLocal, Exercise

# Source: raw exercise data. Set EXERCISE_ROOT env var or update default path.
EXERCISE_ROOT = os.environ.get(
    "EXERCISE_ROOT",
    r"C:\Users\cruci\Coding_Projects\Exercise data\exercises"
)

# Destination: FastAPI static folder (served via /images)
STATIC_IMAGE_ROOT = os.path.join(
    os.path.dirname(__file__), "..", "static", "images"
)


def ingest_exercises():
    if not os.path.isdir(EXERCISE_ROOT):
        raise RuntimeError(f"EXERCISE_ROOT not found: {EXERCISE_ROOT}")

    db: Session = SessionLocal()
    inserted = 0
    skipped = 0

    for folder_name in sorted(os.listdir(EXERCISE_ROOT)):
        folder_path = os.path.join(EXERCISE_ROOT, folder_name)
        if not os.path.isdir(folder_path):
            continue

        json_path = os.path.join(folder_path, "exercise.json")
        if not os.path.isfile(json_path):
            print(f"[SKIP] No JSON: {folder_name}")
            skipped += 1
            continue

        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"[SKIP] Bad JSON in {folder_name}: {e}")
            skipped += 1
            continue

        required = ["name", "primaryMuscles", "instructions"]
        if not all(k in data for k in required):
            print(f"[SKIP] Missing fields in {folder_name}")
            skipped += 1
            continue

        images_path = os.path.join(folder_path, "images")
        start_src = os.path.join(images_path, "0.jpg")
        end_src = os.path.join(images_path, "1.jpg")

        if not os.path.isfile(start_src) or not os.path.isfile(end_src):
            print(f"[SKIP] Missing images in {folder_name}")
            skipped += 1
            continue

        dest_folder = os.path.join(STATIC_IMAGE_ROOT, folder_name)
        os.makedirs(dest_folder, exist_ok=True)
        shutil.copy2(start_src, os.path.join(dest_folder, "0.jpg"))
        shutil.copy2(end_src, os.path.join(dest_folder, "1.jpg"))

        data["startImage"] = f"/images/{folder_name}/0.jpg"
        data["endImage"] = f"/images/{folder_name}/1.jpg"

        db.add(Exercise(**data))
        print(f"[OK] {data['name']}")
        inserted += 1

    db.commit()
    db.close()
    print(f"\nDone: {inserted} inserted, {skipped} skipped.")


if __name__ == "__main__":
    ingest_exercises()
