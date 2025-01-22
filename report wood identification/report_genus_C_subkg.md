# File report of identification taxa with inside wood protocol

Request used to retrieve samples :

```sparql
    SELECT DISTINCT ?family_name ?mismatch ?origin WHERE {
        ?classes txrfp:hasReferenceName ?taxon;
            rdfs:subClassOf/rdfs:subClassOf ?family.
        ?family rdfs:label ?family_name.

        { select ?sample ?label ?taxon ((?origin - COUNT(?feature)) as ?mismatch) ?origin where {
            	{SELECT ?feature WHERE {<sample> pl_tax:hasObservation [sosa:hasResult [rdf:value ?feature; pl_tax:presence ?presence]].} }
            	{SELECT (COUNT(?feature) as ?origin) WHERE {<sample> pl_tax:hasObservation [sosa:hasResult [rdf:value ?feature; pl_tax:presence ?presence]].} }
                ?sample pl_tax:hasObservation [ sosa:hasResult [ rdf:value ?feature; pl_tax:presence ?presence]];
                	pl_tax:identifiedTaxon ?taxon.
                ?taxon skos:prefLabel ?label.
                FILTER (?sample != <sample>)
            }
            GROUP BY ?sample ?origin ?label ?taxon
            ORDER BY ?mismatch        
        }
    }
    ORDER BY ?mismatch
    ```

## Precision at n first result: 
- 1 row(s): precision 0.75
- 2 row(s): precision 0.875
- 3 row(s): precision 0.9375
- 4 row(s): precision 1.0
- 5 row(s): precision 1.0
- 6 row(s): precision 1.0
- 7 row(s): precision 1.0
- 8 row(s): precision 1.0
- 9 row(s): precision 1.0
- 10 row(s): precision 1.0
- 11 row(s): precision 1.0
- 12 row(s): precision 1.0
- 13 row(s): precision 1.0
- 14 row(s): precision 1.0
- 15 row(s): precision 1.0
- 16 row(s): precision 1.0
- 17 row(s): precision 1.0
- 18 row(s): precision 1.0
- 19 row(s): precision 1.0
- 20 row(s): precision 1.0
- 21 row(s): precision 1.0
- 22 row(s): precision 1.0
- 23 row(s): precision 1.0
- 24 row(s): precision 1.0
- 25 row(s): precision 1.0
- 26 row(s): precision 1.0
- 27 row(s): precision 1.0
- 28 row(s): precision 1.0
- 29 row(s): precision 1.0
- 30 row(s): precision 1.0
- 31 row(s): precision 1.0
- 32 row(s): precision 1.0
- 33 row(s): precision 1.0
- 34 row(s): precision 1.0
- 35 row(s): precision 1.0
- 36 row(s): precision 1.0
- 37 row(s): precision 1.0
- 38 row(s): precision 1.0
- 39 row(s): precision 1.0
- 40 row(s): precision 1.0
- 41 row(s): precision 1.0
- 42 row(s): precision 1.0
- 43 row(s): precision 1.0
- 44 row(s): precision 1.0
- 45 row(s): precision 1.0
- 46 row(s): precision 1.0
- 47 row(s): precision 1.0
- 48 row(s): precision 1.0
- 49 row(s): precision 1.0

## Precision at n mismatch: 
| Mismatch | Precision | Average Nb of Row | Standard deviation |
|---|---|---|---|
|0|0.0000|0.0000|0.0000|
|1|0.1250|0.1250|0.3307|
|2|0.1875|0.2500|0.5590|
|3|0.3750|0.5000|0.7906|
|4|0.5000|0.8125|0.8817|
|5|0.7500|1.3750|1.2183|
|6|0.7500|1.6250|1.4524|
|7|0.8125|2.0625|1.7489|
|8|0.8750|2.7500|2.1065|
|9|0.8750|3.4375|2.3971|
|10|0.9375|4.2500|2.7042|
|11|1.0000|4.8750|3.0797|
|12|1.0000|5.6250|3.1795|
|13|1.0000|6.5000|3.4460|
|14|1.0000|7.3750|3.6207|
|15|1.0000|7.8750|3.6550|
|16|1.0000|8.3750|3.5685|
|17|1.0000|8.6875|3.3860|
|18|1.0000|9.1250|2.9765|
|19|1.0000|9.6875|2.2836|
|20|1.0000|9.8125|2.0068|
|21|1.0000|10.0625|1.6759|
|22|1.0000|10.3750|1.1659|
|23|1.0000|10.5625|0.8638|
|24|1.0000|10.7500|0.7500|
|25|1.0000|11.0000|0.0000|
|26|1.0000|11.0000|0.0000|
|27|1.0000|11.0000|0.0000|
|28|1.0000|11.0000|0.0000|
|29|1.0000|11.0000|0.0000|
|30|1.0000|11.0000|0.0000|
|31|1.0000|11.0000|0.0000|
|32|1.0000|11.0000|0.0000|
|33|1.0000|11.0000|0.0000|
|34|1.0000|11.0000|0.0000|
|35|1.0000|11.0000|0.0000|
|36|1.0000|11.0000|0.0000|
|37|1.0000|11.0000|0.0000|
|38|1.0000|11.0000|0.0000|
|39|1.0000|11.0000|0.0000|
|40|1.0000|11.0000|0.0000|
|41|1.0000|11.0000|0.0000|
|42|1.0000|11.0000|0.0000|
|43|1.0000|11.0000|0.0000|
|44|1.0000|11.0000|0.0000|
|45|1.0000|11.0000|0.0000|
|46|1.0000|11.0000|0.0000|
|47|1.0000|11.0000|0.0000|
|48|1.0000|11.0000|0.0000|
|49|1.0000|11.0000|0.0000|

