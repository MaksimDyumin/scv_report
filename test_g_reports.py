from g_reports import read_csv_files, generate_performance_report, main
import pytest

def test_generate_performance_report_basic(tmp_path):
    file1 = tmp_path / "data1.csv"
    file1.write_text(
        """name,position,completed_tasks,performance,skills,team,experience_years
Alex,Backend,10,4.0,Python,API,3
Bob,Backend,20,5.0,Python,API,4
Carla,QA,15,3.0,Testing,QA,2
""",
        encoding="utf-8",
    )

    report = generate_performance_report(read_csv_files([str(file1)]))

    # Expected averages:
    # Backend: (4.0 + 5.0) / 2 = 4.5
    # QA: 3.0

    assert ["Backend", 4.5] in report
    assert ["QA", 3.0] in report

    # Sorted by performance
    assert report[0][1] >= report[1][1]


def test_generate_performance_report_multiple_files(tmp_path):
    file1 = tmp_path / "data1.csv"
    file2 = tmp_path / "data2.csv"

    file1.write_text(
        """name,position,performance
A,DevOps,4.0
B,DevOps,5.0
""",
        encoding="utf-8",
    )

    file2.write_text(
        """name,position,performance
C,DevOps,3.0
D,QA,4.5
""",
        encoding="utf-8",
    )

    rows = read_csv_files([str(file1), str(file2)])
    report = generate_performance_report(rows)

    # DevOps avg = (4 + 5 + 3) / 3 = 4.0
    assert ["DevOps", 4.0] in report
    assert ["QA", 4.5] in report


def test_generate_performance_report_invalid_values(tmp_path):
    file1 = tmp_path / "data.csv"
    file1.write_text(
        """name,position,performance
A,DevOps,notnum
B,DevOps,4.0
""",
        encoding="utf-8",
    )

    report = generate_performance_report(read_csv_files([str(file1)]))

    assert ["DevOps", 4.0] in report


def test_generate_performance_report_zero_performance(tmp_path):
    file1 = tmp_path / "data.csv"
    file1.write_text(
        """name,position,performance
A,Support,0.0
B,Support,4.0
""",
        encoding="utf-8",
    )

    report = generate_performance_report(read_csv_files([str(file1)]))

    # Average = (0 + 4) / 2 = 2.0
    assert ["Support", 2.0] in report


def test_generate_performance_report_missing_position(tmp_path):
    file1 = tmp_path / "data.csv"
    file1.write_text(
        """name,position,performance
A,,4.0
B,DevOps,5.0
""",
        encoding="utf-8",
    )

    report = generate_performance_report(read_csv_files([str(file1)]))

    assert ["DevOps", 5.0] in report
    assert all(row[0] != "" for row in report)


def test_main_argparse_invalid_report(monkeypatch):
    """Проверяем, что argparse вызывает SystemExit при неизвестном отчёте."""
    import sys
    monkeypatch.setattr(sys, "argv", ["g_reports.py", "--files", "dummy.csv", "--report", "unknown"])

    with pytest.raises(SystemExit) as excinfo:
        main()
    assert excinfo.value.code == 2 