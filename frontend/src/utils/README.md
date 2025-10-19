# Utilidades de Formateo - Sistema ERP

## Regla de Formato de Números

En todo el sistema ERP se mantiene el formato chileno para números:

- **Separador de miles**: punto (`.`)
- **Separador de decimales**: coma (`,`)

### Ejemplos:

- `1234567.89` → `$1.234.567,89` (moneda)
- `1000` → `1.000` (cantidad entera)
- `1234.50` → `1.234,5` (cantidad con decimales)
- `19.5` → `19,5%` (porcentaje)

## Funciones Disponibles

### `formatCurrency(value: number | string | null | undefined): string`

Formatea un número como moneda en formato chileno. Acepta números, strings numéricos, null y undefined.

```typescript
import { formatCurrency } from '@/utils/formatters'

formatCurrency(1234567.89) // "$1.234.567,89"
formatCurrency("1000") // "$1.000,00"
formatCurrency(null) // "$0,00"
```

### `formatNumber(value: number | string | null | undefined, decimales?: number): string`

Formatea un número (cantidad) en formato chileno. Acepta números, strings numéricos, null y undefined.

```typescript
import { formatNumber } from '@/utils/formatters'

formatNumber(1000) // "1.000"
formatNumber("1234.5") // "1.234,5"
formatNumber(1234.567, 2) // "1.234,57"
```

### `formatPercentage(value: number | string | null | undefined, decimales?: number): string`

Formatea un porcentaje en formato chileno. Acepta números, strings numéricos, null y undefined.

```typescript
import { formatPercentage } from '@/utils/formatters'

formatPercentage(19) // "19%"
formatPercentage("19.5") // "19,5%"
formatPercentage(19.567, 2) // "19,57%"
```

### `parseChileanNumber(value: string): number`

Convierte un string en formato chileno a número.

```typescript
import { parseChileanNumber } from '@/utils/formatters'

parseChileanNumber("1.234.567,89") // 1234567.89
parseChileanNumber("$1.000,50") // 1000.50
```

### `formatDate(date: string | Date): string`

Formatea una fecha en formato chileno DD/MM/YYYY.

```typescript
import { formatDate } from '@/utils/formatters'

formatDate("2024-10-13") // "13/10/2024"
formatDate(new Date()) // "13/10/2024"
```

### `formatDateTime(datetime: string | Date): string`

Formatea una fecha y hora en formato chileno.

```typescript
import { formatDateTime } from '@/utils/formatters'

formatDateTime("2024-10-13T14:30:00") // "13/10/2024 14:30"
```

## Uso en Componentes Vue

```vue
<script setup lang="ts">
import { formatCurrency, formatNumber } from '@/utils/formatters'

// Usar directamente en el template
const precio = 1234567.89
const cantidad = 1000
</script>

<template>
  <div>
    <p>Precio: {{ formatCurrency(precio) }}</p>
    <p>Cantidad: {{ formatNumber(cantidad) }}</p>
  </div>
</template>
```

## Backend (Python)

En el backend, la función `formatear_numero_chileno()` en `utils/pdf_generator.py` aplica el mismo formato:

```python
from utils.pdf_generator import formatear_numero_chileno

formatear_numero_chileno(1234567.89, 2)  # "1.234.567,89"
formatear_numero_chileno(19.5, 1)  # "19,5"
```

## Importante

- Siempre usar estas funciones para mantener consistencia en todo el sistema
- No usar `toLocaleString()` o `Intl.NumberFormat` directamente
- Al recibir input del usuario, usar `parseChileanNumber()` para convertir a número
