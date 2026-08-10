import unittest

from converter import convert_report_text


class ConvertReportTextTests(unittest.TestCase):
    def test_parses_metadata_and_rows_from_semicolon_report(self):
        report = """Lote: Norte
Fecha: 2026-08-10
Operador: Ana

sector;inicio;fin;caudal_litros
A1;07:00;08:00;450
A2;08:15;09:00;320
"""

        converted = convert_report_text(report)

        self.assertEqual(
            converted["metadata"],
            {"lote": "Norte", "fecha": "2026-08-10", "operador": "Ana"},
        )
        self.assertEqual(converted["record_count"], 2)
        self.assertEqual(converted["records"][0]["sector"], "A1")
        self.assertEqual(converted["records"][1]["caudal_litros"], "320")

    def test_parses_tab_delimited_report(self):
        report = """turno\tsector\tvolumen
mañana\tB1\t120
"""

        converted = convert_report_text(report)

        self.assertEqual(converted["record_count"], 1)
        self.assertEqual(
            converted["records"][0],
            {"turno": "mañana", "sector": "B1", "volumen": "120"},
        )


if __name__ == "__main__":
    unittest.main()
