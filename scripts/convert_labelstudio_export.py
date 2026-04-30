#!/usr/bin/env python3
"""
Convert a Label Studio JSON export into a GitHub-safe annotation summary.

This script summarizes annotations without exporting the original learner texts.
It creates:
1. annotation_summary_no_text.csv
2. annotation_summary_readable.md
"""

import argparse
import json
from collections import Counter
from pathlib import Path

import pandas as pd


def convert(input_json: str, output_dir: str) -> None:
    data = json.load(open(input_json, encoding="utf-8"))
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    rows = []
    all_labels = set()

    # First pass: collect labels
    for item in data:
        for ann in item.get("annotations", []):
            for result in ann.get("result", []):
                if result.get("type") == "labels":
                    for label in result.get("value", {}).get("labels", []):
                        all_labels.add(label)

    for idx, item in enumerate(data, start=1):
        results = []
        for ann in item.get("annotations", []):
            results.extend(ann.get("result", []))

        if not results:
            continue

        text = item.get("data", {}).get("text", "")
        counts = Counter()
        proficiency_labels = []

        for result in results:
            value = result.get("value", {})

            if result.get("type") == "labels":
                for label in value.get("labels", []):
                    counts[label] += 1

            elif result.get("type") == "choices":
                proficiency_labels.extend(value.get("choices", []))

        row = {
            "sample_id": item.get("id", idx),
            "word_count": len(str(text).split()),
            "character_count": len(str(text)),
            "proficiency_label": proficiency_labels[0] if proficiency_labels else "",
            "total_error_annotations": sum(counts.values()),
        }

        for label in sorted(all_labels):
            row[label] = counts.get(label, 0)

        rows.append(row)

    df = pd.DataFrame(rows)
    base_cols = [
        "sample_id",
        "word_count",
        "character_count",
        "proficiency_label",
        "total_error_annotations",
    ]
    error_cols = [col for col in df.columns if col not in base_cols]
    df = df[base_cols + error_cols].sort_values("sample_id")

    csv_path = output / "annotation_summary_no_text.csv"
    df.to_csv(csv_path, index=False)

    summary_counts = df[error_cols].sum().sort_values(ascending=False)
    prof_counts = df["proficiency_label"].replace("", "Unlabeled").value_counts()

    md = []
    md.append("# Annotation Summary\n")
    md.append(
        "This file summarizes a Label Studio annotation export without redistributing "
        "the original learner texts. It is intended for a public portfolio repository.\n"
    )

    md.append("## Dataset Export Summary\n")
    md.append(f"- Annotated/exported samples summarized: **{len(df)}**")
    md.append(
        f"- Total token-level error annotations: "
        f"**{int(df['total_error_annotations'].sum())}**"
    )
    md.append(
        f"- Document-level proficiency labels present: "
        f"**{int((df['proficiency_label'] != '').sum())}**\n"
    )

    md.append("## Proficiency Label Counts\n")
    md.append("| Proficiency label | Count |")
    md.append("|---|---:|")
    for label, count in prof_counts.items():
        md.append(f"| {label} | {count} |")

    md.append("\n## Error Label Counts\n")
    md.append("| Error label | Count |")
    md.append("|---|---:|")
    for label, count in summary_counts.items():
        if count:
            md.append(f"| `{label}` | {int(count)} |")

    md.append("\n## Example Sample Summaries\n")
    md.append(
        "These examples show annotation density and label distribution by sample. "
        "Original text is omitted for licensing/privacy reasons.\n"
    )
    md.append("| Sample ID | Words | Proficiency | Total errors | Top error labels |")
    md.append("|---:|---:|---|---:|---|")

    for _, row in df.head(12).iterrows():
        counts = {
            label: int(row[label])
            for label in error_cols
            if int(row[label]) > 0
        }
        top = ", ".join(
            f"`{label}`={count}"
            for label, count in sorted(counts.items(), key=lambda item: -item[1])[:4]
        )
        proficiency = row["proficiency_label"] or "—"
        md.append(
            f"| {int(row['sample_id'])} | {int(row['word_count'])} | "
            f"{proficiency} | {int(row['total_error_annotations'])} | {top} |"
        )

    md_path = output / "annotation_summary_readable.md"
    md_path.write_text("\n".join(md), encoding="utf-8")

    print(f"Wrote {csv_path}")
    print(f"Wrote {md_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_json", required=True)
    parser.add_argument("--output_dir", default="examples")
    args = parser.parse_args()

    convert(args.input_json, args.output_dir)
