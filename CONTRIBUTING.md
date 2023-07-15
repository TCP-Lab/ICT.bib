# Contributing to the repository's code

The libray is not manually generated. A python script generates it automatically. The code for the library is in the `/code` folder.

The library is generated from two files per section:
- One `.bib` files with the bibiliographic information of papers to include, each with a `pmid` field with the PMID for the publication.
- One `.csv` table with the information with derived metadata like the paper=s scope and the paper's target. This file needs to have specific headers. Please take a look at the `Cancer.csv` and `NonCancer.csv` files for examples.

More information on the generative algorithm is in the source code itself.

## Generating the library
- Install Python;
- Clone the repository locally;
- Set your working directory in `./code`;
- Create a Python virtual environment and activate it (`python -m venv env && source ./env/bin/activate`).
- Install required dependencies: `pip install -r requirements.txt`
- Delete the contents of the `Library` folder (`rm -rf ../Library/*`);
- Run `regen_lib.py` to regenerate the library. The `regen_all` `zsh` script deletes the library and runs these commands for you. You can inspect it to see how it works.
