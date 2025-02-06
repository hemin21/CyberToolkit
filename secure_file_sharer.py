import os
import socket
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

# AES encryption key (32 bytes for AES-256)
KEY_SIZE = 32

def encrypt_file(file_path, key):
    """Encrypts a file using AES-256."""
    cipher = AES.new(key, AES.MODE_CBC)
    with open(file_path, 'rb') as f:
        plaintext = f.read()
    ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))
    return cipher.iv + ciphertext  # Prepend IV to ciphertext

def decrypt_file(encrypted_data, key):
    """Decrypts a file using AES-256."""
    iv = encrypted_data[:AES.block_size]  # Extract IV
    ciphertext = encrypted_data[AES.block_size:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return plaintext

def send_file(file_path, key, host, port):
    """Sends an encrypted file to a recipient."""
    encrypted_data = encrypt_file(file_path, key)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(encrypted_data)
    print(f"File '{file_path}' sent successfully!")

def receive_file(key, port):
    """Receives and decrypts a file."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('0.0.0.0', port))
        s.listen(1)
        print(f"Waiting for sender to connect on port {port}...")
        conn, addr = s.accept()
        with conn:
            print(f"Connected to {addr}")
            encrypted_data = conn.recv(4096)
            decrypted_data = decrypt_file(encrypted_data, key)
            output_file = "received_file.txt"  # Change this as needed
            with open(output_file, 'wb') as f:
                f.write(decrypted_data)
            print(f"File received and saved as '{output_file}'!")

def main():
    print("Secure File Sharing (End-to-End Encryption)")
    mode = input("Are you the sender or receiver? (s/r): ").strip().lower()

    if mode == 's':
        # Sender mode
        file_path = input("Enter the file path to send: ").strip()
        key = get_random_bytes(KEY_SIZE)  # Generate a random key
        print(f"Encryption Key (share this with the recipient): {key.hex()}")
        host = input("Enter recipient's IP address: ").strip()
        port = int(input("Enter recipient's port: ").strip())
        send_file(file_path, key, host, port)

    elif mode == 'r':
        # Receiver mode
        key_hex = input("Enter the encryption key (from sender): ").strip()
        key = bytes.fromhex(key_hex)  # Convert hex key to bytes
        port = int(input("Enter port to listen on: ").strip())
        receive_file(key, port)

    else:
        print("Invalid mode. Please choose 's' for sender or 'r' for receiver.")

if __name__ == "__main__":
    main()