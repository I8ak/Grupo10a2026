import unittest
from api.web.funciones_auxiliares import calcularIVA


class TestCalcularIVA(unittest.TestCase):

    def test_importe_entero(self):
        self.assertEqual(calcularIVA(100), 121.0)

    def test_importe_decimal(self):
        self.assertAlmostEqual(calcularIVA(99.99), 120.9879)

    def test_importe_cero(self):
        self.assertEqual(calcularIVA(0), 0.0)

    def test_importe_negativo(self):
        self.assertEqual(calcularIVA(-10), -12.1)


if __name__ == "__main__":
    unittest.main()
