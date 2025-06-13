# 🌳 WoodKG – African Wood Charcoal Knowledge Graph

**WoodKG** is a knowledge graph dedicated to the study of African charcoal wood. This repository contains:
- the graph construction methodology,
- wood identification tools,
- usage examples.

The graph merges botanical information from three main sources:
1. **[Plants of the World Online (POWO)](http://www.plantsoftheworldonline.org/)** – taxonomy and geolocation.
2. **[InsideWood](http://insidewood.lib.ncsu.edu/)** – wood anatomical descriptions using IAWA features.
3. **Southern African charcoal wood descriptions** – also based on IAWA features.

---

## 📦 Requirements

All implementation is contained within a **Jupyter Notebook**.

---

## 🚀 Usage

### 🔧 Wood description extraction

Notebook: `burnwood_extract.ipynb`

This notebook:
- extracts family, genus, and taxa from unstructured text (CSV),
- aligns data with POWO accepted taxonomy,
- converts IAWA symbols into numerical values:
  - `0`: **lack of information**, which could indicate actual absence of the feature *or* omission by the observer,
  - `1`: doubtful presence,
  - `2`: non-systematic presence,
  - `3`: confirmed presence,
- generates two CSV files:
  - one for RDF export,
  - another for machine learning purposes.

---

### 🧠 Wood Identification

Script: `identlib.py`

Functionality:
- Takes a CSV of wood descriptions.
- Returns closest species based on IAWA features.
- Ranked by number of mismatches.
- Focused on four African regions to match the initial dataset.

---

### 📊 Knowledge Graph Query Examples

Notebook: `QC_sparql.ipynb`

Contains real use cases and their translation into SPARQL queries.

---

## 🔍 Identification Example

Example: “Type 7” sample from the SACHA database.

| Family        | Taxon                               | Mismatches |
|---------------|-------------------------------------|------------|
| Olea          | Olea europaea subsp. cuspidata      | 7          |
| Olea          | Olea capensis subsp. enervis        | 8          |
| Oleaceae      | Olea schliebenii                     | 8          |
| Asteraceae    | Brachylaena huillensis              | 9          |
| Loganiaceae   | Strychnos mitis                     | 9          |
| ...           | ...                                 | ...        |

---

## 🙏 Acknowledgements

### InsideWood
- **Website**: http://insidewood.lib.ncsu.edu/search  
- Wheeler, E.A. (2011). *InsideWood – A Web Resource For Hardwood Identification*. [PDF](https://insidewood.lib.ncsu.edu/files/insidewood/Wheeler.2011.InsideWood.pdf)  
- Wheeler, E.A., Gasson, P.E., & Baas, P. (2020). *Using The InsideWood Web Site: Potentials And Pitfalls*. [PDF](https://insidewood.lib.ncsu.edu/files/Wheeler.Gasson.Baas.2020.IW.pdf)

### POWO – Plants of the World Online
- POWO (2023). *Royal Botanic Gardens, Kew*.  
  http://www.plantsoftheworldonline.org/  
  Accessed on September 4th, 2023.
