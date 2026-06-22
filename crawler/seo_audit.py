"""
seo_audit.py

Phase 3 SEO Audit Engine
"""

from collections import Counter


def audit_seo(results):

    summary = {
        "total_pages": len(results),
        "missing_titles": [],
        "missing_meta": [],
        "missing_h1": [],
        "duplicate_titles": [],
        "duplicate_meta": []
    }

    # -----------------------------
    # Missing Checks
    # -----------------------------

    for page in results:

        if (
            not page["title"]
            or page["title"] == "Missing"
        ):
            summary["missing_titles"].append(
                page["url"]
            )

        if (
            not page["meta_description"]
            or page["meta_description"] == "Missing"
        ):
            summary["missing_meta"].append(
                page["url"]
            )

        if (
            not page["h1"]
            or page["h1"] == "Missing"
        ):
            summary["missing_h1"].append(
                page["url"]
            )

    # -----------------------------
    # Duplicate Titles
    # -----------------------------

    title_counter = Counter()

    for page in results:

        title = page["title"]

        if title != "Missing":
            title_counter[title] += 1

    duplicate_titles = [
        title
        for title, count
        in title_counter.items()
        if count > 1
    ]

    summary["duplicate_titles"] = duplicate_titles

    # -----------------------------
    # Duplicate Meta
    # -----------------------------

    meta_counter = Counter()

    for page in results:

        meta = page["meta_description"]

        if meta != "Missing":
            meta_counter[meta] += 1

    duplicate_meta = [
        meta
        for meta, count
        in meta_counter.items()
        if count > 1
    ]

    summary["duplicate_meta"] = duplicate_meta

    return summary