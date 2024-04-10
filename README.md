# This is our Information Security Final Project. We are a group of three people :
1. Manoj Sharma - 2330575
2. Thuvaarakkesh Ramanathan - 202331425
3. Omid Moridnejad - 202331293

Here we covering the following steps in this repository:

1. Key Generation: Implemented functions named **generate_key_pair()** to generate RSA key pairs using the cryptography library.
2. File Encryption: Implemented functions named **encrypt_file()** to encrypt a file using the public key of the recipient and the RSA encryption scheme.
3. File Decryption: Implemented functions named **decrypt_file()** an encrypted file using the corresponding private key and the RSA decryption scheme.
4. Hashing: Implemented functions named **generate_file_hash()** to generate a hash (e.g., SHA-256) of a file using the hashlib library.
5. Integrity Verification: Developed functions named **verify_integrity()** to verify the integrity of the received file by comparing its hash with the original hash.
6. User Interface: Created a simple user interface named **user_interface()** for interacting with the system.


** All the function are available in the file named key_generation.py.
** Testing: wrote comprehensive unit test cases for each functionality using a testing framework like unittest. all are available in the file named - unittest.py file.
