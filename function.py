# Key Generation: Implement functions to generate RSA key pairs using the cryptography library.
#************************************************************************************************************************

# Importing modules from the cryptography library for handling cryptographic operations.
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
# Creating a function named generate_key_pair which will generate a key pair of RSA keys.
def generate_key_pair():
    # This line generates a private key using RSA algorithm with specific parameters like public exponent and key size.
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()  
    pem_private_key = private_key.private_bytes(encoding=serialization.Encoding.PEM,format=serialization.PrivateFormat.PKCS8,encryption_algorithm=serialization.NoEncryption())
    pem_public_key=public_key.public_bytes(encoding=serialization.Encoding.PEM,format=serialization.PublicFormat.SubjectPublicKeyInfo)
    
    # Save private key to a file
    with open('private_key.pem', 'wb') as f:
      f.write(pem_private_key)

    # Save public key to a file
    with open('public_key.pem', 'wb') as f:
      f.write(pem_public_key)
      
    return private_key, public_key

def load_public_key(public_key_file):
    with open(public_key_file, "rb") as public_key_in:
        public_key_bytes = public_key_in.read()
        public_key = serialization.load_pem_public_key(public_key_bytes)
    return public_key

def load_private_key(private_key_file):
    with open(private_key_file, "rb") as private_key_in:
        private_key_bytes = private_key_in.read()
        private_key = serialization.load_pem_private_key(private_key_bytes, password=None)
    return private_key
#************************************************************************************************************************

# File Encryption: Write functions to encrypt a file using the public key of the recipient and the RSA encryption scheme.

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

# function to encrypt a file using RSA public key
def encrypt_file(file_path, public_key, encrypted_file_path):
    with open(file_path, 'rb') as file:
        data = file.read()  # Read file content as bytes 

    # Encrypt the file content using RSA OAEP padding with SHA256 hashing
    encrypted_data = public_key.encrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),  # Mask generation function
            algorithm=hashes.SHA256(),  # Hashing algorithm
            label=None
        )
    )

    # Write the encrypted data to a new file
    with open(encrypted_file_path, 'wb') as encrypted_file:
        encrypted_file.write(encrypted_data)

#************************************************************************************************************************

# File Decryption: Create functions to decrypt an encrypted file using the corresponding private key and the RSA decryption scheme.

# function to decrypt an encrypted file using RSA private key
def decrypt_file(encrypted_file_path, private_key, decrypted_file_path):

    with open(encrypted_file_path, 'rb') as encrypted_file:
        encrypted_data = encrypted_file.read()  # Read encrypted data

    # Decrypt the encrypted data using RSA OAEP padding with SHA256 hashing
    decrypted_data = private_key.decrypt(
        encrypted_data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),  # Mask generation function
            algorithm=hashes.SHA256(),  # Hashing algorithm
            label=None
        )
    )

    # Write the decrypted data to a new file
    with open(decrypted_file_path, 'wb') as decrypted_file:
        decrypted_file.write(decrypted_data)

#************************************************************************************************************************

# Hashing: Implement functions to generate a hash (e.g., SHA-256) of a file using the hashlib library.

import hashlib

# function to generate SHA-256 hash of a file, generate_file_hash() function takes a file path as input. 

def generate_file_hash(file_path):
    # Create a SHA-256 hash object
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as file:
        while True:
            data = file.read(65536)  # Reading data in chunks of 64 KB
            if not data:  
                break
            hasher.update(data)  # Updating hash with the read data
    # Return the hexadecimal digest of the hash
    return hasher.hexdigest()

#************************************************************************************************************************

# Integrity Verification: Develop functions to verify the integrity of the received file by comparing its hash with the original hash.

# function to verify integrity of a file. It generates the current hash of the file and compares it with the original hash.
def verify_integrity(file_path, original_hash):
    # Generating the hash of the file
    current_hash = generate_file_hash(file_path)
    # Comparing the current hash with the original hash. If both hashes match, it returns True, indicating the file's integrity is verified. Else it returns False.
    return current_hash == original_hash

#************************************************************************************************************************

# User Interface
def user_interface():
    print("Secure File Transfer System")
    print("---------------------------")

    while True:
        print("\nMenu:")
        print("1. Generate RSA Key Pair")
        print("2. Encrypt File")
        print("3. Decrypt File")
        print("4. Verify Integrity")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            # Generate RSA key pair
            private_key, public_key = generate_key_pair()
            print("RSA Key Pair generated successfully.")

        elif choice == "2":
            # Encrypt file
            file_path = input("Enter the path of the file to encrypt: ")
            recipient_public_key_path = input("Enter the path of the recipient's public key: ")
            encrypted_file_path = input("Enter the path to save the encrypted file: ")
            public_key = load_public_key(recipient_public_key_path)
            encrypt_file(file_path, public_key, encrypted_file_path)
            print("File encrypted successfully.")

        elif choice == "3":
            # Decrypt file
            encrypted_file_path = input("Enter the path of the encrypted file: ")
            private_key_path = input("Enter the path of your private key: ")
            decrypted_file_path = input("Enter the path to save the decrypted file: ")
            private_key = load_private_key(private_key_path)
            decrypt_file(encrypted_file_path, private_key, decrypted_file_path)
            print("File decrypted successfully.")

        elif choice == "4":
            # Verify integrity
            original_file_path = input("Enter the path of the original file to verify integrity: ")
            decrypted_file_path = input("Enter the path of the decrypted file: ")
            original_hash = generate_file_hash(original_file_path)
            if verify_integrity(decrypted_file_path, original_hash):
                print("Integrity verified: The file remains unchanged.")
            else:
                print("Integrity verification failed: The file has been tampered with.")

        elif choice == "5":
            # Exit the program
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    user_interface()




