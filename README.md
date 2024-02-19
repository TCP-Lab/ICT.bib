# ICT::bib

<p align="center">
    <img src="./code/logo-small.png" width = 250>
</p>

This repository attempts to trace all the published scientific works regarding
the _transportome_, defined as the collection of all the membrane proteins
responsible for the translocation of any kind of solutes across the lipid
bilayer.

If you use this repository for your research, please cite
[our paper](https://pubmed.ncbi.nlm.nih.gov/37668550/):

> Federico Alessandro Ruffinatti, Giorgia Scarpellino, Giorgia Chinigò,
> Luca Visentin, Luca Munaron.
> **The Emerging Concept of Transportome: State of the Art**
> _Review Physiology (Bethesda)_. 2023 Nov 1;38(6):0.
> PMID: 37668550; DOI: 10.1152/physiol.00010.2023

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

The library (accessible in `/Library/`) is divided into two different
*sections*:
- the `Reviews` section collects all reviews about the transportome;
  - the `Cancer` subsection collects all reviews regarding the transportome in
    cancer;
  - the `Non Cancer` section collects all other reviews;
- the `Research Articles` section collects all research articles investigating
  the transportome--or, at least, an entire molecular class of transporters
  (e.g., all SLCs, all ion channels, _etc._).

We manually annotate each article in the library with the following information,
in addition to the standard bibliographical information:
- **Macro-area**: the main scientific area the paper covers (e.g., "Breast
  Cancer", "Cell Motility", "Plants", _etc._);
- **Topic**: the specific topic the paper covers (e.g. "Evolution", "Intestinal
  Inflammation", _etc._);
- **Transportomic Target**: the specific portion (or _layer_) of the
  transportome investigated in the paper, chosen among the following entries:
   - `Ion Channels`
   - `Aquaporins`
   - `Pores` (= `Ion Channels` AND `Aquaporins`)
   - `SLCs` (= solute carriers)
   - `Pumps` (= ATPase pumps)
   - `ABCs` (= ATP-binding cassette transporters)
   - `Transporters` (= `SLCs` AND `Pumps` AND `ABCs`)
   - `ICTs` (= the whole transportome)

Inside each section, the library is organized in four different
*categorizations*, one for each of the above-mentioned manual annotations, plus
by year of publication.

Inside each categorization folder, there is a `README.md` file with an index of
all papers on that section, sorted by the specific categorization criterion.

By navigating into a subsection (e.g., `/Library/Reviews/Cancer/by year/2022/`)
you will find one file per publication, with information such as DOI, Journal of
publication, abstract, and more.
Each subsection also contains one `.library.bib` file with the bibliographical
information of all the papers in that subsection in `.bib` format, for ease of
inclusion in bibliography managers.

## Contributing
We welcome and encourage all contributions! If you find an error, or wish to
contribute your own article or an article you find to the library, please
[open an issue](https://github.com/CMA-Lab/ICT.bib/issues/new/choose).

If you want to contribute to the repository's code, please take a look at the
[CONTRIBUTING.md](https://github.com/CMA-Lab/ICT.bib/blob/main/CONTRIBUTING.md)
file.
