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
- 1 row(s): precision 0.7421875
- 2 row(s): precision 0.8515625
- 3 row(s): precision 0.8828125
- 4 row(s): precision 0.921875
- 5 row(s): precision 0.9296875
- 6 row(s): precision 0.9375
- 7 row(s): precision 0.953125
- 8 row(s): precision 0.96875
- 9 row(s): precision 0.96875
- 10 row(s): precision 0.96875
- 11 row(s): precision 0.96875
- 12 row(s): precision 0.96875
- 13 row(s): precision 0.96875
- 14 row(s): precision 0.9765625
- 15 row(s): precision 0.9765625
- 16 row(s): precision 0.9765625
- 17 row(s): precision 0.9765625
- 18 row(s): precision 0.984375
- 19 row(s): precision 0.984375
- 20 row(s): precision 0.9921875
- 21 row(s): precision 0.9921875
- 22 row(s): precision 0.9921875
- 23 row(s): precision 0.9921875
- 24 row(s): precision 0.9921875
- 25 row(s): precision 0.9921875
- 26 row(s): precision 0.9921875
- 27 row(s): precision 0.9921875
- 28 row(s): precision 0.9921875
- 29 row(s): precision 0.9921875
- 30 row(s): precision 0.9921875
- 31 row(s): precision 0.9921875
- 32 row(s): precision 0.9921875
- 33 row(s): precision 0.9921875
- 34 row(s): precision 0.9921875
- 35 row(s): precision 0.9921875
- 36 row(s): precision 0.9921875
- 37 row(s): precision 0.9921875
- 38 row(s): precision 0.9921875
- 39 row(s): precision 0.9921875
- 40 row(s): precision 0.9921875
- 41 row(s): precision 0.9921875
- 42 row(s): precision 0.9921875
- 43 row(s): precision 0.9921875
- 44 row(s): precision 0.9921875
- 45 row(s): precision 0.9921875
- 46 row(s): precision 0.9921875
- 47 row(s): precision 0.9921875
- 48 row(s): precision 0.9921875
- 49 row(s): precision 0.9921875

## Precision at n mismatch: 
| Mismatch | Precision | Average Nb of Row | Standard deviation |
|---|---|---|---|
|0|0.0859|0.1016|0.3269|
|1|0.2969|0.4141|0.8797|
|2|0.4297|0.7656|1.4333|
|3|0.5469|1.3594|2.4960|
|4|0.6719|2.2344|4.0282|
|5|0.7656|3.8750|6.4311|
|6|0.8125|5.8750|8.4484|
|7|0.8906|8.9609|10.6861|
|8|0.8906|12.9766|12.7925|
|9|0.9453|18.2109|14.9857|
|10|0.9531|24.0703|16.7846|
|11|0.9609|30.0547|17.6371|
|12|0.9766|36.1016|18.4144|
|13|0.9766|41.8828|18.3825|
|14|0.9844|46.5391|17.8408|
|15|0.9922|50.5312|16.4131|
|16|0.9922|53.5781|15.1305|
|17|0.9922|56.0000|13.8304|
|18|1.0000|58.2266|11.4818|
|19|1.0000|59.7812|9.7291|
|20|1.0000|61.1406|7.2389|
|21|1.0000|62.1406|5.2048|
|22|1.0000|62.8281|3.6489|
|23|1.0000|63.2734|2.4067|
|24|1.0000|63.6016|1.3308|
|25|1.0000|63.7812|0.8655|
|26|1.0000|63.9062|0.4582|
|27|1.0000|63.9688|0.2142|
|28|1.0000|63.9844|0.1761|
|29|1.0000|63.9922|0.0880|
|30|1.0000|64.0000|0.0000|
|31|1.0000|64.0000|0.0000|
|32|1.0000|64.0000|0.0000|
|33|1.0000|64.0000|0.0000|
|34|1.0000|64.0000|0.0000|
|35|1.0000|64.0000|0.0000|
|36|1.0000|64.0000|0.0000|
|37|1.0000|64.0000|0.0000|
|38|1.0000|64.0000|0.0000|
|39|1.0000|64.0000|0.0000|
|40|1.0000|64.0000|0.0000|
|41|1.0000|64.0000|0.0000|
|42|1.0000|64.0000|0.0000|
|43|1.0000|64.0000|0.0000|
|44|1.0000|64.0000|0.0000|
|45|1.0000|64.0000|0.0000|
|46|1.0000|64.0000|0.0000|
|47|1.0000|64.0000|0.0000|
|48|1.0000|64.0000|0.0000|
|49|1.0000|64.0000|0.0000|

## Precision at n first mismatch: (note: *it can be 0 mismatch*)
- 1 first mismatch: precision 0.8047
- 2 first mismatch: precision 0.9062
- 3 first mismatch: precision 0.9531
- 4 first mismatch: precision 0.9609
- 5 first mismatch: precision 0.9844
- 6 first mismatch: precision 0.9922
- 7 first mismatch: precision 0.9922
- 8 first mismatch: precision 0.9922
- 9 first mismatch: precision 0.9922
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

