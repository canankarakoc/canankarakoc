#!/usr/bin/env python3
"""Add a paper to publications.yml from its DOI.

    python3 scripts/add_publication.py 10.1073/pnas.2524274123
    python3 scripts/add_publication.py https://doi.org/10.1111/brv.70079 --dry-run

The details (title, authors, journal, volume, year, abstract) are looked up
at doi.org and written as a new entry at the top of publications.yml.
Check the entry afterwards: add `note:`, `code:` or `pdf:` lines if needed.
Needs only Python 3 (no extra packages).
"""
import argparse
import html
import json
import re
import sys
import textwrap
import unicodedata
import urllib.error
import urllib.request
from pathlib import Path

PUBS = Path(__file__).resolve().parent.parent / "publications.yml"
ME = "Karakoç C"  # written exactly like this so the website can bold it


def clean_doi(text):
    match = re.search(r"10\.\d{4,9}/\S+", text.strip())
    if not match:
        sys.exit(f"That does not look like a DOI: {text!r}")
    return match.group(0).rstrip(".")


def fetch(doi):
    req = urllib.request.Request(
        "https://doi.org/" + doi,
        headers={
            "Accept": "application/vnd.citationstyles.csl+json",
            "User-Agent": "ckarakoc.com publication helper (+https://www.ckarakoc.com)",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as err:
        sys.exit(f"doi.org could not find {doi} ({err.code}). Check the DOI.")
    except urllib.error.URLError as err:
        sys.exit(f"Could not reach doi.org: {err.reason}")


def fold(s):
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()


def short_name(person):
    family = (person.get("family") or person.get("literal") or "").strip()
    given = (person.get("given") or "").replace(".", " ")
    initials = " ".join(
        "-".join(part[0] for part in word.split("-") if part) for word in given.split()
    ).replace(" ", "")
    name = f"{family} {initials}".strip()
    return ME if fold(name) == fold(ME) else name


def plain(text):
    """Strip JATS/HTML tags; keep <i>/<em> as *italics*."""
    text = re.sub(r"</?(i|em)>", "*", text or "")
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(re.sub(r"\s+", " ", text)).strip()
    return re.sub(r"^Abstract\s*", "", text)


def first(value):
    return (value[0] if isinstance(value, list) and value else value) or ""


def entry_from_csl(data):
    year = (data.get("issued") or data.get("published-print") or data.get("published-online") or {})
    year = (year.get("date-parts") or [[None]])[0][0]
    volume, issue = data.get("volume"), data.get("issue")
    pages = data.get("page") or data.get("article-number")
    details = ""
    if volume:
        details = str(volume) + (f"({issue})" if issue else "")
    if pages:
        details = f"{details}: {pages}" if details else str(pages)
    return {
        "title": plain(first(data.get("title"))),
        "authors": ", ".join(short_name(a) for a in data.get("author", [])),
        "journal": plain(first(data.get("container-title")) or data.get("publisher") or ""),
        "details": details.replace("--", "–"),
        "year": year,
        "doi": data.get("DOI", ""),
        "abstract": plain(data.get("abstract", "")),
    }


def to_yaml(entry):
    lines = []
    for key in ["title", "authors", "journal", "details", "year", "doi"]:
        value = entry.get(key)
        if value in (None, ""):
            continue
        if isinstance(value, str) and (re.search(r"[:#'\"\[\]{}&*!|>%@`]", value) or value[0] in "-?"):
            value = json.dumps(value, ensure_ascii=False)
        lines.append(f"{'- ' if not lines else '  '}{key}: {value}")
    if entry.get("abstract"):
        lines.append("  abstract: >-")
        lines += ["    " + l for l in textwrap.wrap(entry["abstract"], 76, break_on_hyphens=False)]
    return "\n".join(lines) + "\n"


def insert(entry_text):
    text = PUBS.read_text(encoding="utf-8")
    at = text.find("\n- ")  # first existing entry
    at = len(text) if at < 0 else at + 1
    PUBS.write_text(text[:at] + entry_text + "\n" + text[at:], encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Add a paper to publications.yml from its DOI.")
    parser.add_argument("doi", help="DOI or doi.org link")
    parser.add_argument("--dry-run", action="store_true", help="only print the entry")
    args = parser.parse_args()

    doi = clean_doi(args.doi)
    if doi.lower() in PUBS.read_text(encoding="utf-8").lower():
        sys.exit(f"{doi} is already in publications.yml")

    entry = entry_from_csl(fetch(doi))
    entry_text = to_yaml(entry)
    print(entry_text)
    if ME not in entry["authors"]:
        print(f"Note: '{ME}' was not found in the author list; check how your name is spelled.")
    if fold(entry["title"]).replace("*", "") in fold(PUBS.read_text(encoding="utf-8")).replace("*", ""):
        print("Note: an entry with this title is already listed (in press / under review?). "
              "Delete the old one after adding this.")
    if not args.dry_run:
        insert(entry_text)
        print(f"Added to {PUBS.name}. Review it, then commit.")


if __name__ == "__main__":
    main()
