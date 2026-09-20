import hashlib
import json
import os

HASH_FILE = "document_hashes.json"


def load_hashes():
    if os.path.exists(HASH_FILE):
        with open(HASH_FILE, "r") as file:
            return json.load(file)
    return {}


def save_hashes(hashes):
    with open(HASH_FILE, "w") as file:
        json.dump(hashes, file, indent=4)


def calculate_file_hash(file_path):
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        while True:
            data = file.read(8192)

            if not data:
                break

            sha256.update(data)

    return sha256.hexdigest()


def is_duplicate(file_hash):
    hashes = load_hashes()
    return file_hash in hashes


def register_document(file_hash, document_id, filename):
    print("Registering:", filename)

    hashes = load_hashes()

    hashes[file_hash] = {
        "document_id": document_id,
        "filename": filename
    }

    save_hashes(hashes)

    print(load_hashes())

    hashes[file_hash] = {
        "document_id": document_id,
        "filename": filename
    }

    save_hashes(hashes)


def get_existing_document(file_hash):
    hashes = load_hashes()
    return hashes[file_hash]