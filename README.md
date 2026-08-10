# RiegosICConverter

Aplicación de línea de comandos para transformar reportes de riego de ICC en datos legibles (JSON).

## Uso

```bash
python /home/runner/work/RiegosICConverter/RiegosICConverter/converter.py /ruta/reporte_icc.txt -o salida.json
```

Si no usas `-o`, el JSON se imprime en consola.

## Formato esperado de entrada

El convertidor soporta:
- Líneas de metadatos con formato `Clave: Valor`
- Tabla delimitada por `;`, `,`, `\t` o `|`

Ejemplo:

```txt
Lote: Norte
Fecha: 2026-08-10

sector;inicio;fin;caudal_litros
A1;07:00;08:00;450
A2;08:15;09:00;320
```