## Precision at n first mismatch with limited result number: (note: *it can be 0 mismatch*)
| N-first mismatch/Number of line | 1|3|5|7|9|10|13|15|17|20 | 
|--- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---  | 
| 1 | 0.7422|0.8047|0.8047|0.8047|0.8047|0.8047|0.8047|0.8047|0.8047|0.8047 |
| 2 | 0.7422|0.8672|0.8906|0.9062|0.9062|0.9062|0.9062|0.9062|0.9062|0.9062 |
| 3 | 0.7422|0.8828|0.9297|0.9531|0.9531|0.9531|0.9531|0.9531|0.9531|0.9531 |
| 4 | 0.7422|0.8828|0.9297|0.9531|0.9531|0.9531|0.9531|0.9609|0.9609|0.9609 |
| 5 | 0.7422|0.8828|0.9297|0.9531|0.9688|0.9688|0.9688|0.9766|0.9766|0.9844 |
| 6 | 0.7422|0.8828|0.9297|0.9531|0.9688|0.9688|0.9688|0.9766|0.9766|0.9922 |
| 7 | 0.7422|0.8828|0.9297|0.9531|0.9688|0.9688|0.9688|0.9766|0.9766|0.9922 |
| 8 | 0.7422|0.8828|0.9297|0.9531|0.9688|0.9688|0.9688|0.9766|0.9766|0.9922 |
| 9 | 0.7422|0.8828|0.9297|0.9531|0.9688|0.9688|0.9688|0.9766|0.9766|0.9922 |
| 10 | 0.7422|0.8828|0.9297|0.9531|0.9688|0.9688|0.9688|0.9766|0.9766|0.9922 |
| 11 | 0.7422|0.8828|0.9297|0.9531|0.9688|0.9688|0.9688|0.9766|0.9766|0.9922 |
| 12 | 0.7422|0.8828|0.9297|0.9531|0.9688|0.9688|0.9688|0.9766|0.9766|0.9922 |
| 13 | 0.7422|0.8828|0.9297|0.9531|0.9688|0.9688|0.9688|0.9766|0.9766|0.9922 |
| 14 | 0.7422|0.8828|0.9297|0.9531|0.9688|0.9688|0.9688|0.9766|0.9766|0.9922 |
| 15 | 0.7422|0.8828|0.9297|0.9531|0.9688|0.9688|0.9688|0.9766|0.9766|0.9922 |
| 16 | 0.7422|0.8828|0.9297|0.9531|0.9688|0.9688|0.9688|0.9766|0.9766|0.9922 |
| 17 | 0.7422|0.8828|0.9297|0.9531|0.9688|0.9688|0.9688|0.9766|0.9766|0.9922 |
| 18 | 0.7422|0.8828|0.9297|0.9531|0.9688|0.9688|0.9688|0.9766|0.9766|0.9922 |
| 19 | 0.7422|0.8828|0.9297|0.9531|0.9688|0.9688|0.9688|0.9766|0.9766|0.9922 |
| 20 | 0.7422|0.8828|0.9297|0.9531|0.9688|0.9688|0.9688|0.9766|0.9766|0.9922 |
| 21 | 0.7422|0.8828|0.9297|0.9531|0.9688|0.9688|0.9688|0.9766|0.9766|0.9922 |
| 22 | 0.7422|0.8828|0.9297|0.9531|0.9688|0.9688|0.9688|0.9766|0.9766|0.9922 |
| 23 | 0.7422|0.8828|0.9297|0.9531|0.9688|0.9688|0.9688|0.9766|0.9766|0.9922 |
| 24 | 0.7422|0.8828|0.9297|0.9531|0.9688|0.9688|0.9688|0.9766|0.9766|0.9922 |
| 25 | 0.7422|0.8828|0.9297|0.9531|0.9688|0.9688|0.9688|0.9766|0.9766|0.9922 |
| 26 | 0.7422|0.8828|0.9297|0.9531|0.9688|0.9688|0.9688|0.9766|0.9766|0.9922 |
| 27 | 0.7422|0.8828|0.9297|0.9531|0.9688|0.9688|0.9688|0.9766|0.9766|0.9922 |
| 28 | 0.7422|0.8828|0.9297|0.9531|0.9688|0.9688|0.9688|0.9766|0.9766|0.9922 |
| 29 | 0.7422|0.8828|0.9297|0.9531|0.9688|0.9688|0.9688|0.9766|0.9766|0.9922 |
| 30 | 0.7422|0.8828|0.9297|0.9531|0.9688|0.9688|0.9688|0.9766|0.9766|0.9922 |
| 31 | 0.7422|0.8828|0.9297|0.9531|0.9688|0.9688|0.9688|0.9766|0.9766|0.9922 |
| 32 | 0.7422|0.8828|0.9297|0.9531|0.9688|0.9688|0.9688|0.9766|0.9766|0.9922 |
| 33 | 0.7422|0.8828|0.9297|0.9531|0.9688|0.9688|0.9688|0.9766|0.9766|0.9922 |
| 34 | 0.7422|0.8828|0.9297|0.9531|0.9688|0.9688|0.9688|0.9766|0.9766|0.9922 |
