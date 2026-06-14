import unittest

from crypto_shredding.key_manager import KeyManager, KeyNotFoundError


class TestCryptoShredding(unittest.TestCase):
    def test_rtbf_shredded_key_cannot_decrypt(self) -> None:
        manager = KeyManager()
        key_id = manager.create_key("CUS-1")
        encrypted = manager.encrypt(key_id, "sensitive-value")

        manager.shred_key(key_id)

        with self.assertRaises(KeyNotFoundError):
            manager.decrypt(key_id, encrypted)

    def test_audit_log_records_key_operations(self) -> None:
        manager = KeyManager()
        key_id = manager.create_key("CUS-2")
        encrypted = manager.encrypt(key_id, "hello")
        _ = manager.decrypt(key_id, encrypted)
        manager.shred_key(key_id)

        operations = [entry["operation"] for entry in manager.list_audit_events()]
        self.assertEqual(operations, ["create_key", "encrypt", "decrypt", "shred_key"])


if __name__ == "__main__":
    unittest.main()
