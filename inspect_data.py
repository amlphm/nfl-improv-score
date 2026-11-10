"""
One-off data inspection for the Improv Score project.

We normally use pandas, but this sandbox has no internet access to install it,
so this script uses only Python's built-in csv module. It prints the same
information (shape, columns, sample rows, value counts) for each file in
data/raw/ and is used to generate notes/data_overview.md.

Run:  python3 inspect_data.py
"""
import csv
import glob
import os
from collections import Counter

RAW = os.path.join("data", "raw")


def read_csv(path, limit=None):
    """Read a CSV into a header list and a list of row dicts.

    If limit is given, stop after that many data rows (used for the huge
    tracking files so we don't load everything into memory just to peek)."""
    with open(path, newline="") as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = []
        for i, row in enumerate(reader):
            if limit is not None and i >= limit:
                break
            rows.append(dict(zip(header, row)))
    return header, rows


def count_rows(path):
    """Count data rows (lines minus the header) without loading the file."""
    with open(path, newline="") as f:
        n = sum(1 for _ in f)
    return max(n - 1, 0)


def value_counts(path, column):
    """Return a Counter of the values in one column across the whole file."""
    counts = Counter()
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            counts[row.get(column, "")] += 1
    return counts


def describe_flat_file(name):
    """Print shape, columns, and 3 sample rows for a normal (non-tracking) CSV."""
    path = os.path.join(RAW, name)
    header, sample = read_csv(path, limit=3)
    nrows = count_rows(path)
    print(f"\n{'='*70}\nFILE: {name}")
    print(f"shape: {nrows} rows x {len(header)} columns")
    print(f"columns ({len(header)}): {header}")
    print("3 sample rows:")
    for i, row in enumerate(sample, 1):
        print(f"  [{i}] {row}")


def describe_tracking():
    """Summarise how tracking files are organised + unique event values."""
    files = sorted(glob.glob(os.path.join(RAW, "tracking", "*.csv")))
    print(f"\n{'='*70}\nTRACKING FILES")
    print(f"number of tracking files: {len(files)}")
    print("naming pattern: tracking_<gameId>.csv  (one file per game)")
    print("first few file names:")
    for p in files[:5]:
        print(f"  {os.path.basename(p)}")
    print("  ...")

    # Columns + sample from the first file
    header, sample = read_csv(files[0], limit=3)
    print(f"\ncolumns ({len(header)}): {header}")
    print(f"3 sample rows (from {os.path.basename(files[0])}):")
    for i, row in enumerate(sample, 1):
        print(f"  [{i}] {row}")

    # Unique event values across ALL tracking files
    events = Counter()
    total_rows = 0
    for p in files:
        with open(p, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                total_rows += 1
                events[row.get("event", "")] += 1
    print(f"\ntotal tracking rows across all files: {total_rows}")
    print(f"unique `event` values ({len(events)}):")
    for ev, c in events.most_common():
        label = ev if ev != "" else "(blank / no event this frame)"
        print(f"  {label:35s} {c}")


def main():
    for name in ["games.csv", "players.csv", "plays.csv", "pffScoutingData.csv"]:
        describe_flat_file(name)

    # Value counts requested for plays.csv
    for col in ["dropBackType", "passResult"]:
        print(f"\nplays.csv — value counts of `{col}`:")
        for val, c in value_counts(os.path.join(RAW, "plays.csv"), col).most_common():
            label = val if val != "" else "(blank)"
            print(f"  {label:25s} {c}")

    describe_tracking()


if __name__ == "__main__":
    main()
