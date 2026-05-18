# WCVP Knowledge Graph Documentation

This document describes a representation of WCVP (World Checklist of Vascular Plants) as a KG in the Resource Description Format (RDF).

To account for the semantics of represented resources, we model nomenclatural information as a thesaurus wherein each concept denotes a scientific name along with its taxonomic rank, status, authority etc. 
By contrast, taxonomic information is modeled as an ontology wherein each class denotes a taxon linked to its accepted name and synonyms thereof.

The modeling relies primarily on the Darwin Core (DwC) RDF vocabulary, making it fully aligned with the DwC-A distribution of WCVP.
However since most DwC (datatype) properties have literals as an object, it is complemented with (object) properties and resources for taxonomic ranks and statuses.

## Used prefixes

```turtle
@prefix dwc:     <http://rs.tdwg.org/dwc/terms/> .
@prefix owl:     <http://www.w3.org/2002/07/owl#> .
@prefix rdfs:    <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos:    <http://www.w3.org/2004/02/skos/core#> .
@prefix schema:  <http://schema.org/> .
@prefix txrfp:   <http://taxref.mnhn.fr/lod/property/> .
```

## Taxon

A taxon has an accepted scientific name and associated synonyms. Taxa are created only for accepted names and serve as the primary reference point in the knowledge graph.

### Description

- **URI Pattern:** `http://ns.inria.fr/wcvp/taxon/{taxonid}`
- **Type:** `owl:Class`
- **Key Properties:**
  - `rdfs:label`: accepted name of the taxon
  - `rdfs:subClassOf`: parent taxon (for hierarchical relationships)
  - `dwc:taxonID`: unique identifier for the taxon
  - `dwc:taxonRank`: taxonomic rank as it is labeled in WCVP (e.g., Species, Genus, nothosubs., micromorph)
  - `txrfp:hasRank`: taxonomic rank as an IRI (from `dataset/taxrefld_static_defs_taxranks.ttl`) only for Forma, Genus, Species, SubForma, SubSpecies, SubVarietas, Varietas
  - `txrfp:hasReferenceName`: link to the accepted scientific name with the same taxon ID
  - `txrfp:hasSynonym`: link to one or more synonym scientific names

### Example

```turtle
<http://ns.inria.fr/wcvp/taxon/2772885>
    a       owl:Class ;
    rdfs:label "Discocalyx latepetiolata" ;
    rdfs:subClassOf <http://ns.inria.fr/wcvp/taxon/2772860> ;
    dwc:taxonID "2772885" ;
    dwc:taxonRank "Species" ;
    txrfp:hasRank <http://taxref.mnhn.fr/lod/taxrank/Species> ;
    txrfp:hasReferenceName <http://ns.inria.fr/wcvp/name/2772885> ;
    txrfp:hasSynonym <http://ns.inria.fr/wcvp/name/2494499> , <http://ns.inria.fr/wcvp/name/2494514> .
```

In this example, taxon 2772885 has one reference name "Discocalyx latepetiolata" and two synonyms:
  - `<http://ns.inria.fr/wcvp/name/2494499>` — "Loheria sessilifolia Mez"
  - `<http://ns.inria.fr/wcvp/name/2494514>` — "Loheria latepetiolata Mez"

---

## Scientific Name

### Description:

- **URI Pattern:** `http://ns.inria.fr/wcvp/name/{taxonid}`
- **Type:** `skos:Concept`
- **Key Properties:**
  - `skos:prefLabel`: label combining name and authority
  - `skos:broader`: link to the parent name (when applicable)
  - `dwc:scientificName`: nomenclatural string (e.g., "Loheria sessilifolia")
  - `dwc:scientificNameAuthorship`: author citation (e.g., "Mez")
  - `dwc:scientificNameID`: unique identifier for this name
  - `dwc:taxonomicStatus`: status as it is labeled in WCVP: Accepted, Synonym, Illegitimate, Invalid, Misplaced, etc.
  - `txrfp:hasTaxonomicStatus`: IRI reference to the taxonomic status, build from the WCVP label (given in `data/wcvp_taxonomic_statuses.ttl`)
  - `dwc:taxonRank`: taxonomic rank as it is labeled in WCVP (e.g., Species, Genus, nothosubs., micromorph)
  - `txrfp:hasRank`: taxonomic rank as an IRI (given in `dataset/taxrefld_static_defs_taxranks.ttl`) only for Forma, Genus, Species, SubForma, SubSpecies, SubVarietas, Varietas
  - `dwc:namePublishedIn`: publication reference
  - `dwc:family`, `dwc:genus`, `dwc:specificEpithet`, `dwc:infraspecificEpithet`: taxonomic classification
  - `rdfs:seeAlso`: for names whose status is not Accepted or Synonym, link to the accepted name
  - `schema:mainEntityOfPage`: external reference (e.g., POWO link)

### Example 1: Synonym Name

```turtle
<http://ns.inria.fr/wcvp/name/2494499>
    a skos:Concept ;
    skos:prefLabel "Loheria sessilifolia Mez" ;
    dwc:scientificName "Loheria sessilifolia" ;
    dwc:scientificNameAuthorship "Mez" ;
    dwc:scientificNameID "2494499" ;
    dwc:namePublishedIn "Bot. Arch. 2: 210 (1922)" ;

    dwc:taxonomicStatus "Synonym" ;
    txrfp:hasTaxonomicStatus <http://ns.inria.fr/wcvp/taxonomicStatus/Synonym> ;

    dwc:taxonRank "Species" ;
    txrfp:hasRank <http://taxref.mnhn.fr/lod/taxrank/Species> ;

    dwc:family "Primulaceae" ;
    dwc:genus "Loheria" ;
    dwc:specificEpithet "sessilifolia" ;

    schema:mainEntityOfPage "https://powo.science.kew.org/taxon/urn:lsid:ipni.org:names:588724-1" .
```

In this example, the scientific name "Loheria sessilifolia" is marked as a `Synonym` of the accepted name in taxon 2772885.

### Example 2: Illegitimate Name with Related Accepted Name

```turtle
<http://ns.inria.fr/wcvp/name/350474>
    a skos:Concept ;
    skos:prefLabel "Thymus serpyllum var. alpestris Briq." ;
    dwc:family "Lamiaceae" ;
    dwc:genus "Thymus" ;
    dwc:specificEpithet "serpyllum" ;
    dwc:infraspecificEpithet "alpestris" ;

    dwc:scientificName "Thymus serpyllum var. alpestris" ;
    dwc:scientificNameAuthorship "Briq." ;
    dwc:scientificNameID "350474" ;
    dwc:namePublishedIn "Neue Denkschr. Allg. Schweiz. Ges. Gesammten Naturwiss. 34: 450 (1895)" ;

    dwc:taxonRank "Varietas" ;
    txrfp:hasRank <http://taxref.mnhn.fr/lod/taxrank/Varietas> ;

    dwc:taxonomicStatus "Illegitimate" ;
    txrfp:hasTaxonomicStatus <http://ns.inria.fr/wcvp/taxonomicStatus/Illegitimate> ;

    rdfs:seeAlso <http://ns.inria.fr/wcvp/name/205276> ;

    schema:mainEntityOfPage "https://powo.science.kew.org/taxon/urn:lsid:ipni.org:names:77293152-1" .
```

In this example, the scientific name has a taxonomic status of `Illegitimate`.
The `rdfs:seeAlso` property links to name `205276`, which is the accepted name it relates to
