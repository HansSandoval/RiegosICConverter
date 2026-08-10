from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path
from typing import Any

_KEY_VALUE_PATTERN = re.compile(r"^\s*([^:]+?)\s*:\s*(.+?)\s*$")


def _normalize_key(key: str) -> str:
    normalized = re.sub(r"[^\w]+", "_", key.strip().lower(), flags=re.UNICODE)
    return normalized.strip("_")


def _detect_delimiter(lines: list[str]) -> str:
    sample = "\n".join(line for line in lines if line.strip())
    try:
        dialect = csv.Sniffer().sniff(sample, delimiters=",;\t|")
        return dialect.delimiter
    except csv.Error:
        for delimiter in (";", ",", "\t", "|"):
            if any(delimiter in line for line in lines):
                return delimiter
    return ";"


def convert_report_text(text: str) -> dict[str, Any]:
    lines = text.splitlines()
    metadata: dict[str, str] = {}
    table_start = -1

    for idx, line in enumerate(lines):
        stripped = line.strip()
        if not stripped:
            continue

        match = _KEY_VALUE_PATTERN.match(line)
        if match and table_start == -1:
            key, value = match.groups()
            metadata[_normalize_key(key)] = value.strip()
            continue

        if any(separator in line for separator in (";", ",", "\t", "|")):
            table_start = idx
            break

    records: list[dict[str, str]] = []

    if table_start != -1:
        table_lines = [line for line in lines[table_start:] if line.strip()]
        delimiter = _detect_delimiter(table_lines)
        reader = csv.DictReader(table_lines, delimiter=delimiter)

        for row in reader:
            cleaned = {
                _normalize_key(str(key)): (value.strip() if isinstance(value, str) else "")
                for key, value in row.items()
                if key is not None and str(key).strip()
            }
            if any(value for value in cleaned.values()):
                records.append(cleaned)

    return {
        "metadata": metadata,
        "records": records,
        "record_count": len(records),
    }


def convert_report_file(input_path: Path, encoding: str = "utf-8") -> dict[str, Any]:
    text = input_path.read_text(encoding=encoding)
    converted = convert_report_text(text)
    converted["source_file"] = str(input_path)
    return converted


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convierte reportes de riego ICC a datos legibles en JSON."
    )
    parser.add_argument("input", type=Path, help="Ruta al archivo de reporte ICC")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Ruta del archivo JSON de salida. Si se omite, se imprime en consola.",
    )
    parser.add_argument(
        "--encoding",
        default="utf-8",
        help="Encoding del archivo de entrada (por defecto: utf-8)",
    )
    args = parser.parse_args()

    converted = convert_report_file(args.input, encoding=args.encoding)
    output = json.dumps(converted, ensure_ascii=False, indent=2)

    if args.output:
        args.output.write_text(output + "\n", encoding="utf-8")
    else:
        print(output)


if __name__ == "__main__":
    main()
