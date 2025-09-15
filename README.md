# Tech Test Flask API

## Descripción
Este proyecto implementa una API REST en **Python 3 + Flask** para manejar inventario y calcular rentabilidad de productos.  
Se diseñó para ser consumida posteriormente desde un bot de RPA (Automation Anywhere), el cual enviará las transacciones en formato JSON.

---

## 📂 Arquitectura del Proyecto

```
tech-test-flask/
├── app/
│   ├── __init__.py       # Punto de creación de la app Flask (App Factory)
│   ├── routes.py         # Definición de endpoints de la API
├── wsgi.py               # Punto de entrada para ejecutar la aplicación
├── test.json             # Archivo de ejemplo con transacciones
└── README.md             # Documentación
```

### Flujo principal
1. El bot o cliente envía un **JSON con transacciones** a los endpoints.
2. La API procesa la información:
   - `/calculate-stock`: Calcula inventario sumando BUY y restando SELL.
   - `/product-profit/<product-name>`: Calcula ganancia total de un producto en base a las ventas (`SELL`).
3. La API responde con **JSON estructurado** y códigos de estado (`200` en éxito, `400` en errores).

---

## Endpoints

### 1️⃣ POST `/calculate-stock`
Recibe un JSON con transacciones y devuelve el stock final por producto.

#### Ejemplo de request
```json
{
  "transactions": [
    {"transactionType": "SELL", "productType": "COAL", "quantity": 455, "unitValue": 996812},
    {"transactionType": "BUY",  "productType": "GOLD", "quantity": 289, "unitValue": 1077073}
  ]
}
```

#### Ejemplo de response
```json
{
  "finalStock": {
    "COAL": -455,
    "GOLD": 289
  }
}
```

---

### POST `/product-profit/<product-name>`
Recibe un JSON con transacciones y devuelve el beneficio total (`cantidad * valorUnitario`)  
solo para las transacciones de tipo **SELL** del producto indicado.

#### Ejemplo de request
`POST http://127.0.0.1:5000/product-profit/COAL`

```json
{
  "transactions": [
    {"transactionType": "SELL", "productType": "COAL", "quantity": 455, "unitValue": 996812},
    {"transactionType": "SELL", "productType": "COAL", "quantity": 442, "unitValue": 1202229}
  ]
}
```

#### Ejemplo de response
```json
{
  "product": "COAL",
  "totalProfit": 719508059
}
```

---

## Ejecución del Proyecto

### 1. Instalar dependencias

```bash
pip install flask
```

### 2. Ejecutar servidor
Desde la raíz del proyecto:

```bash
python wsgi.py
```

El servidor correrá en:  
👉 `http://127.0.0.1:5000/`

### 3. Probar con PowerShell
Ejemplo para `/calculate-stock`:

```powershell
Invoke-WebRequest -Uri http://127.0.0.1:5000/calculate-stock `
-Method POST `
-ContentType "application/json" `
-InFile test.json | Select-Object StatusCode, Content
```

Ejemplo para `/product-profit/COAL`:

```powershell
Invoke-WebRequest -Uri http://127.0.0.1:5000/product-profit/COAL `
-Method POST `
-ContentType "application/json" `
-InFile test.json | Select-Object StatusCode, Content
```

---
- **Validación de entrada**:  
  Se valida que los JSON tengan la estructura correcta, de lo contrario se retorna `400`.

- **Escalabilidad**:  
  - Actualmente corre con el servidor de desarrollo Flask (`wsgi.py`).  
  - La API puede escalar horizontalmente ya que es **stateless** (no guarda estado en memoria).
- **Extensibilidad**:  
  Nuevos endpoints se pueden agregar en `routes.py` fácilmente siguiendo el mismo patrón.

---

## Futuras Mejoras
- Integración con base de datos (SQLite, PostgreSQL, etc.) para persistir inventario.

---

**Autor**: Miguel Ibañez - Septiembre 2025