## Precision at n first mismatch: (note: *it can be 0 mismatch*)
- 1 first mismatch: precision 0.8750
- 2 first mismatch: precision 0.9375
- 3 first mismatch: precision 1.0000
- 4 first mismatch: precision 1.0000
- 5 first mismatch: precision 1.0000
- 6 first mismatch: precision 1.0000
- 7 first mismatch: precision 1.0000
- 8 first mismatch: precision 1.0000
- 9 first mismatch: precision 1.0000
- 10 first mismatch: precision 1.0000
- 11 first mismatch: precision 1.0000
- 12 first mismatch: precision 1.0000
- 13 first mismatch: precision 1.0000
- 14 first mismatch: precision 1.0000
- 15 first mismatch: precision 1.0000
- 16 first mismatch: precision 1.0000
- 17 first mismatch: precision 1.0000
- 18 first mismatch: precision 1.0000
- 19 first mismatch: precision 1.0000
- 20 first mismatch: precision 1.0000
- 21 first mismatch: precision 1.0000
- 22 first mismatch: precision 1.0000
- 23 first mismatch: precision 1.0000
- 24 first mismatch: precision 1.0000
- 25 first mismatch: precision 1.0000
- 26 first mismatch: precision 1.0000
- 27 first mismatch: precision 1.0000
- 28 first mismatch: precision 1.0000
- 29 first mismatch: precision 1.0000
- 30 first mismatch: precision 1.0000
- 31 first mismatch: precision 1.0000
- 32 first mismatch: precision 1.0000
- 33 first mismatch: precision 1.0000
- 34 first mismatch: precision 1.0000
- 35 first mismatch: precision 1.0000
- 36 first mismatch: precision 1.0000
- 37 first mismatch: precision 1.0000
- 38 first mismatch: precision 1.0000
- 39 first mismatch: precision 1.0000

## Precision at n first mismatch with limited result number: (note: *it can be 0 mismatch*)
| N-first mismatch/Number of line | 1|3|5|7|9|10|13|15|17|20 | 
|--- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---  | 
| 1 | 0.7500|0.8750|0.8750|0.8750|0.8750|0.8750|0.8750|0.8750|0.8750|0.8750 |
| 2 | 0.7500|0.8750|0.9375|0.9375|0.9375|0.9375|0.9375|0.9375|0.9375|0.9375 |
| 3 | 0.7500|0.9375|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000 |
| 4 | 0.7500|0.9375|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000 |
| 5 | 0.7500|0.9375|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000 |
| 6 | 0.7500|0.9375|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000 |
| 7 | 0.7500|0.9375|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000 |
| 8 | 0.7500|0.9375|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000 |
| 9 | 0.7500|0.9375|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000 |
| 10 | 0.7500|0.9375|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000 |
| 11 | 0.7500|0.9375|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000 |
| 12 | 0.7500|0.9375|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000 |
| 13 | 0.7500|0.9375|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000 |
| 14 | 0.7500|0.9375|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000 |
| 15 | 0.7500|0.9375|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000 |
| 16 | 0.7500|0.9375|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000 |
| 17 | 0.7500|0.9375|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000 |
| 18 | 0.7500|0.9375|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000 |
| 19 | 0.7500|0.9375|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000 |
| 20 | 0.7500|0.9375|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000 |
| 21 | 0.7500|0.9375|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000 |
| 22 | 0.7500|0.9375|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000 |
| 23 | 0.7500|0.9375|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000 |
| 24 | 0.7500|0.9375|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000 |
| 25 | 0.7500|0.9375|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000 |
| 26 | 0.7500|0.9375|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000 |
| 27 | 0.7500|0.9375|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000 |
| 28 | 0.7500|0.9375|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000 |
| 29 | 0.7500|0.9375|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000 |
| 30 | 0.7500|0.9375|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000 |
| 31 | 0.7500|0.9375|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000 |
| 32 | 0.7500|0.9375|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000 |
| 33 | 0.7500|0.9375|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000 |
| 34 | 0.7500|0.9375|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000 |
