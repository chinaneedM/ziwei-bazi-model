import hashlib
import importlib.util
import io
import unittest
from pathlib import Path
from PIL import Image

path = Path(__file__).resolve().parents[1] / "scripts/acquire-tianwen-13jz-g893-exact-pages.py"
spec = importlib.util.spec_from_file_location("g893_recovery", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class ExactSourceIntake(unittest.TestCase):
    def jpeg(self, size=(1150, 2000)):
        out = io.BytesIO()
        Image.new("RGB", size).save(out, format="JPEG")
        return out.getvalue()

    def test_only_previously_registered_pages(self):
        self.assertEqual(set(module.targets()), {"018b", "019b", "035b", "036b"})

    def test_exact_bytes_and_dimensions(self):
        raw = self.jpeg()
        self.assertEqual(module.inspect(raw, hashlib.sha256(raw).hexdigest())["size_px"], [1150, 2000])

    def test_altered_bytes_fail_even_for_valid_jpeg(self):
        with self.assertRaises(ValueError):
            module.inspect(self.jpeg(), "0" * 64)

    def test_html_error_page_cannot_pass_with_own_hash(self):
        raw = b"<html>service unavailable</html>"
        with self.assertRaises(ValueError):
            module.inspect(raw, hashlib.sha256(raw).hexdigest())

    def test_preview_size_cannot_pass_with_own_hash(self):
        raw = self.jpeg((115, 200))
        with self.assertRaises(ValueError):
            module.inspect(raw, hashlib.sha256(raw).hexdigest())


if __name__ == "__main__":
    unittest.main()
