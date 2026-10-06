"""Тесты разбора вывода RAC.

Ключевые регрессии, которые здесь закреплены:

* раньше синхронный ``RawOutput`` на выводе с CRLF склеивал все записи в одну
  (``dict_entry_count`` не распознавал пустую строку ``"\\r"``);
* раньше асинхронный ``RawOutput`` использовал регекс с обязательным ``\\r`` и на
  Linux-выводе с LF молча возвращал пустой список.
"""

from __future__ import annotations

import unittest
from dataclasses import dataclass

from raclib._shared import (
    RawOutput,
    dict_entry_count,
    get_array_chunks,
    to_record,
    to_records,
)
from raclib.asynchronous.session import RawOutput as AsyncRawOutput

from . import CLUSTER_INFO, CLUSTER_LIST, MULTILINE_VALUE

#: Оба класса разбора обязаны вести себя одинаково.
RAW_OUTPUT_CLASSES = (RawOutput, AsyncRawOutput)

#: Все варианты переводов строк, которые встречаются в реальной эксплуатации:
#: LF (Linux), CRLF (Windows), CR (старые сборки).
LINE_ENDINGS = (("\n", "LF"), ("\r\n", "CRLF"), ("\r", "CR"))


class LineEndingTestCase(unittest.TestCase):
    """Разбор не должен зависеть от переводов строк."""

    def test_to_list_splits_records_for_every_line_ending(self) -> None:
        for raw_class in RAW_OUTPUT_CLASSES:
            for newline, label in LINE_ENDINGS:
                with self.subTest(parser=raw_class.__name__, newline=label):
                    records = raw_class(CLUSTER_LIST.replace("\n", newline)).to_list()
                    self.assertEqual(len(records), 2, f"{raw_class.__name__} / {label}")

    def test_values_are_clean_for_every_line_ending(self) -> None:
        for raw_class in RAW_OUTPUT_CLASSES:
            for newline, label in LINE_ENDINGS:
                with self.subTest(parser=raw_class.__name__, newline=label):
                    first = raw_class(CLUSTER_LIST.replace("\n", newline)).to_list()[0]
                    self.assertEqual(first["name"], "Production")
                    self.assertEqual(first["host"], "rac1.local")
                    # \r не должен утекать в значение и ломать приведение типа.
                    self.assertEqual(first["port"], 1541)
                    self.assertIsInstance(first["port"], int)

    def test_single_record_without_trailing_blank_line(self) -> None:
        for raw_class in RAW_OUTPUT_CLASSES:
            for newline, label in LINE_ENDINGS:
                with self.subTest(parser=raw_class.__name__, newline=label):
                    record = raw_class(
                        CLUSTER_INFO.replace("\n", newline)
                    ).to_dict()
                    self.assertEqual(record["name"], "Production")
                    self.assertEqual(record["expiration_timeout"], 60)

    def test_reader_of_lines(self) -> None:
        for newline, label in LINE_ENDINGS:
            with self.subTest(newline=label):
                self.assertEqual(
                    len(to_records(CLUSTER_LIST.replace("\n", newline))), 2
                )


class RawOutputSemanticsTestCase(unittest.TestCase):
    """Поведение разбора, не зависящее от переводов строк."""

    def test_to_list_returns_all_records(self) -> None:
        for raw_class in RAW_OUTPUT_CLASSES:
            with self.subTest(parser=raw_class.__name__):
                records = raw_class(CLUSTER_LIST).to_list()
                self.assertEqual(len(records), 2)
                self.assertEqual(records[0]["cluster"], "6a4c0b3f-1111-2222-3333-444455556666")
                self.assertEqual(records[1]["cluster"], "7b5d1c4e-aaaa-bbbb-cccc-ddddeeeeffff")
                self.assertEqual(records[1]["descr"], "Резервный")

    def test_keys_are_written_with_underscores(self) -> None:
        record = to_record(CLUSTER_INFO)
        self.assertIn("expiration_timeout", record)
        self.assertNotIn("expiration-timeout", record)

    def test_decimal_values_become_int(self) -> None:
        record = to_record(CLUSTER_INFO)
        self.assertIsInstance(record["port"], int)
        self.assertEqual(record["port"], 1541)

    def test_quoted_values_lose_quotes(self) -> None:
        self.assertEqual(to_record(CLUSTER_INFO)["name"], "Production")

    def test_to_dict_returns_last_record(self) -> None:
        # Историческое поведение: to_dict поверх списка отдаёт последнюю запись.
        record = RawOutput(CLUSTER_LIST).to_dict()
        self.assertEqual(record["name"], "Test")

    def test_empty_output_gives_empty_results(self) -> None:
        for raw_class in RAW_OUTPUT_CLASSES:
            with self.subTest(parser=raw_class.__name__):
                output = raw_class("")
                self.assertEqual(output.to_list(), [])
                self.assertEqual(output.to_dict(), {})
                self.assertEqual(output.to_str(), "")

    def test_value_containing_colon_is_kept(self) -> None:
        record = to_record("descr : host=localhost;db=TestIB\n")
        self.assertEqual(record["descr"], "host=localhost;db=TestIB")

    def test_multiline_value_is_glued_to_previous_key(self) -> None:
        record = to_record(MULTILINE_VALUE)
        self.assertEqual(record["dbms"], "PostgreSQL")
        self.assertIn("продолжение описания", str(record["descr"]))

    def test_to_dataclass(self) -> None:
        @dataclass
        class Cluster:
            cluster: str
            name: str
            host: str
            port: int
            expiration_timeout: int

        parsed = RawOutput(CLUSTER_INFO).to_dataclass(Cluster)
        self.assertEqual(parsed.name, "Production")
        self.assertEqual(parsed.port, 1541)
        self.assertEqual(parsed.expiration_timeout, 60)

    def test_to_list_of_dataclass(self) -> None:
        @dataclass
        class Cluster:
            cluster: str
            name: str
            host: str
            port: int
            expiration_timeout: int
            lifetime_limit: int
            security_level: int
            descr: str

        parsed = RawOutput(CLUSTER_LIST).to_list_of_dataclass(Cluster)
        self.assertEqual([item.name for item in parsed], ["Production", "Test"])
        self.assertEqual(parsed[1].descr, "Резервный")


class SyncAsyncEquivalenceTestCase(unittest.TestCase):
    """Синхронный и асинхронный разбор обязаны совпадать полностью."""

    def test_results_are_identical(self) -> None:
        for newline, label in LINE_ENDINGS:
            with self.subTest(newline=label):
                payload = CLUSTER_LIST.replace("\n", newline)
                self.assertEqual(RawOutput(payload).to_list(), AsyncRawOutput(payload).to_list())
                self.assertEqual(RawOutput(payload).to_dict(), AsyncRawOutput(payload).to_dict())


class LegacyUtilsTestCase(unittest.TestCase):
    """Устаревшие утилиты остались и больше не падают неочевидным образом."""

    def test_get_array_chunks(self) -> None:
        self.assertEqual(get_array_chunks([("a", "1"), ("b", "2"), ("c", "3")], 2),
                         [[("a", "1"), ("b", "2")], [("c", "3")]])

    def test_get_array_chunks_rejects_zero(self) -> None:
        # Раньше это был ValueError из range() с невнятным текстом.
        with self.assertRaises(ValueError):
            get_array_chunks([("a", "1")], 0)

    def test_dict_entry_count(self) -> None:
        self.assertEqual(dict_entry_count(["a", "b", "", "c"]), 2)
        self.assertEqual(dict_entry_count(["a", "b"]), 2)


if __name__ == "__main__":
    unittest.main()
