import argparse
import csv
from collections import defaultdict
from typing import Iterable, List, Mapping, Dict, Callable
from tabulate import tabulate


def read_csv_files(files: Iterable[str]) -> List[Mapping[str, str]]:
    rows = []
    for file in files:
        with open(file, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            rows.extend(reader)
    return rows

def generate_performance_report(rows: Iterable[Mapping[str, str]]) -> List[List[object]]:
    performance_by_position: Dict[str, List[float]] = defaultdict(list)

    for row in rows:
        position = row.get("position")
        if not position:
            continue
        raw = row.get("performance", "0")
        try:
            perf = float(raw)
        except (ValueError, TypeError):
            continue
        performance_by_position[position].append(perf)


    report = [
    [pos, round(sum(perfs) / len(perfs), 2)]
        for pos, perfs in performance_by_position.items()
    ]
    report.sort(key=lambda x: x[1], reverse=True)
    return report


REPORTS: Dict[str, Callable] = {
"performance": generate_performance_report,
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate reports from CSVs")
    parser.add_argument("--files", nargs="+", required=True)
    parser.add_argument("--report", required=True, choices=list(REPORTS.keys()))
    args = parser.parse_args()

    rows = read_csv_files(args.files)
    func = REPORTS[args.report]
    report = func(rows)
    print(tabulate(report, headers=["Position", "Average Performance"], tablefmt="github"))


if __name__ == "__main__":
    main()

