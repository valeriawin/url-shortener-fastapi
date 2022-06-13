from re import findall
from unittest import TestCase

from services.url_generator import generate_url_key


class KeyGenerationCase(TestCase):

    def test_key_generation(self):
        generated_key = generate_url_key()
        found_keys = findall(
            r"^[a-zA-Z0-9]{6}$",
            generated_key
        )
        self.assertEqual(len(found_keys), 1)
        self.assertEqual(found_keys[0], generated_key)
