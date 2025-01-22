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
- 1 row(s): precision 0.717741935483871
- 2 row(s): precision 0.8266129032258065
- 3 row(s): precision 0.8951612903225806
- 4 row(s): precision 0.9193548387096774
- 5 row(s): precision 0.9314516129032258
- 6 row(s): precision 0.9556451612903226
- 7 row(s): precision 0.967741935483871
- 8 row(s): precision 0.967741935483871
- 9 row(s): precision 0.9717741935483871
- 10 row(s): precision 0.9758064516129032
- 11 row(s): precision 0.9838709677419355
- 12 row(s): precision 0.9838709677419355
- 13 row(s): precision 0.9838709677419355
- 14 row(s): precision 0.9879032258064516
- 15 row(s): precision 0.9879032258064516
- 16 row(s): precision 0.9879032258064516
- 17 row(s): precision 0.9879032258064516
- 18 row(s): precision 0.9879032258064516
- 19 row(s): precision 0.9879032258064516
- 20 row(s): precision 0.9879032258064516
- 21 row(s): precision 0.9879032258064516
- 22 row(s): precision 0.9919354838709677
- 23 row(s): precision 0.9959677419354839
- 24 row(s): precision 0.9959677419354839
- 25 row(s): precision 0.9959677419354839
- 26 row(s): precision 0.9959677419354839
- 27 row(s): precision 0.9959677419354839
- 28 row(s): precision 0.9959677419354839
- 29 row(s): precision 0.9959677419354839
- 30 row(s): precision 0.9959677419354839
- 31 row(s): precision 0.9959677419354839
- 32 row(s): precision 0.9959677419354839
- 33 row(s): precision 0.9959677419354839
- 34 row(s): precision 0.9959677419354839
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
|0|0.0363|0.0524|0.3610|
|1|0.1250|0.1492|0.4556|
|2|0.2702|0.3347|0.5998|
|3|0.4435|0.8145|1.3221|
|4|0.5484|1.5161|2.6365|
|5|0.7097|2.9879|4.6494|
|6|0.8024|4.9395|6.4107|
|7|0.8750|7.9113|8.6281|
|8|0.9153|11.7984|11.0701|
|9|0.9476|16.5121|13.3788|
|10|0.9597|21.3185|14.9720|
|11|0.9839|26.3952|15.7043|
|12|0.9919|31.5806|15.6430|
|13|0.9919|36.1008|14.9119|
|14|0.9919|40.2581|13.9705|
|15|0.9960|43.8266|12.4427|
|16|1.0000|46.5363|10.9592|
|17|1.0000|48.6532|9.2314|
|18|1.0000|50.2540|7.3146|
|19|1.0000|51.4355|5.8244|
|20|1.0000|52.2903|4.4255|
|21|1.0000|52.9073|3.2632|
|22|1.0000|53.3871|2.0721|
|23|1.0000|53.6694|1.4268|
|24|1.0000|53.8024|0.9946|
|25|1.0000|53.8750|0.6322|
|26|1.0000|53.9435|0.3312|
|27|1.0000|53.9677|0.2176|
|28|1.0000|53.9798|0.1668|
|29|1.0000|53.9960|0.0634|
|30|1.0000|54.0000|0.0000|
|31|1.0000|54.0000|0.0000|
|32|1.0000|54.0000|0.0000|
|33|1.0000|54.0000|0.0000|
|34|1.0000|54.0000|0.0000|
|35|1.0000|54.0000|0.0000|
|36|1.0000|54.0000|0.0000|
|37|1.0000|54.0000|0.0000|
|38|1.0000|54.0000|0.0000|
|39|1.0000|54.0000|0.0000|
|40|1.0000|54.0000|0.0000|
|41|1.0000|54.0000|0.0000|
|42|1.0000|54.0000|0.0000|
|43|1.0000|54.0000|0.0000|
|44|1.0000|54.0000|0.0000|
|45|1.0000|54.0000|0.0000|
|46|1.0000|54.0000|0.0000|
|47|1.0000|54.0000|0.0000|
|48|1.0000|54.0000|0.0000|
|49|1.0000|54.0000|0.0000|

