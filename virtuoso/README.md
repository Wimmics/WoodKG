# What this folder contains

Various script to run a Docker container for Virtuoso and load RDF files.

### Run Virtuoso 

Script `run_virtuoso.sh`starts a Docker container for Virtuoso and mounts the current folder into the container so that Virtuoso will get access to the RDF files to be loaded.

👉 The current folder (where you run this script) must contain the `output` and `dataset` folders, that are at the root of this repository.

⚠️ Variable `$VIRTUOSO_DBA_PWD` must be set in the environment.

### Load RDF files into Virtuoso 

Script `run_import_woodkg.sh`connects to the running Virtuoso Docker container and executes `import_woodkg.isql` to load the files from the `output` and `dataset` folders.

Named graphs:
  - `http://ns.inria.fr/iawa/graph`: contains the IAWA thesaurus (file `iawa_thesaurus.ttl`)
  - `http://ns.inria.fr/wvcp/graph`: contains the WCVP taxonomy (files `wcvp_taxonomy_*.ttl`)
  - `http://ns.inria.fr/woodkg/graph/cepam_observations`: contains the CEPAM observations (file `observations_cepam.ttl`)
  - `http://ns.inria.fr/woodkg/graph/insidewood_observations`: contains the InsideWood observations (file `observations_insidewood.ttl`)


### Usage

```bash
export VIRTUOSO_DBA_PWD=yourpassword
cd WoodKG/virtuoso
./run_virtuoso.sh
./run_import_woodkg.sh
```
