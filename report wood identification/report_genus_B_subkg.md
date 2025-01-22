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
- 1 row(s): precision 0.7605633802816901
- 2 row(s): precision 0.8732394366197183
- 3 row(s): precision 0.9436619718309859
- 4 row(s): precision 0.9577464788732394
- 5 row(s): precision 0.9859154929577465
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
|0|0.0423|0.0423|0.2012|
|1|0.1690|0.2394|0.5163|
|2|0.3944|0.5634|0.7642|
|3|0.5211|0.8732|1.0997|
|4|0.6901|1.4789|1.7268|
|5|0.8169|2.1127|2.4238|
|6|0.8592|3.3239|3.6455|
|7|0.8873|4.8732|5.0293|
|8|0.9155|7.0423|6.6702|
|9|0.9437|9.7042|7.9300|
|10|0.9437|12.7183|8.9932|
|11|0.9577|16.3662|9.9282|
|12|0.9859|20.0141|10.2524|
|13|0.9859|23.0141|10.4686|
|14|0.9859|25.4366|10.0249|
|15|1.0000|27.7183|9.0960|
|16|1.0000|29.5352|8.1393|
|17|1.0000|30.7746|7.3699|
|18|1.0000|31.9859|6.1633|
|19|1.0000|32.9296|5.1712|
|20|1.0000|33.5634|4.1341|
|21|1.0000|34.0141|3.2174|
|22|1.0000|34.2676|2.6852|
|23|1.0000|34.5493|1.7506|
|24|1.0000|34.7183|1.3757|
|25|1.0000|34.8451|0.6848|
|26|1.0000|34.9437|0.3710|
|27|1.0000|34.9718|0.1655|
|28|1.0000|34.9859|0.1178|
|29|1.0000|35.0000|0.0000|
|30|1.0000|35.0000|0.0000|
|31|1.0000|35.0000|0.0000|
|32|1.0000|35.0000|0.0000|
|33|1.0000|35.0000|0.0000|
|34|1.0000|35.0000|0.0000|
|35|1.0000|35.0000|0.0000|
|36|1.0000|35.0000|0.0000|
|37|1.0000|35.0000|0.0000|
|38|1.0000|35.0000|0.0000|
|39|1.0000|35.0000|0.0000|
|40|1.0000|35.0000|0.0000|
|41|1.0000|35.0000|0.0000|
|42|1.0000|35.0000|0.0000|
|43|1.0000|35.0000|0.0000|
|44|1.0000|35.0000|0.0000|
|45|1.0000|35.0000|0.0000|
|46|1.0000|35.0000|0.0000|
|47|1.0000|35.0000|0.0000|
|48|1.0000|35.0000|0.0000|
|49|1.0000|35.0000|0.0000|

## Precision at n first mismatch: (note: *it can be 0 mismatch*)
- 1 first mismatch: precision 0.8310
- 2 first mismatch: precision 0.9437
- 3 first mismatch: precision 0.9718
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

## Precision at n first mismatch with limited result number: (note: *it can be 0 mismatch*)
| N-first mismatch/Number of line | 1|3|5|7|9|10|13|15|17|20 | 
|--- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---  | 
| 1 | 0.7606|0.8310|0.8310|0.8310|0.8310|0.8310|0.8310|0.8310|0.8310|0.8310 |
| 2 | 0.7606|0.9296|0.9437|0.9437|0.9437|0.9437|0.9437|0.9437|0.9437|0.9437 |
| 3 | 0.7606|0.9437|0.9577|0.9718|0.9718|0.9718|0.9718|0.9718|0.9718|0.9718 |
| 4 | 0.7606|0.9437|0.9859|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000 |
| 5 | 0.7606|0.9437|0.9859|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000 |
| 6 | 0.7606|0.9437|0.9859|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000 |
| 7 | 0.7606|0.9437|0.9859|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000 |
| 8 | 0.7606|0.9437|0.9859|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000 |
| 9 | 0.7606|0.9437|0.9859|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000 |
| 10 | 0.7606|0.9437|0.9859|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000 |
| 11 | 0.7606|0.9437|0.9859|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000 |
| 12 | 0.7606|0.9437|0.9859|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000 |
| 13 | 0.7606|0.9437|0.9859|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000 |
| 14 | 0.7606|0.9437|0.9859|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000 |
| 15 | 0.7606|0.9437|0.9859|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000 |
| 16 | 0.7606|0.9437|0.9859|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000 |
| 17 | 0.7606|0.9437|0.9859|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000 |
| 18 | 0.7606|0.9437|0.9859|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000 |
| 19 | 0.7606|0.9437|0.9859|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000 |
| 20 | 0.7606|0.9437|0.9859|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000 |
| 21 | 0.7606|0.9437|0.9859|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000 |
| 22 | 0.7606|0.9437|0.9859|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000 |
| 23 | 0.7606|0.9437|0.9859|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000 |
| 24 | 0.7606|0.9437|0.9859|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000 |
| 25 | 0.7606|0.9437|0.9859|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000 |
| 26 | 0.7606|0.9437|0.9859|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000 |
| 27 | 0.7606|0.9437|0.9859|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000 |
| 28 | 0.7606|0.9437|0.9859|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000 |
| 29 | 0.7606|0.9437|0.9859|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000 |
| 30 | 0.7606|0.9437|0.9859|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000 |
| 31 | 0.7606|0.9437|0.9859|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000 |
| 32 | 0.7606|0.9437|0.9859|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000 |
| 33 | 0.7606|0.9437|0.9859|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000 |
| 34 | 0.7606|0.9437|0.9859|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000|1.0000 |
