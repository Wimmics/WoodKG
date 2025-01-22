# Requêtes SPARQL pour questions de compétences

## Préfixes pour les requêtes

```turtle
prefix rdf:    <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
prefix owl:    <http://www.w3.org/2002/07/owl#> .
prefix iawa: <https://www.iawa-website.org/core#> .
prefix skos: <http://www.w3.org/2004/02/skos/core#>.
prefix pl_tax: <http://www.plant-taxonomy-kg.com/core#>.
prefix sosa: <http://www.w3.org/ns/sosa/> .
prefix wcvp: <http://www.wcvp-core.com/class#>.
prefix txrfp: <http://taxref.mnhn.fr/lod/property/>.
```

## Template des URIs du graphe

|       Type       |                             URI                              |
| :--------------: | :----------------------------------------------------------: |
|    WCVP-Taxon    |          http://www.wcvp-core.com/taxon/{id_taxon}           |
|    WCVP-label    |           http://www.wcvp-core.com/name/{id_taxon}           |
| WCVP-geolocation |     http://www.wcvp-core.com/geoloc/{type}/{location_id}     |
|    IPNI-taxon    |                 https://ipni.org/n/{ipni_id}                 |
|    POWO-Taxon    |         https://powo.science.kew.org/taxon/{ipni_id}         |
|      Sample      |  https://www.wood-sample-observation.com/sample/{sample_id}  |
|   Observation    | https://www.wood-sample-observation.com/observation/{sample_id}\_{taxon_id}_{id_feature} |
|  IAWA-Features   |      https://www.iawa-website.org/features/{feature_id}      |
| IAWA-Collection  |     https://www.iawa-website.org/collection/{collection}     |

## 0. Tests des liens entre les ressources

```SPARQL
select ?label_taxon ?sample_name ?loc_name where {
  ?sample skos:prefLabel ?sample_name;
	pl_tax:identifiedTaxon ?label.
   
  ?taxon txrfp:hasReferenceName ?label;
         wcvp:location ?location;
         wcvp:location ?location2.

  ?label skos:prefLabel ?label_taxon.

  ?location rdfs:label "AFRICA".
  ?location2 rdfs:label ?loc_name.
  filter(?location != ?location2)
}


```

```SPARQL
select ?area ?area_name ?region ?region_name ?continent where {

  <http://www.wcvp-core.com/taxon/2469745> wcvp:location ?area.

  ?area a wcvp:Area;
	skos:broader ?region;
	rdfs:label ?area_name.
  ?region skos:broader ?continent;
	rdfs:label ?region_name.

  ?continent rdfs:label "AFRICA".
}

```



## 1.  Quels sont les individus observés se trouvant en Afrique ?

```SPARQL
select distinct ?sample_name ?taxon ?taxon_value ?label ?label_taxon ?loc_name where {
  ?sample skos:prefLabel ?sample_name;
	pl_tax:identifiedTaxon ?label.
   
  ?taxon txrfp:hasReferenceName ?label;
        rdfs:label ?taxon_value;
         wcvp:location ?location;
         wcvp:location ?location2.

  ?label skos:prefLabel ?label_taxon.

  ?location rdfs:label "AFRICA".
  ?location2 rdfs:label ?loc_name.
  filter(?location != ?location2)
}
```



## 2. Quels sont les taxons possibles pour cette séquence de caractères observables ?

```SPARQL
SELECT * WHERE {
    
}
```



## 3. Quels sont les observations disponibles pour le taxon (espèces, ou genre, ou famille) ?

```SPARQL
SELECT * WHERE {
    
}
```

