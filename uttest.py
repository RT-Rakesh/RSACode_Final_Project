from function import *
import unittest
import os

class TestSecureFileTransfer(unittest.TestCase):
    def test_generate_rsa_key_pair(self):
        # Test generating RSA key pair
        private_key, public_key = generate_key_pair()
        self.assertIsNotNone(private_key)
        self.assertIsNotNone(public_key)

    def test_file_encryption_decryption(self):
        # Test file encryption and decryption
        file_path = "test_file.txt"
        with open(file_path, "wb") as file:
            file.write(b"Test data")

        private_key, public_key = generate_key_pair()
        encrypted_file_path = "encrypted_test_file.bin"
        encrypt_file(file_path, public_key, encrypted_file_path)
        self.assertTrue(os.path.exists(encrypted_file_path))

        decrypted_file_path = "decrypted_test_file.txt"
        decrypt_file(encrypted_file_path, private_key, decrypted_file_path)
        self.assertTrue(os.path.exists(decrypted_file_path))

        with open(decrypted_file_path, "rb") as file:
            decrypted_data = file.read()
            self.assertEqual(decrypted_data, b"Test data")

    def test_generate_file_hash(self):
        # Test generating file hash
        file_path = "test_file.txt"
        with open(file_path, "wb") as file:
            file.write(b"Test data")

        file_hash = generate_file_hash(file_path)
        self.assertEqual(file_hash, "532eaabd9574880dbf76b9b8cc00832c20a6ec113d682299550d7a6e0f3454f6")

    def test_verify_integrity(self):
        # Test verifying integrity of the file
        file_path = "test_file.txt"
        with open(file_path, "wb") as file:
            file.write(b"Test data")

        original_hash = generate_file_hash(file_path)
        self.assertTrue(verify_integrity(file_path, original_hash))


    def setUp(self):
        # Create a test file with some data
        self.test_file_path = 'test_file.txt'
        self.test_data = b'This is a test message.'
        with open(self.test_file_path, 'wb') as file:
            file.write(self.test_data)
        
        # Generate hash for the test file
        self.original_hash = hashlib.sha256(self.test_data).digest()

    def test_integrity_verification(self):
        # Test integrity verification for a file
        self.assertTrue(verify_integrity(self.test_file_path, self.original_hash))

    def test_integrity_verification_with_tampered_file(self):
        # Test integrity verification for a tampered file
        with open(self.test_file_path, 'ab') as file:
            file.write(b'Tampered data')
        self.assertFalse(verify_integrity(self.test_file_path, self.original_hash))

    def test_integrity_verification_with_nonexistent_file(self):
        # Test integrity verification for a nonexistent file
        non_existent_file_path = 'non_existent_file.txt'
        with self.assertRaises(FileNotFoundError):
            verify_integrity(non_existent_file_path, self.original_hash)

    def tearDown(self):
        # Clean up test files
        if os.path.exists(self.test_file_path):
            os.remove(self.test_file_path)

            
if __name__ == "__main__":
    unittest.main()
