import unittest

from pii_masking.masker import TokenVault, hash_value, mask_record


class TestPIIMasking(unittest.TestCase):
    def test_production_uses_hashing(self) -> None:
        record = {"name": "Alice", "email": "alice@example.com", "order_id": "1"}
        masked = mask_record(record, environment="production")

        self.assertTrue(masked["name"].startswith("sha256:"))
        self.assertTrue(masked["email"].startswith("sha256:"))
        self.assertEqual(masked["masking_environment"], "production")

    def test_staging_uses_tokenization_and_is_reversible(self) -> None:
        vault = TokenVault()
        record = {"name": "Alice", "email": "alice@example.com"}
        masked = mask_record(record, environment="staging", vault=vault)

        self.assertTrue(masked["name"].startswith("tok_"))
        self.assertEqual(vault.detokenize(masked["name"]), "Alice")

    def test_hash_is_deterministic_for_same_input_and_salt(self) -> None:
        first = hash_value("alice@example.com", salt="fixed")
        second = hash_value("alice@example.com", salt="fixed")
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
