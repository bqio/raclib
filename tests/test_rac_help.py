"""Сверка параметров raclib с реальной справкой установленного ``rac``.

Эти тесты запускаются только там, где есть ``rac`` (обычно машина
администратора) и пропускаются в остальных окружениях. Они ловят то, что не
видят ни модульные тесты, ни сборка:

* опечатки в именах параметров — RAC молча игнорирует неизвестный параметр,
  поэтому команда уходит без нужной настройки. Так был найден
  ``--safe-working-processess-memory-limit`` вместо ``...processes...``;
* параметры, которых у команды нет: ``--db-user`` у ``rac infobase drop``.
"""

from __future__ import annotations

import importlib.util
import unittest

from . import REPO_ROOT


def load_audit():
    """Загружает ``tools/audit_rac_help.py`` как модуль."""
    path = REPO_ROOT / "tools" / "audit_rac_help.py"
    spec = importlib.util.spec_from_file_location("raclib_audit_rac_help", path)
    if spec is None or spec.loader is None:  # pragma: no cover - защита
        raise ImportError(f"Не удалось загрузить инструмент: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


AUDIT = load_audit()
RAC = AUDIT.find_rac(None)

SKIP_REASON = "rac не найден на этой машине — сверка со справкой недоступна"


@unittest.skipIf(RAC is None, SKIP_REASON)
class RacHelpAuditTestCase(unittest.TestCase):
    """Параметры в коде должны существовать в справке установленного rac."""

    def test_all_flags_are_documented_by_rac(self) -> None:
        help_by_mode = {
            mode: AUDIT.run_help(RAC, mode) for mode in sorted(set(AUDIT.MODULE_MODES.values()))
        }
        commands_by_mode = {
            mode: AUDIT.flags_by_command(text, mode) for mode, text in help_by_mode.items()
        }

        problems: list[str] = []
        checked = 0
        for module, method in AUDIT.command_names():
            mode = AUDIT.MODULE_MODES[module]
            documented = commands_by_mode[mode]
            command_flags = documented.get(method)
            if not command_flags:
                continue
            checked += 1
            known = command_flags | documented.get(AUDIT.MODE_LEVEL, set())
            unknown = sorted(
                AUDIT.method_flags(module, method) - known - AUDIT.COMMON_FLAGS
            )
            if unknown:
                problems.append(f"{module}.{method}: RAC не знает {unknown}")

        self.assertGreater(checked, 0, "ни один метод не сопоставлен со справкой rac")
        self.assertEqual(problems, [], "Параметры, которых нет в справке rac: " + str(problems))

    def test_spot_check_known_flags(self) -> None:
        # Контроль самого разбора: два параметра, которые точно есть в справке.
        server_help = AUDIT.run_help(RAC, "server")
        self.assertIn("--safe-working-processes-memory-limit", server_help)
        self.assertNotIn("--safe-working-processess-memory-limit", server_help)

        infobase_help = AUDIT.run_help(RAC, "infobase")
        self.assertIn("--drop-database", infobase_help)


if __name__ == "__main__":
    unittest.main()
