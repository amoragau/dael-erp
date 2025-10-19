/**
 * Utilidades de formateo para el sistema ERP
 * Mantiene el formato chileno: separador de miles "." y separador de decimales ","
 */

/**
 * Formatea un número como moneda en formato chileno
 * Ejemplo: 1234567.89 -> $1.234.567,89
 *
 * @param value - Valor numérico a formatear
 * @returns String formateado como moneda
 */
export function formatCurrency(value: number | string | null | undefined): string {
  // Convertir a número, manejando strings, null y undefined
  const numero = typeof value === 'string' ? parseFloat(value) || 0 : (value || 0)
  const partes = numero.toFixed(2).split('.')
  const entero = partes[0].replace(/\B(?=(\d{3})+(?!\d))/g, '.')
  const decimal = partes[1]
  return `$${entero},${decimal}`
}

/**
 * Formatea un número (cantidad) en formato chileno
 * - Números enteros sin decimales: 1000 -> 1.000
 * - Números con decimales: 1234.50 -> 1.234,5
 *
 * @param value - Valor numérico a formatear
 * @param decimales - Número de decimales a mostrar (opcional)
 * @returns String formateado
 */
export function formatNumber(value: number | string | null | undefined, decimales?: number): string {
  // Convertir a número, manejando strings, null y undefined
  const numero = typeof value === 'string' ? parseFloat(value) || 0 : (value || 0)

  // Si se especifican decimales fijos
  if (decimales !== undefined) {
    const partes = numero.toFixed(decimales).split('.')
    const entero = partes[0].replace(/\B(?=(\d{3})+(?!\d))/g, '.')
    const decimal = partes[1]
    return decimal && parseInt(decimal) > 0 ? `${entero},${decimal}` : entero
  }

  // Si es un número entero, mostrarlo sin decimales
  if (Number.isInteger(numero)) {
    return numero.toString().replace(/\B(?=(\d{3})+(?!\d))/g, '.')
  }

  // Si tiene decimales, mostrar hasta 2 decimales sin ceros finales
  const partes = numero.toFixed(2).split('.')
  const entero = partes[0].replace(/\B(?=(\d{3})+(?!\d))/g, '.')
  const decimal = partes[1].replace(/0+$/, '') // Eliminar ceros finales

  return decimal ? `${entero},${decimal}` : entero
}

/**
 * Formatea un porcentaje en formato chileno
 * Ejemplo: 19.5 -> 19,5%
 *
 * @param value - Valor del porcentaje
 * @param decimales - Número de decimales (default: 1)
 * @returns String formateado como porcentaje
 */
export function formatPercentage(value: number | string | null | undefined, decimales: number = 1): string {
  // Convertir a número, manejando strings, null y undefined
  const numero = typeof value === 'string' ? parseFloat(value) || 0 : (value || 0)
  const partes = numero.toFixed(decimales).split('.')
  const entero = partes[0]
  const decimal = partes[1]

  if (decimal && parseInt(decimal) > 0) {
    return `${entero},${decimal}%`
  }
  return `${entero}%`
}

/**
 * Convierte un string en formato chileno a número
 * Ejemplo: "1.234.567,89" -> 1234567.89
 *
 * @param value - String en formato chileno
 * @returns Número parseado
 */
export function parseChileanNumber(value: string): number {
  if (!value) return 0

  // Remover símbolo de moneda y espacios
  let cleaned = value.replace(/[$\s]/g, '')

  // Reemplazar separadores chilenos por formato estándar
  cleaned = cleaned.replace(/\./g, '') // Remover separador de miles
  cleaned = cleaned.replace(',', '.') // Cambiar separador decimal

  return parseFloat(cleaned) || 0
}

/**
 * Formatea una fecha en formato chileno DD/MM/YYYY
 *
 * @param date - Fecha como string o Date
 * @returns String formateado como fecha
 */
export function formatDate(date: string | Date | null | undefined): string {
  if (!date) return ''

  const dateObj = typeof date === 'string' ? new Date(date + 'T00:00:00') : date

  const day = dateObj.getDate().toString().padStart(2, '0')
  const month = (dateObj.getMonth() + 1).toString().padStart(2, '0')
  const year = dateObj.getFullYear()

  return `${day}/${month}/${year}`
}

/**
 * Formatea una fecha y hora en formato chileno
 *
 * @param datetime - Fecha/hora como string o Date
 * @returns String formateado como fecha y hora
 */
export function formatDateTime(datetime: string | Date | null | undefined): string {
  if (!datetime) return ''

  const dateObj = typeof datetime === 'string' ? new Date(datetime) : datetime

  const day = dateObj.getDate().toString().padStart(2, '0')
  const month = (dateObj.getMonth() + 1).toString().padStart(2, '0')
  const year = dateObj.getFullYear()
  const hours = dateObj.getHours().toString().padStart(2, '0')
  const minutes = dateObj.getMinutes().toString().padStart(2, '0')

  return `${day}/${month}/${year} ${hours}:${minutes}`
}
