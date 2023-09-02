# ICT::bib

<p align="center">
    <img src="./code/logo-small.png" width = 250>
</p>

This repository attempts to collect the current works regarding the Transportome, defined as the collection of all proteins present in the cell membrane surface that allow the passage of molecules through the membrane itself.

If you use this repository for your research, please cite:

> Coming soon!

<!--FactsTopAnchor-->
## Main Facts

| Category | Entries |
| -------- |:-------:|
| Transportome Research Articles | 56 |
| Transportome Reviews: Cancer | 40 |
| Transportome Reviews: Non-cancer  | 43 |
|           |              |
| **Total** | **139** |

<!--FactsBottomAnchor-->

## Library Structure

The library (accessible in `\Library\`) is divided into two different *sections*:
- The `Reviews` section collects all reviews regarding the transportome;
  - The `Cancer` subsection collects all reviews regarding the transportome in cancer;
  - The `Non Cancer` section collects all other reviews;
- The `Research Articles` section collects all research articles investigating the Trasportome or a subsection of it.

We manually describe each article in the library with the following information, in addition to the standard bibliographical information:
- **Macro-area**: The main scientific area the paper covers (e.g. "Breast Cancer", "Cell Motility", "Plants", etc...);
- **Topic**: The specific topic the paper covers (e.g. "Evolution", "Intestinal Inflammation", etc...);
- **Target**: The specific portion of the Transportome the paper investigates (e.g. "ICTs", "ion channels", etc...);

Inside each section, the library is organized in four different *categorizations*, one for each of the above-mentioned manual descriptions, plus by year of publication.

Inside each categorization folder, there is a `README.md` file with an index od all papers on that section, sorted by the specific categorization criteria.

By navigating into a subsection (e.g. `/Library/Reviews/Cancer/by year/2022/`) you will find one file per publication, with information such as DOI, Journal of publication, abstract and more.
Each subsection also contains one `.library.bib` file with the bibliographical information of all the papers in that subsection in `.bib` format, for ease of inclusion in bibliography managers.

## Contributing
We welcome and encourage all contributions! If you find an error, or wish to contribute your own article or an article you find to the library, please [open an issue](https://github.com/CMA-Lab/ICT.bib/issues/new/choose).

If you want to contribute to the repository's code, please take a look at the [CONTRIBUTING.md](https://github.com/CMA-Lab/ICT.bib/blob/main/CONTRIBUTING.md) file.
