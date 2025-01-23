# Insert

```sparql
prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
prefix owl: <http://www.w3.org/2002/07/owl#>
prefix iawa:<https://www.iawa-website.org/core#>
prefix skos: <http://www.w3.org/2004/02/skos/core#>
prefix pl_tax: <http://www.plant-taxonomy-kg.com/core#>
prefix sosa: <http://www.w3.org/ns/sosa/>
prefix wcvp: <http://www.wcvp-core.com/class#>
prefix txrfp: <http://taxref.mnhn.fr/lod/property/>

insert {<https://www.wood-sample-observation.com/sample/TSW-1> pl_tax:hasObservation 

}
where {}

```



# Search

```sparql
prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
prefix owl: <http://www.w3.org/2002/07/owl#>
prefix iawa:<https://www.iawa-website.org/core#>
prefix skos: <http://www.w3.org/2004/02/skos/core#>
prefix pl_tax: <http://www.plant-taxonomy-kg.com/core#>
prefix sosa: <http://www.w3.org/ns/sosa/>
prefix wcvp: <http://www.wcvp-core.com/class#>
prefix txrfp: <http://taxref.mnhn.fr/lod/property/>
SELECT DISTINCT ?genus_name WHERE {
{SELECT DISTINCT ?sample ?family_name ?genus_name ?label ?mismatch ?origin WHERE {
    ?classes txrfp:hasReferenceName ?taxon;
        rdfs:subClassOf ?genus.
    ?genus rdfs:label ?genus_name;
	rdfs:subClassOf ?family.
    ?family rdfs:label ?family_name.

    { select ?sample ?label ?taxon ((?origin - COUNT(?feature)) as ?mismatch) ?origin where {
        	{SELECT ?feature WHERE {<https://www.wood-sample-observation.com/sample/TSW-1> pl_tax:hasObservation [sosa:hasResult [rdf:value ?feature]].} }
        	{SELECT (COUNT(?feature) as ?origin) WHERE {<https://www.wood-sample-observation.com/sample/TSW-1> pl_tax:hasObservation [sosa:hasResult [rdf:value ?feature]].} }
            ?sample pl_tax:hasObservation [ sosa:hasResult [ rdf:value ?feature]];
            	pl_tax:identifiedTaxon ?taxon.
            ?taxon skos:prefLabel ?label.
            FILTER (?sample != <https://www.wood-sample-observation.com/sample/TSW-1>)
        }
        GROUP BY ?sample ?origin ?label ?taxon
        ORDER BY ?mismatch        
    }
}
ORDER BY ?mismatch ?family_name ?label}}
```



# DELETE

```sparql
prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
prefix owl: <http://www.w3.org/2002/07/owl#>
prefix iawa:<https://www.iawa-website.org/core#>
prefix skos: <http://www.w3.org/2004/02/skos/core#>
prefix pl_tax: <http://www.plant-taxonomy-kg.com/core#>
prefix sosa: <http://www.w3.org/ns/sosa/>
prefix wcvp: <http://www.wcvp-core.com/class#>
prefix txrfp: <http://taxref.mnhn.fr/lod/property/>

delete where {
  <https://www.wood-sample-observation.com/sample/TSW-1> pl_tax:hasObservation ?obs
}

```



# OLD precision at n row

```python
for k in range(1, 50):
    good_sample = False
    
    if not good_sample:
        precision_at_k.append((k, 0))

global_prec_at_n.append(precision_at_k)
```

