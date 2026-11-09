"""One-off diagnostic: measure duplicate / near-duplicate overlap across splits."""
import sys
import os
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ml.config import TRAIN_DATA_PATH, VAL_DATA_PATH, TEST_DATA_PATH


def normalize(s):
    if not isinstance(s, str):
        return ""
    return " ".join(s.lower().split())


def main():
    train = pd.read_csv(TRAIN_DATA_PATH)
    val = pd.read_csv(VAL_DATA_PATH)
    test = pd.read_csv(TEST_DATA_PATH)

    for name, df in [("train", train), ("val", val), ("test", test)]:
        print(f"{name}: {len(df)} rows")

    pairs = [("train", train), ("val", val), ("test", test)]

    # Build normalized keys
    for df in (train, val, test):
        df["_norm_combined"] = (df["title"].fillna("").map(normalize) + " || " +
                                df["text"].fillna("").map(normalize))
        df["_norm_text"] = df["text"].fillna("").map(normalize)
        df["_norm_title"] = df["title"].fillna("").map(normalize)

    def report(keycol, label):
        sets = {name: set(df[keycol]) for name, df in pairs}
        print(f"\n=== Cross-split overlap by {label} ===")
        for a, b in [("train", "val"), ("train", "test"), ("val", "test")]:
            inter = sets[a] & sets[b]
            inter.discard("")
            smaller = min(len(sets[a]), len(sets[b]))
            print(f"  {a} & {b}: {len(inter)} shared keys "
                  f"({len(inter)/smaller*100:.2f}% of smaller split)")

    report("_norm_combined", "normalized title+text")
    report("_norm_text", "normalized text only")
    report("_norm_title", "normalized title only")

    # Also: within-dataset remaining exact dupes on normalized combined
    all_df = pd.concat([train, val, test], ignore_index=True)
    dupes = all_df.duplicated(subset=["_norm_combined"]).sum()
    print(f"\nExact duplicates (normalized combined) remaining across ALL splits: {dupes}")
    dupes_text = all_df[all_df["_norm_combined"] != ""].duplicated(subset=["_norm_text"]).sum()
    print(f"Exact duplicates (normalized text-only) remaining across ALL splits: {dupes_text}")


if __name__ == "__main__":
    main()
