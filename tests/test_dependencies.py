import unittest
from pathlib import Path


class DependencyPinTest(unittest.TestCase):
    def test_requests_is_at_or_above_fixed_version(self):
        pins = Path("requirements.txt").read_text().splitlines()
        pin = next(line for line in pins if line.startswith("requests=="))
        version = tuple(int(part) for part in pin.split("==")[1].split("."))
        self.assertGreaterEqual(version, (2, 33, 0))


if __name__ == "__main__":
    unittest.main()
