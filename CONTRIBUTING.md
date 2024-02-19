# Contributing to the repository's code

The libray is not manually generated. A __python__ script generates it
automatically. The code for the library is in the `/code` folder.

The library is generated from two files per section:
- a `.bib` file with the bibliographic information about papers to include, each
	entry featuring a `pmid` field with the PMID of the publication.
- a `.csv` table containing derived metadata like the paper's scope and
	transportomic target. This file needs to have specific headers. Please take
	a look at the `review_cancer.csv` and `articles.csv` files for examples.

More information on the generative algorithm can be found in the source code
itself.

## Generating the library
- Install Python;
- Clone the repository locally;
- Set your working directory in `./code`;
- Create a Python virtual environment and activate it
	(`python -m venv env && source ./env/bin/activate`).
- Install the required dependencies: `pip install -r requirements.txt`
- Delete the contents of the `Library` folder (`rm -rf ../Library/*`);
- Run `regen_lib.py` to regenerate the library.

> [!NOTE]
> The `regen_all` `bash` script deletes the library and runs the last two
> commands for you. You can inspect it to see how it works. In addition, the
> scripts edits the `README.md` file updating the
> [__Main Facts__](https://github.com/TCP-Lab/ICT.bib?tab=readme-ov-file#main-facts)
> table with the actual number of __ICT::bib__ entries. For these reasons, this
> should be the preferred way to go.
