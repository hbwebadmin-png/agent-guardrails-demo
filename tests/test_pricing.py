import unittest

from app.pricing import apply_discount


class ApplyDiscountTest(unittest.TestCase):
    def test_typical_discount(self):
        self.assertEqual(apply_discount(100.0, 15), 85.0)

    def test_rounds_to_cents(self):
        self.assertEqual(apply_discount(19.99, 10), 17.99)

    def test_rejects_negative_price(self):
        with self.assertRaises(ValueError):
            apply_discount(-1.0, 10)

    def test_rejects_out_of_range_percent(self):
        with self.assertRaises(ValueError):
            apply_discount(10.0, 150)


if __name__ == "__main__":
    unittest.main()
