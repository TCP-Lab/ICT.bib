<style>
    .container {
    display: flex;
    align-items: center;
    justify-content: center
    }
</style>


<div class="container">
    <div class="text">
        <font size="+4"><b>ICT.bib</b></font>
    </div>
    <div class="image">
        <img src="./code/logo-small.png" width = 200>
    </div>
</div>


This repository attempts to collect the current reviews regarding the Transportome, defined as the collection of all proteins present in the cell membrane surface that allow the passage of molecules through the membrane itself.

If you use this repository for your research, please cite:

> Coming soon! (we hope)

## Library Structure

The library (accessible in `\Library\`) is divided into two different *sections*:
- The `Cancer` section collects all papers regarding cancer;
- The `Non Cancer` section collects all other papers;

Inside each section, the library is organized by three different *categorizations*:
- The `by scope` section aggregates papers by their scope, i.e. by the main scientific area they cover (e.g. "Cancer Therapy", "Cell Motility", etc...);
- The `by target` section aggregates papers by what portion of the Transportome they investigate (e.g. "ICTs", "ion channels", etc...).
- The `by year` section aggregates papers by the year they were published in.

Inside each categorization folder, there is a `README.md` file with an index od all papers on that section, sorted by the specific categorization criteria.

By navigating into a subsection (e.g. `/Library/Cancer/by year/2022/`) you will find one file per publication inside that subsection, with information such as DOI, Journal of publication, abstract and more. Each subsection also contains one `.library.bib` file with the bibliographical information of all the papers in that subsection in `.bib` format, for ease of inclusion in bibliography managers.

## Contributing
We welcome and encourage all contributions! If you find an error, or wish to contribute your own article or an article you find to the library, please [open an issue](https://github.com/CMA-Lab/ICT.bib/issues/new/choose).

If you want to contribute to the repository's code, please take a look at the [CONTRIBUTING.md](https://github.com/CMA-Lab/ICT.bib/blob/main/CONTRIBUTING.md) file.

