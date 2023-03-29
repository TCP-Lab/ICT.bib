#!/usr/bin/env python

### >>>> BIG DISCLAIMER <<<<<
# This is a very - very - bad script to quickly regen the library from the
# tables that we had + the .bib files from Mendeley/Zotero that we had before.
# Please don't judge me for it. I had like 3 hours to make it.

import bibtexparser as bibx
import pandas as pd
from pathlib import Path

import os
from copy import copy

TEMPLATE = """{title}

>> By {authors} ({year})

Macroarea: "{scope}"
Topic: {target}
Transportome considered: {transportome}

References:
    Journal: {journal}
    DOI: {doi}
    PMID: {pmid}

Abstract:
    {abstract}
"""

README_TEMPLATE = """# Index

{readme_lines}
"""
README_SECTION_TEMPLATE = "- {value}:"
README_LINE_TEMPLATE_FULL = "  - ({year}) - {scope}: [{title}](https://doi.org/{doi}) ([Pubmed](https://pubmed.ncbi.nlm.nih.gov/{pmid}))"
README_LINE_TEMPLATE_YEAR = "  - {scope}: [{title}](https://doi.org/{doi}) ([Pubmed](https://pubmed.ncbi.nlm.nih.gov/{pmid}))"
README_LINE_TEMPLATE_SCOPE = "  - ({year}): [{title}](https://doi.org/{doi}) ([Pubmed](https://pubmed.ncbi.nlm.nih.gov/{pmid}))"


def get_entry(pmid: str, bib: dict):
    for item in bib:
        if bib[item]["PMID"] == pmid:
            return bib[item]

    raise ValueError(f"Cannot find pmid {pmid} in bibliography!")


def main(
    bib_file: Path,
    csv_structure: Path,
    output_dir: Path,
    pmid_col: str = "PMID",
):
    print(f"Reading csv file {bib_file}...")
    with bib_file.open("r") as stream:
        parser = bibx.bparser.BibTexParser()
        parser.customization = bibx.customization.homogenize_latex_encoding

        bib_data = bibx.load(stream)

    print("Taking out PMIDs...")
    available_pmids = []
    for entry in bib_data.entries:
        if "pmid" in entry:
            available_pmids.append(entry["pmid"])

    print(f"Loading csv table {csv_structure}...")
    with csv_structure.open("r") as stream:
        table = pd.read_csv(stream, header=0, dtype=str)

    needed_cols = {
        "SCOPE": "by scope",
        "YEAR": "by year",
        "TRANSPORTOME": "by target",
    }

    assert all(
        [x in table.columns.to_list() for x in needed_cols]
    ), f"Missing columns in table: {[x for x in needed_cols if x not in table.columns]} (available: {table.columns})"
    assert pmid_col in table.columns, "Missing PMID col in table"
    assert all(
        [x in available_pmids for x in table[pmid_col].to_list()]
    ), f"There are PMIDs in the table not in the .bib: {[x for x in table[pmid_col].to_list() if x not in available_pmids]}"

    print("Writing output files...")
    # Remove bib entries if there is no bib
    available_bibs = []
    for entry in bib_data.entries:
        if "pmid" in entry:
            available_bibs.append(entry)
    # We need to fi
    for col, folder_name in needed_cols.items():
        print(f"Ordering entries {folder_name}...")
        os.makedirs(output_dir / folder_name, exist_ok=True)

        readme_lines = []

        for value in sorted(set(table[col].tolist())):
            print(f"Saving value {value}...")
            os.makedirs(output_dir / folder_name / value, exist_ok=True)
            # Get the PMIDs of the values that are needed to be populated in this
            # folder
            pmid_set = table.loc[table[col] == value, pmid_col].to_list()

            # Get the corresponding .bib entries.
            bibs = [x for x in available_bibs if x["pmid"] in pmid_set]
            # If the asserts above passed, this must be correct
            print([x["pmid"] for x in bibs])
            print(pmid_set)
            assert len(bibs) == len(
                pmid_set
            ), f"Something went horribly wrong? : {len(bibs)} vs {len(pmid_set)}"

            # Save the bib files...
            for single_bib in bibs:
                # ... as single files...
                filename = "{}.txt".format(single_bib["title"])
                # Replace weird {}
                filename = filename.replace("/", "").replace("}", "").replace("{", "")

                with (output_dir / folder_name / value / filename).open(
                    "w+"
                ) as out_file:
                    out_file.write(
                        TEMPLATE.format(
                            title=single_bib["title"].replace("{", "").replace("}", ""),
                            authors=single_bib["author"],
                            year=single_bib["year"],
                            # This is pretty bad, but it takes the single data from
                            # the table @ col = col and pmid_col = pmid
                            scope=table["SCOPE"][
                                table[pmid_col] == single_bib["pmid"]
                            ].to_list()[0],
                            target=table["TARGET"][
                                table[pmid_col] == single_bib["pmid"]
                            ].to_list()[0],
                            transportome=table["TRANSPORTOME"][
                                table[pmid_col] == single_bib["pmid"]
                            ].to_list()[0],
                            journal=single_bib["journal"],
                            doi=single_bib["doi"],
                            pmid=single_bib["pmid"],
                            abstract=single_bib["abstract"]
                            if "abstract" in single_bib
                            else "N/A",
                        )
                    )
            # ... and as a single README file in the folder.
            readme_lines.append(README_SECTION_TEMPLATE.format(value=value))
            for single_bib in bibs:
                # This is pretty bad to do, but all of this script is bad, so...
                template = README_LINE_TEMPLATE_FULL
                if col == "SCOPE":
                    template = README_LINE_TEMPLATE_SCOPE
                if col == "YEAR":
                    template = README_LINE_TEMPLATE_YEAR
                readme_lines.append(
                    template.format(
                        year=single_bib["year"],
                        scope=table["SCOPE"][
                            table[pmid_col] == single_bib["pmid"]
                        ].to_list()[0],
                        title=single_bib["title"].replace("{", "").replace("}", ""),
                        doi=single_bib["doi"].replace(")", "\\)"),
                        pmid=single_bib["pmid"],
                    )
                )

            # Write out the .bib file for this folder alongside the README.
            with (output_dir / folder_name / value / ".library.bib").open(
                "w+"
            ) as out_file:
                sub_bib_data = bibx.bibdatabase.BibDatabase()
                sub_bib_data.entries = bibs
                bibx.dump(sub_bib_data, out_file)

        readme_content = README_TEMPLATE.format(readme_lines="\n".join(readme_lines))
        with (output_dir / folder_name / "README.md").open("w+") as out_file:
            out_file.write(readme_content)


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
    parser.add_argument(
        "--pmid_col",
        type=str,
        default="PMID",
        help="The name of the column with Pubmed IDs in the filter_csv file.",
    )

    args = parser.parse_args()

    main(
        bib_file=args.bib_file,
        csv_structure=args.csv_structure,
        output_dir=args.out_dir,
        pmid_col=args.pmid_col,
    )