## Precision at n first mismatch: (note: *it can be 0 mismatch*)
- 1 first mismatch: precision 0.7944
- 2 first mismatch: precision 0.8992
- 3 first mismatch: precision 0.9556
- 4 first mismatch: precision 0.9839
- 5 first mismatch: precision 0.9919
- 6 first mismatch: precision 0.9960
- 7 first mismatch: precision 0.9960
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
| 1 | 0.7177|0.7903|0.7903|0.7944|0.7944|0.7944|0.7944|0.7944|0.7944|0.7944 |
| 2 | 0.7177|0.8669|0.8750|0.8952|0.8952|0.8992|0.8992|0.8992|0.8992|0.8992 |
| 3 | 0.7177|0.8831|0.9113|0.9476|0.9516|0.9556|0.9556|0.9556|0.9556|0.9556 |
| 4 | 0.7177|0.8952|0.9274|0.9637|0.9677|0.9718|0.9798|0.9798|0.9798|0.9798 |
| 5 | 0.7177|0.8952|0.9315|0.9677|0.9718|0.9758|0.9839|0.9839|0.9839|0.9839 |
| 6 | 0.7177|0.8952|0.9315|0.9677|0.9718|0.9758|0.9839|0.9879|0.9879|0.9879 |
| 7 | 0.7177|0.8952|0.9315|0.9677|0.9718|0.9758|0.9839|0.9879|0.9879|0.9879 |
| 8 | 0.7177|0.8952|0.9315|0.9677|0.9718|0.9758|0.9839|0.9879|0.9879|0.9879 |
| 9 | 0.7177|0.8952|0.9315|0.9677|0.9718|0.9758|0.9839|0.9879|0.9879|0.9879 |
| 10 | 0.7177|0.8952|0.9315|0.9677|0.9718|0.9758|0.9839|0.9879|0.9879|0.9879 |
| 11 | 0.7177|0.8952|0.9315|0.9677|0.9718|0.9758|0.9839|0.9879|0.9879|0.9879 |
| 12 | 0.7177|0.8952|0.9315|0.9677|0.9718|0.9758|0.9839|0.9879|0.9879|0.9879 |
| 13 | 0.7177|0.8952|0.9315|0.9677|0.9718|0.9758|0.9839|0.9879|0.9879|0.9879 |
| 14 | 0.7177|0.8952|0.9315|0.9677|0.9718|0.9758|0.9839|0.9879|0.9879|0.9879 |
| 15 | 0.7177|0.8952|0.9315|0.9677|0.9718|0.9758|0.9839|0.9879|0.9879|0.9879 |
| 16 | 0.7177|0.8952|0.9315|0.9677|0.9718|0.9758|0.9839|0.9879|0.9879|0.9879 |
| 17 | 0.7177|0.8952|0.9315|0.9677|0.9718|0.9758|0.9839|0.9879|0.9879|0.9879 |
| 18 | 0.7177|0.8952|0.9315|0.9677|0.9718|0.9758|0.9839|0.9879|0.9879|0.9879 |
| 19 | 0.7177|0.8952|0.9315|0.9677|0.9718|0.9758|0.9839|0.9879|0.9879|0.9879 |
| 20 | 0.7177|0.8952|0.9315|0.9677|0.9718|0.9758|0.9839|0.9879|0.9879|0.9879 |
| 21 | 0.7177|0.8952|0.9315|0.9677|0.9718|0.9758|0.9839|0.9879|0.9879|0.9879 |
| 22 | 0.7177|0.8952|0.9315|0.9677|0.9718|0.9758|0.9839|0.9879|0.9879|0.9879 |
| 23 | 0.7177|0.8952|0.9315|0.9677|0.9718|0.9758|0.9839|0.9879|0.9879|0.9879 |
| 24 | 0.7177|0.8952|0.9315|0.9677|0.9718|0.9758|0.9839|0.9879|0.9879|0.9879 |
| 25 | 0.7177|0.8952|0.9315|0.9677|0.9718|0.9758|0.9839|0.9879|0.9879|0.9879 |
| 26 | 0.7177|0.8952|0.9315|0.9677|0.9718|0.9758|0.9839|0.9879|0.9879|0.9879 |
| 27 | 0.7177|0.8952|0.9315|0.9677|0.9718|0.9758|0.9839|0.9879|0.9879|0.9879 |
| 28 | 0.7177|0.8952|0.9315|0.9677|0.9718|0.9758|0.9839|0.9879|0.9879|0.9879 |
| 29 | 0.7177|0.8952|0.9315|0.9677|0.9718|0.9758|0.9839|0.9879|0.9879|0.9879 |
| 30 | 0.7177|0.8952|0.9315|0.9677|0.9718|0.9758|0.9839|0.9879|0.9879|0.9879 |
| 31 | 0.7177|0.8952|0.9315|0.9677|0.9718|0.9758|0.9839|0.9879|0.9879|0.9879 |
| 32 | 0.7177|0.8952|0.9315|0.9677|0.9718|0.9758|0.9839|0.9879|0.9879|0.9879 |
| 33 | 0.7177|0.8952|0.9315|0.9677|0.9718|0.9758|0.9839|0.9879|0.9879|0.9879 |
| 34 | 0.7177|0.8952|0.9315|0.9677|0.9718|0.9758|0.9839|0.9879|0.9879|0.9879 |
