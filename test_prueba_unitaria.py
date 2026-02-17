import unittest
from api.web.funciones_auxiliares import calcularIVA


class TestCalcularIVA(unittest.TestCase):

    def test_importe_entero(self):
        self.assertEqual(calcularIVA(100), 121.0)

if __name__ == "__main__":
    unittest.main()
