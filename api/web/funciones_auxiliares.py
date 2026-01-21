import decimal
import json

class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal): return float(obj)

    
def calcularIVA(importe):
        return importe * 1.21
