#!/usr/bin/env python
from __future__ import annotations
import bibtexparser as bibx
import pandas as pd
from pathlib import Path

import os
from copy import copy
from dataclasses import dataclass
import io
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

log = logging.getLogger(__name__)

## Constants
PAGE_TEMPLATE = """# {title}

> By {author}

- **Macro-area**: {macroarea}
- **Topic**: {topic}
- **Year**: {year}
- **Transportome layer investigated**: {transportome}

- References:
  - Journal: {journal}
  - DOI: [{doi}](https://doi.org/{doi})
  - PMID: {pmid}

### Abstract

{abstract}
"""

README = {
    "template": "# Index \n\n{readme_lines}",
    "lines": {
        "full": "- ({year}) - {topic}: [{title}](https://doi.org/{doi}) ([Pubmed](https://pubmed.ncbi.nlm.nih.gov/{pmid}))",
        "year": "- {topic}: [{title}](https://doi.org/{doi}) ([Pubmed](https://pubmed.ncbi.nlm.nih.gov/{pmid}))",
        "topic": "- ({year}): [{title}](https://doi.org/{doi}) ([Pubmed](https://pubmed.ncbi.nlm.nih.gov/{pmid}))",
    },
}
README_TEMPLATE = """# Index

{readme_lines}
"""


SPLIT_COLS = {
    "macroarea": {
        "display": "by macroarea",
        "readme_line_template": README["lines"]["full"],
    },
    "topic": {"display": "by topic", "readme_line_template": README["lines"]["topic"]},
    "year": {"display": "by year", "readme_line_template": README["lines"]["year"]},
    "transportome": {
        "display": "by transportomic target",
        "readme_line_template": README["lines"]["full"],
    },
}
"""
A dict that governs over which strings to split on. Plus,
it directs which README lines to use to make that split.
"""


class MissingKeyError(Exception):
    pass


@dataclass
class Entry:
    pmid: str
    macroarea: str = None
    topic: str = None
    transportome: str = None
    doi: str = None
    year: str = None
    journal: str = None
    author: str = None
    title: str = None
    abstract: str = None

    def fill_with_bib(self, bib: dict) -> Entry:
        new_dict = copy(self.__dict__)
        for key, value in self.__dict__.items():
            value = bib.get(key)
            if value is not None:
                new_dict[key] = value

        self.__dict__ = new_dict

        return self

    @property
    def full(self) -> bool:
        return not all([x is None for x in self.__dict__.values()])

    def validate(self):
        if self.full:
            return
        missing_keys = [x for x, value in self.__dict__.items() if value is None]

        raise MissingKeyError(
            "Missing keys: {} for entry {self}".format(
                ", ".join(missing_keys), self=self
            )
        )

    def __str__(self) -> str:
        return f"<Entry with PMID {self.pmid}>"

    def __getitem__(self, key) -> str:
        return self.__dict__[key]


def make_entries_from_csv(frame: pd.DataFrame) -> list[Entry]:
    entries = list()

    for _, row in frame.iterrows():
        entries.append(
            Entry(
                macroarea=row["MACROAREA"],
                topic=row["TOPIC"],
                pmid=row["PMID"],
                transportome=row["TRANSPORTOME"],
            )
        )

    return entries


def make_readme_section(entries: list[Entry], line_template: str) -> io.StringIO:
    formatted_lines = []

    for entry in entries:
        formatted_lines.append(line_template.format(**entry.__dict__))

    return io.StringIO("\n".join(formatted_lines))


def make_readme(
    exploded_entries: dict[str, list[Entry]], template: str, line_template: str
) -> io.StringIO:
    readme_lines = []
    for key, entries in exploded_entries.items():
        section_lines = make_readme_section(entries, line_template).readlines()
        # We need to pad this by a bit since it's indented
        section_lines = [f"  {line}" for line in section_lines]
        section_lines.sort()
        readme_lines.append(f"- {key}")
        readme_lines.extend(section_lines)

    return io.StringIO(template.format(readme_lines="\n".join(readme_lines)))


def make_page_from_entry(entry: Entry, template: str) -> io.StringIO:
    entry.validate()
    return io.StringIO(template.format(**entry.__dict__))


def load_bib(stream: io.StringIO):
    def customize(record):
        record = bibx.customization.convert_to_unicode(record)

        # Replace slashes with the U+2215 division symbol in 'title' field
        if 'title' in record:
            record['title'] = record['title'].replace('/', '\u2215')

        return record

    parser = bibx.bparser.BibTexParser(common_strings=True, customization=customize)

    bib_data = bibx.load(stream, parser)

    return bib_data


