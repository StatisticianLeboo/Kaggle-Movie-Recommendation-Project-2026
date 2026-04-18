from pathlib import Path

from src.data.loaders import load_movies_data, load_sample_submission, load_test_data, load_train_data


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    data_dir = project_root / "data" / "movie-recommendation-hackathon-2026"

    train = load_train_data(data_dir)
    test = load_test_data(data_dir)
    movies = load_movies_data(data_dir)
    sample_submission = load_sample_submission(data_dir)

    print("Train shape:", train.shape)
    print("Test shape:", test.shape)
    print("Movies shape:", movies.shape)
    print("Sample submission shape:", sample_submission.shape)
    print()
    print("Train columns:", list(train.columns))
    print("Test columns:", list(test.columns))
    print("Movies columns:", list(movies.columns))
    print("Sample submission columns:", list(sample_submission.columns))


if __name__ == "__main__":
    main()