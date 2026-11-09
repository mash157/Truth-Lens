import os
import json
import pandas as pd
from sklearn.model_selection import train_test_split

from ml.config import (
    RAW_DATA_PATH,
    TRAIN_DATA_PATH,
    VAL_DATA_PATH,
    TEST_DATA_PATH,
    RESULTS_DIR,
    TEST_SIZE,
    VAL_SIZE,
    RANDOM_STATE
)

from ml.preprocessing.clean_text import combine_headline_and_body


def inspect_and_prepare():
    print("Starting dataset preparation pipeline...")

    # 1. Check if raw dataset exists
    if not os.path.exists(RAW_DATA_PATH):
        raise FileNotFoundError(
            f"\n[ERROR] WELFake Dataset not found at: {RAW_DATA_PATH}\n"
            "Please download the 'WELFake_Dataset.csv' file from Kaggle:\n"
            "https://www.kaggle.com/datasets/saurabhshahane/velfake-dataset\n"
            "and place the compressed 'WELFake_Dataset.zip' file "
            "inside the 'dataset/raw/' folder.\n"
        )

    # 2. Load compressed dataset
    print(f"Loading raw dataset from {RAW_DATA_PATH}...")

    # Pandas automatically reads the CSV inside the ZIP file.
    # No manual extraction is required.
    df = pd.read_csv(
        RAW_DATA_PATH,
        compression="zip"
    )

    # 3. Basic Inspection Info
    initial_rows = len(df)
    cols = list(df.columns)

    print(f"Loaded {initial_rows} rows. Columns: {cols}")

    # Check expected columns
    required_cols = {'title', 'text', 'label'}

    if not required_cols.issubset(df.columns):
        raise ValueError(
            f"Dataset must contain columns: {required_cols}"
        )

    # 4. Handle Missing Values
    missing_title = df['title'].isnull().sum()
    missing_text = df['text'].isnull().sum()

    # Fill NaN with empty string
    df['title'] = df['title'].fillna("")
    df['text'] = df['text'].fillna("")

    # Drop rows where both title and text are empty
    empty_both = (
        (df['title'] == "") &
        (df['text'] == "")
    ).sum()

    df = df[
        ~(
            (df['title'] == "") &
            (df['text'] == "")
        )
    ]

    # 5. Remove Duplicates (pass 1, raw)
    # Check duplicates using title + text
    duplicate_count = df.duplicated(
        subset=['title', 'text']
    ).sum()

    df = df.drop_duplicates(
        subset=['title', 'text']
    )

    final_clean_rows = len(df)

    # 6. Preprocess & Combine Title & Text
    print(
        "Combining title and article text "
        "and applying clean_text..."
    )

    df['combined_text'] = df.apply(
        lambda row: combine_headline_and_body(
            row['title'],
            row['text']
        ),
        axis=1
    )

    # Remove records that became empty after cleaning
    empty_after_clean = int((df['combined_text'].str.strip() == "").sum())
    df = df[df['combined_text'].str.strip() != ""]

    # 5b. Remove near-duplicates (pass 2, normalized text key)
    # Catches articles whose bodies are identical after lowercasing and
    # whitespace normalization but differ in title or punctuation. This
    # prevents the same underlying article from leaking across the
    # train / validation / test boundaries.
    df['_norm_text_key'] = (
        df['text']
        .fillna("")
        .map(lambda s: " ".join(str(s).lower().split()))
    )
    duplicate_count += int(df.duplicated(subset=['_norm_text_key']).sum())
    df = df.drop_duplicates(subset=['_norm_text_key'])
    df = df.drop(columns=['_norm_text_key'])

    final_clean_rows = len(df)

    # 7. Calculate Text Length Statistics
    # Use raw article text word counts
    word_counts = df['text'].apply(
        lambda x: len(x.split())
        if isinstance(x, str)
        else 0
    )

    avg_text_length = float(word_counts.mean())
    min_text_length = int(word_counts.min())
    max_text_length = int(word_counts.max())

    # Class distribution
    class_counts = df['label'].value_counts().to_dict()

    # 0 = Genuine, 1 = Fake
    genuine_count = int(class_counts.get(0, 0))
    fake_count = int(class_counts.get(1, 0))

    total_class_sum = genuine_count + fake_count

    genuine_percent = (
        (genuine_count / total_class_sum) * 100
        if total_class_sum > 0
        else 0
    )

    fake_percent = (
        (fake_count / total_class_sum) * 100
        if total_class_sum > 0
        else 0
    )

    print(
        f"Class Distribution: "
        f"{genuine_count} Genuine "
        f"({genuine_percent:.2f}%), "
        f"{fake_count} Fake "
        f"({fake_percent:.2f}%)"
    )

    # 8. Stratified Split (Train, Validation, Test)

    # First: split off the test set
    print(
        "Splitting dataset into train, "
        "validation, and test sets..."
    )

    train_val_df, test_df = train_test_split(
        df,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=df['label']
    )

    # Second: split remaining data into
    # train and validation
    val_ratio_adjusted = VAL_SIZE / (1.0 - TEST_SIZE)

    train_df, val_df = train_test_split(
        train_val_df,
        test_size=val_ratio_adjusted,
        random_state=RANDOM_STATE,
        stratify=train_val_df['label']
    )

    print(f"Train samples: {len(train_df)}")
    print(f"Validation samples: {len(val_df)}")
    print(f"Test samples: {len(test_df)}")

    # Save splits
    train_df.to_csv(
        TRAIN_DATA_PATH,
        index=False
    )

    val_df.to_csv(
        VAL_DATA_PATH,
        index=False
    )

    test_df.to_csv(
        TEST_DATA_PATH,
        index=False
    )

    print(
        f"Saved split files to "
        f"{TRAIN_DATA_PATH.parent}"
    )

    # 9. Compile Statistics JSON
    stats = {
        "raw_record_count": initial_rows,
        "clean_record_count": final_clean_rows,
        "columns": cols,

        "missing_values": {
            "title": int(missing_title),
            "text": int(missing_text),
            "both_empty": int(empty_both),
            "empty_after_cleaning": int(empty_after_clean)
        },

        "duplicate_records": int(duplicate_count),

        "class_distribution": {
            "genuine": genuine_count,
            "fake": fake_count
        },

        "class_percentages": {
            "genuine": float(
                round(genuine_percent, 2)
            ),
            "fake": float(
                round(fake_percent, 2)
            )
        },

        "text_length": {
            "min_words": min_text_length,
            "max_words": max_text_length,
            "avg_words": float(
                round(avg_text_length, 2)
            )
        },

        "splits": {
            "train": len(train_df),
            "validation": len(val_df),
            "test": len(test_df)
        }
    }

    stats_file = RESULTS_DIR / "dataset_statistics.json"

    with open(stats_file, 'w') as f:
        json.dump(
            stats,
            f,
            indent=4
        )

    print(
        f"Dataset statistics saved to {stats_file}"
    )

    return stats


if __name__ == "__main__":
    inspect_and_prepare()