def explode_entries_by_var(entries: list[Entry], var: str):
    # TODO: This is not particularly efficient, but who cares.
    # We could make the buckets and put the items in in just one
    # pass through the list, while here we make len(possible_values) + 1 passes
    possible_values = set([x[var] for x in entries])
    result = {}
    for value in possible_values:
        result[value] = [x for x in entries if x[var] == value]

    return result


def get_file_title_from_entry(entry: Entry) -> str:
    return f"{entry.title}.md"


def write_file(file: tuple(Path, io.StringIO)) -> None:
    path = file[0]
    content = file[1]

    assert isinstance(path, Path), f"{path} is not a path"
    assert isinstance(content, io.StringIO), f"{content} is not a path"

    log.debug(f"Writing {path}...")
    os.makedirs(path.parent, exist_ok=True)
    with file[0].open("w+") as stream:
        stream.writelines(content.readlines())


def get_bib_from_entries(
    entries: list[Entry], bib: bibx.bibdatabase.BibDatabase
) -> bibx.bibdatabase.BibDatabase:
    selection_pmids = [x.pmid for x in entries]
    # I .get(..., "null") to avoid accidentally having None in selection_pmids
    # validating everything.
    selected_entries = [x for x in bib.entries if x.get("pmid", "null") in selection_pmids]

    db = bibx.bibdatabase.BibDatabase()
    db.entries = selected_entries

    return db

def get_entry(pmid: str, bib: bibx.bibdatabase.BibDatabase):
    for item in bib.entries:
        if item.get("pmid") == pmid or item.get("PMID") == pmid:
            return item

    raise ValueError(f"Cannot find pmid {pmid} in bibliography!")

def main(bib_file: Path, csv_file: Path, output_dir: Path):
    # I do this ALL the time. There must be a better way...
    bib_file = bib_file.expanduser().resolve()
    csv_file = csv_file.expanduser().resolve()
    output_dir = output_dir.expanduser().resolve()

    log.info(f"Reading csv file @ {csv_file}")
    frame = pd.read_csv(csv_file, header=0, dtype=str)

    log.info(f"Loading bib entries @ {bib_file}")
    with bib_file.open("r+") as file:
        bib = load_bib(file)

    log.info("Making entries...")
    entries = make_entries_from_csv(frame)
    log.info(f"Made {len(entries)} partial entries.")

    # I don't like this, since the state has to change before
    # we use the entry, but since it's such a simple use case
    # I'll just do it like this since it's easy
    log.info("Filling entries with bib data...")
    entries = [entry.fill_with_bib(get_entry(entry.pmid, bib)) for entry in entries]

    log.info("Validating all entries...")
    [x.validate() for x in entries]

    # Ok, so here we have a list of filled entries. We just
    # need to create the various sub-lists.
    files: list[tuple[Path, io.StringIO]] = list()

    for split_key, vars in SPLIT_COLS.items():
        sublists = explode_entries_by_var(entries, split_key)
        readme = make_readme(
            exploded_entries=sublists,
            template=README["template"],
            line_template=vars["readme_line_template"],
        )
        files.append((output_dir / vars["display"] / "README.md", readme))
        for value, sublist in sublists.items():
            base_path = output_dir / vars["display"] / str(value)
            # Save each entry file
            for entry in sublist:
                files.append(
                    (
                        base_path / get_file_title_from_entry(entry),
                        make_page_from_entry(entry, PAGE_TEMPLATE),
                    )
                )
            # Save the bib
            files.append(
                (
                    base_path / ".library.bib",
                    io.StringIO(bibx.dumps(get_bib_from_entries(sublist, bib))),
                )
            )

    log.info(f"Writing {len(files)} files...")
    for file in files:
        write_file(file)

    log.info(f"Done regenerating {output_dir}!")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("bib_file", type=Path, help="Bib file to parse")
    parser.add_argument(
        "csv_structure",
        type=Path,
        help="A .csv file with specific columns to use to guide the population of the library.",
    )
    parser.add_argument("out_dir", type=Path, help="Output directory to save files to.")
    args = parser.parse_args()

    main(
        bib_file=args.bib_file,
        csv_file=args.csv_structure,
        output_dir=args.out_dir,
    )
