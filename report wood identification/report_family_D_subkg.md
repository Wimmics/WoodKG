# File report of identification taxa with inside wood protocol

Request used to retrieve samples :

```sparql
    SELECT DISTINCT ?family_name ?mismatch ?origin WHERE {
        ?classes txrfp:hasReferenceName ?taxon;
            rdfs:subClassOf/rdfs:subClassOf ?family.
        ?family rdfs:label ?family_name.

        { select ?sample ?label ?taxon ((?origin - COUNT(?feature)) as ?mismatch) ?origin where {
            	{SELECT ?feature WHERE {<sample> pl_tax:hasObservation [sosa:hasResult [rdf:value ?feature]].} }
            	{SELECT (COUNT(?feature) as ?origin) WHERE {<sample> pl_tax:hasObservation [sosa:hasResult [rdf:value ?feature]].} }
                ?sample pl_tax:hasObservation [ sosa:hasResult [ rdf:value ?feature]];
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
- 1 row(s): precision 0.5957446808510638
- 2 row(s): precision 0.7659574468085106
- 3 row(s): precision 0.8085106382978723
- 4 row(s): precision 0.8297872340425532
- 5 row(s): precision 0.851063829787234
- 6 row(s): precision 0.8723404255319149
- 7 row(s): precision 0.8936170212765957
- 8 row(s): precision 0.8936170212765957
- 9 row(s): precision 0.9148936170212766
- 10 row(s): precision 0.9361702127659575
- 11 row(s): precision 0.9574468085106383
- 12 row(s): precision 0.9787234042553191
- 13 row(s): precision 0.9787234042553191
- 14 row(s): precision 0.9787234042553191
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
|1|0.0638|0.0638|0.2444|
|2|0.1277|0.1277|0.3337|
|3|0.2128|0.2340|0.4234|
|4|0.3191|0.4468|0.6461|
|5|0.4894|0.8723|1.0235|
|6|0.5745|1.3191|1.7395|
|7|0.7021|2.2128|2.7206|
|8|0.7872|3.3617|3.6868|
|9|0.8085|4.8298|4.5724|
|10|0.8511|6.6383|5.5214|
|11|0.8723|8.5745|6.0836|
|12|0.9149|10.5957|6.4136|
|13|0.9149|12.2766|6.2150|
|14|0.9149|14.1489|5.8345|
|15|0.9574|15.7021|5.6112|
|16|0.9574|16.8085|5.1844|
|17|0.9574|17.7872|4.3366|
|18|0.9574|18.4468|3.6426|
|19|0.9574|18.7872|3.4017|
|20|0.9574|19.0426|3.0733|
|21|0.9787|19.3404|2.5539|
|22|0.9787|19.4681|2.3416|
|23|1.0000|19.6170|1.7449|
|24|1.0000|19.7872|1.0092|
|25|1.0000|19.8936|0.5151|
|26|1.0000|19.9787|0.1443|
|27|1.0000|19.9787|0.1443|
|28|1.0000|20.0000|0.0000|
|29|1.0000|20.0000|0.0000|
|30|1.0000|20.0000|0.0000|
|31|1.0000|20.0000|0.0000|
|32|1.0000|20.0000|0.0000|
|33|1.0000|20.0000|0.0000|
|34|1.0000|20.0000|0.0000|
|35|1.0000|20.0000|0.0000|
|36|1.0000|20.0000|0.0000|
|37|1.0000|20.0000|0.0000|
|38|1.0000|20.0000|0.0000|
|39|1.0000|20.0000|0.0000|
|40|1.0000|20.0000|0.0000|
|41|1.0000|20.0000|0.0000|
|42|1.0000|20.0000|0.0000|
|43|1.0000|20.0000|0.0000|
|44|1.0000|20.0000|0.0000|
|45|1.0000|20.0000|0.0000|
|46|1.0000|20.0000|0.0000|
|47|1.0000|20.0000|0.0000|
|48|1.0000|20.0000|0.0000|
|49|1.0000|20.0000|0.0000|

## Precision at n first mismatch: (note: *it can be 0 mismatch*)
- 1 first mismatch: precision 0.6383
- 2 first mismatch: precision 0.7447
- 3 first mismatch: precision 0.8511
- 4 first mismatch: precision 0.9149
- 5 first mismatch: precision 0.9574
- 6 first mismatch: precision 0.9574
- 7 first mismatch: precision 0.9574
- 8 first mismatch: precision 0.9787
- 9 first mismatch: precision 0.9787
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

## Precision at n first mismatch with limited result number: (note: *it can be 0 mismatch*)
| N-first mismatch/Number of line | 1|3|5|7|9|10|13|15|17|20 | 
|--- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---  | 
| 1 | 0.5957|0.6383|0.6383|0.6383|0.6383|0.6383|0.6383|0.6383|0.6383|0.6383 |
| 2 | 0.5957|0.7447|0.7447|0.7447|0.7447|0.7447|0.7447|0.7447|0.7447|0.7447 |
| 3 | 0.5957|0.7872|0.8085|0.8298|0.8511|0.8511|0.8511|0.8511|0.8511|0.8511 |
| 4 | 0.5957|0.8085|0.8511|0.8936|0.9149|0.9149|0.9149|0.9149|0.9149|0.9149 |
| 5 | 0.5957|0.8085|0.8511|0.8936|0.9149|0.9149|0.9362|0.9574|0.9574|0.9574 |
| 6 | 0.5957|0.8085|0.8511|0.8936|0.9149|0.9149|0.9362|0.9574|0.9574|0.9574 |
| 7 | 0.5957|0.8085|0.8511|0.8936|0.9149|0.9149|0.9362|0.9574|0.9574|0.9574 |
| 8 | 0.5957|0.8085|0.8511|0.8936|0.9149|0.9362|0.9574|0.9787|0.9787|0.9787 |
| 9 | 0.5957|0.8085|0.8511|0.8936|0.9149|0.9362|0.9574|0.9787|0.9787|0.9787 |
| 10 | 0.5957|0.8085|0.8511|0.8936|0.9149|0.9362|0.9787|1.0000|1.0000|1.0000 |
| 11 | 0.5957|0.8085|0.8511|0.8936|0.9149|0.9362|0.9787|1.0000|1.0000|1.0000 |
| 12 | 0.5957|0.8085|0.8511|0.8936|0.9149|0.9362|0.9787|1.0000|1.0000|1.0000 |
| 13 | 0.5957|0.8085|0.8511|0.8936|0.9149|0.9362|0.9787|1.0000|1.0000|1.0000 |
| 14 | 0.5957|0.8085|0.8511|0.8936|0.9149|0.9362|0.9787|1.0000|1.0000|1.0000 |
| 15 | 0.5957|0.8085|0.8511|0.8936|0.9149|0.9362|0.9787|1.0000|1.0000|1.0000 |
| 16 | 0.5957|0.8085|0.8511|0.8936|0.9149|0.9362|0.9787|1.0000|1.0000|1.0000 |
| 17 | 0.5957|0.8085|0.8511|0.8936|0.9149|0.9362|0.9787|1.0000|1.0000|1.0000 |
| 18 | 0.5957|0.8085|0.8511|0.8936|0.9149|0.9362|0.9787|1.0000|1.0000|1.0000 |
| 19 | 0.5957|0.8085|0.8511|0.8936|0.9149|0.9362|0.9787|1.0000|1.0000|1.0000 |
| 20 | 0.5957|0.8085|0.8511|0.8936|0.9149|0.9362|0.9787|1.0000|1.0000|1.0000 |
| 21 | 0.5957|0.8085|0.8511|0.8936|0.9149|0.9362|0.9787|1.0000|1.0000|1.0000 |
| 22 | 0.5957|0.8085|0.8511|0.8936|0.9149|0.9362|0.9787|1.0000|1.0000|1.0000 |
| 23 | 0.5957|0.8085|0.8511|0.8936|0.9149|0.9362|0.9787|1.0000|1.0000|1.0000 |
| 24 | 0.5957|0.8085|0.8511|0.8936|0.9149|0.9362|0.9787|1.0000|1.0000|1.0000 |
| 25 | 0.5957|0.8085|0.8511|0.8936|0.9149|0.9362|0.9787|1.0000|1.0000|1.0000 |
| 26 | 0.5957|0.8085|0.8511|0.8936|0.9149|0.9362|0.9787|1.0000|1.0000|1.0000 |
| 27 | 0.5957|0.8085|0.8511|0.8936|0.9149|0.9362|0.9787|1.0000|1.0000|1.0000 |
| 28 | 0.5957|0.8085|0.8511|0.8936|0.9149|0.9362|0.9787|1.0000|1.0000|1.0000 |
| 29 | 0.5957|0.8085|0.8511|0.8936|0.9149|0.9362|0.9787|1.0000|1.0000|1.0000 |
| 30 | 0.5957|0.8085|0.8511|0.8936|0.9149|0.9362|0.9787|1.0000|1.0000|1.0000 |
| 31 | 0.5957|0.8085|0.8511|0.8936|0.9149|0.9362|0.9787|1.0000|1.0000|1.0000 |
| 32 | 0.5957|0.8085|0.8511|0.8936|0.9149|0.9362|0.9787|1.0000|1.0000|1.0000 |
| 33 |  |
| 34 |  |
