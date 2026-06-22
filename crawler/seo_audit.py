"""
SEO Audit Engine
Phase 4
"""

from collections import Counter


def audit_seo(results):

    audit = {
        "total_pages": len(results),
        "missing_titles": [],
        "missing_meta": [],
        "missing_h1": [],
        "duplicate_titles": [],
        "duplicate_meta": [],
        "seo_score": 100,
        "recommendations": []
    }

    # ------------------
    # Missing Checks
    # ------------------

    for page in results:

        if page["title"] == "Missing":

            audit["missing_titles"].append(
                page["url"]
            )

            audit["seo_score"] -= 10

        if page["meta_description"] == "Missing":

            audit["missing_meta"].append(
                page["url"]
            )

            audit["seo_score"] -= 5

        if page["h1"] == "Missing":

            audit["missing_h1"].append(
                page["url"]
            )

            audit["seo_score"] -= 5

    # ------------------
    # Duplicate Titles
    # ------------------

    title_counter = Counter()

    for page in results:

        title = page["title"]

        if title != "Missing":

            title_counter[title] += 1

    for title, count in title_counter.items():

        if count > 1:

            audit["duplicate_titles"].append(
                {
                    "title": title,
                    "count": count
                }
            )

            audit["seo_score"] -= 8

    # ------------------
    # Duplicate Meta
    # ------------------

    meta_counter = Counter()

    for page in results:

        meta = page["meta_description"]

        if meta != "Missing":

            meta_counter[meta] += 1

    for meta, count in meta_counter.items():

        if count > 1:

            audit["duplicate_meta"].append(
                {
                    "meta": meta,
                    "count": count
                }
            )

            audit["seo_score"] -= 5

    # ------------------
    # Score Floor
    # ------------------

    if audit["seo_score"] < 0:

        audit["seo_score"] = 0

    # ------------------
    # Recommendations
    # ------------------

    if audit["missing_titles"]:

        audit["recommendations"].append(
            f"Add titles to {len(audit['missing_titles'])} pages"
        )

    if audit["missing_meta"]:

        audit["recommendations"].append(
            f"Add meta descriptions to {len(audit['missing_meta'])} pages"
        )

    if audit["missing_h1"]:

        audit["recommendations"].append(
            f"Add H1 tags to {len(audit['missing_h1'])} pages"
        )

    if audit["duplicate_titles"]:

        audit["recommendations"].append(
            "Resolve duplicate page titles"
        )

    if audit["duplicate_meta"]:

        audit["recommendations"].append(
            "Resolve duplicate meta descriptions"
        )

    return audit