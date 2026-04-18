from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Validate Kaggle submission CSV format and quality checks "
            "for movie recommendation predictions."
        )
    )
    parser.add_argument(
        "--file",
        type=Path,
        default=Path("submissions/user_cf_submission.csv"),
        help="Path to submission CSV file.",
    )
    parser.add_argument(
        "--expected-rows",
        type=int,
        default=None,
        help="Expected number of rows (optional).",
    )
    parser.add_argument(
        "--min-rating",
        type=float,
        default=0.5,
        help="Minimum allowed rating.",
    )
    parser.add_argument(
        "--max-rating",
        type=float,
        default=5.0,
        help="Maximum allowed rating.",
    )
    parser.add_argument(
        "--allow-duplicates",
        action="store_true",
        help="Allow duplicate Id values (not recommended).",
    )
    return parser


def validate_submission(
    file_path: Path,
    expected_rows: int | None,
    min_rating: float,
    max_rating: float,
    allow_duplicates: bool,
) -> tuple[bool, list[str]]:
    errors: list[str] = []

    if not file_path.exists():
        return False, [f"File does not exist: {file_path}"]

    try:
        df = pd.read_csv(file_path)
    except Exception as exc:  # noqa: BLE001
        return False, [f"Failed to read CSV: {exc}"]

    expected_cols = ["Id", "rating"]
    cols = list(df.columns)
    if cols != expected_cols:
        errors.append(f"Invalid columns. Expected {expected_cols}, got {cols}")

    if expected_rows is not None and len(df) != expected_rows:
        errors.append(
            f"Row count mismatch. Expected {expected_rows}, got {len(df)}"
        )

    if "Id" in df.columns:
        missing_id = int(df["Id"].isna().sum())
        if missing_id > 0:
            errors.append(f"Found {missing_id} missing Id values")

        if not allow_duplicates:
            duplicate_count = int(df["Id"].duplicated().sum())
            if duplicate_count > 0:
                errors.append(f"Found {duplicate_count} duplicate Id values")

    if "rating" in df.columns:
        rating_numeric = pd.to_numeric(df["rating"], errors="coerce")
        missing_rating = int(rating_numeric.isna().sum())
        if missing_rating > 0:
            errors.append(f"Found {missing_rating} non-numeric or missing ratings")
        else:
            below_min = int((rating_numeric < min_rating).sum())
            above_max = int((rating_numeric > max_rating).sum())
            if below_min > 0 or above_max > 0:
                errors.append(
                    "Rating out of bounds. "
                    f"Below min: {below_min}, Above max: {above_max}, "
                    f"Allowed range: [{min_rating}, {max_rating}]"
                )

    return len(errors) == 0, errors


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    is_valid, errors = validate_submission(
        file_path=args.file,
        expected_rows=args.expected_rows,
        min_rating=args.min_rating,
        max_rating=args.max_rating,
        allow_duplicates=args.allow_duplicates,
    )

    print("Submission Validation")
    print("---------------------")
    print(f"File: {args.file}")

    if is_valid:
        df = pd.read_csv(args.file)
        print("Status: PASS")
        print(f"Rows: {len(df):,}")
        print(
            "Rating range: "
            f"{df['rating'].min():.4f} to {df['rating'].max():.4f}"
        )
        print("Checks: columns, nulls, numeric ratings, bounds, duplicates")
        return 0

    print("Status: FAIL")
    for error in errors:
        print(f"- {error}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
