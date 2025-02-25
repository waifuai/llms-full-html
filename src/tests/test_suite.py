import os
import shutil
import tempfile
import unittest

import sys
from utils import safe_read, CODE_EXTENSIONS

class TestSafeRead(unittest.TestCase):
    def setUp(self):
        # Create a temporary file to test safe_read.
        self.test_dir = tempfile.mkdtemp()
        self.file_path = os.path.join(self.test_dir, "test.txt")
        self.content = "Sample content for safe read."
        with open(self.file_path, "w", encoding="utf-8") as f:
            f.write(self.content)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_safe_read_success(self):
        # Verify safe_read correctly returns the content.
        result = safe_read(self.file_path)
        self.assertEqual(result, self.content)

    def test_safe_read_nonexistent(self):
        # Verify safe_read returns None for a non-existent file.
        non_existent = os.path.join(self.test_dir, "nofile.txt")
        result = safe_read(non_existent)
        self.assertIsNone(result)

if __name__ == "__main__":
    unittest.main()