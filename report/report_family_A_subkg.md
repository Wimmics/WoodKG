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
- 1 row(s): precision 0.7427055702917772
- 2 row(s): precision 0.8620689655172413
- 3 row(s): precision 0.8992042440318302
- 4 row(s): precision 0.9204244031830239
- 5 row(s): precision 0.9416445623342176
- 6 row(s): precision 0.9522546419098143
- 7 row(s): precision 0.9575596816976127
- 8 row(s): precision 0.9602122015915119
- 9 row(s): precision 0.9655172413793104
- 10 row(s): precision 0.9708222811671088
- 11 row(s): precision 0.9734748010610079
- 12 row(s): precision 0.9734748010610079
- 13 row(s): precision 0.9814323607427056
- 14 row(s): precision 0.9814323607427056
- 15 row(s): precision 0.9840848806366048
- 16 row(s): precision 0.9893899204244032
- 17 row(s): precision 0.9893899204244032
- 18 row(s): precision 0.9893899204244032
- 19 row(s): precision 0.9893899204244032
- 20 row(s): precision 0.9893899204244032
- 21 row(s): precision 0.9893899204244032
- 22 row(s): precision 0.9893899204244032
- 23 row(s): precision 0.9920424403183024
- 24 row(s): precision 0.9920424403183024
- 25 row(s): precision 0.9920424403183024
- 26 row(s): precision 0.9946949602122016
- 27 row(s): precision 0.9946949602122016
- 28 row(s): precision 0.9946949602122016
- 29 row(s): precision 0.9973474801061007
- 30 row(s): precision 0.9973474801061007
- 31 row(s): precision 0.9973474801061007
- 32 row(s): precision 0.9973474801061007
- 33 row(s): precision 0.9973474801061007
- 34 row(s): precision 0.9973474801061007
- 35 row(s): precision 0.9973474801061007
- 36 row(s): precision 0.9973474801061007
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
|0|0.0424|0.0451|0.2199|
|1|0.1698|0.1963|0.4533|
|2|0.3369|0.5093|1.0683|
|3|0.4960|0.9735|1.7854|
|4|0.6180|1.8382|3.2886|
|5|0.7109|3.2679|4.9640|
|6|0.8064|5.6552|7.5333|
|7|0.8647|8.8143|10.1219|
|8|0.9125|12.8594|12.7780|
|9|0.9416|17.7613|14.9564|
|10|0.9682|23.2599|16.6536|
|11|0.9867|28.6923|17.5121|
|12|0.9920|34.4244|17.4636|
|13|0.9947|39.8780|16.7616|
|14|1.0000|44.6923|15.5988|
|15|1.0000|48.7613|13.9891|
|16|1.0000|51.9098|12.1896|
|17|1.0000|54.4960|10.5303|
|18|1.0000|56.3767|8.8078|
|19|1.0000|57.7905|7.2891|
|20|1.0000|58.8064|5.8111|
|21|1.0000|59.5438|4.4750|
|22|1.0000|60.0928|3.3920|
|23|1.0000|60.4377|2.5476|
|24|1.0000|60.6658|1.8894|
|25|1.0000|60.7745|1.3799|
|26|1.0000|60.8515|1.0450|
|27|1.0000|60.9019|0.7732|
|28|1.0000|60.9523|0.4157|
|29|1.0000|60.9708|0.3119|
|30|1.0000|60.9814|0.1986|
|31|1.0000|60.9920|0.0888|
|32|1.0000|60.9947|0.0726|
|33|1.0000|61.0000|0.0000|
|34|1.0000|61.0000|0.0000|
|35|1.0000|61.0000|0.0000|
|36|1.0000|61.0000|0.0000|
|37|1.0000|61.0000|0.0000|
|38|1.0000|61.0000|0.0000|
|39|1.0000|61.0000|0.0000|
|40|1.0000|61.0000|0.0000|
|41|1.0000|61.0000|0.0000|
|42|1.0000|61.0000|0.0000|
|43|1.0000|61.0000|0.0000|
|44|1.0000|61.0000|0.0000|
|45|1.0000|61.0000|0.0000|
|46|1.0000|61.0000|0.0000|
|47|1.0000|61.0000|0.0000|
|48|1.0000|61.0000|0.0000|
|49|1.0000|61.0000|0.0000|

## Precision at n first mismatch: (note: *it can be 0 mismatch*)
- 1 first mismatch: precision 0.8090
- 2 first mismatch: precision 0.9045
- 3 first mismatch: precision 0.9390
- 4 first mismatch: precision 0.9682
- 5 first mismatch: precision 0.9867
- 6 first mismatch: precision 0.9973
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

## Precision at n first mismatch with limited result number: (note: *it can be 0 mismatch*)
| N-first mismatch/Number of line | 1|3|5|7|9|10|13|15|17|20 | 
|--- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---  | 
| 1 | 0.7427|0.8037|0.8090|0.8090|0.8090|0.8090|0.8090|0.8090|0.8090|0.8090 |
| 2 | 0.7427|0.8833|0.9045|0.9045|0.9045|0.9045|0.9045|0.9045|0.9045|0.9045 |
| 3 | 0.7427|0.8912|0.9257|0.9284|0.9337|0.9390|0.9390|0.9390|0.9390|0.9390 |
| 4 | 0.7427|0.8992|0.9363|0.9496|0.9549|0.9602|0.9682|0.9682|0.9682|0.9682 |
| 5 | 0.7427|0.8992|0.9390|0.9549|0.9629|0.9682|0.9761|0.9761|0.9788|0.9788 |
| 6 | 0.7427|0.8992|0.9416|0.9576|0.9655|0.9708|0.9788|0.9814|0.9867|0.9867 |
| 7 | 0.7427|0.8992|0.9416|0.9576|0.9655|0.9708|0.9814|0.9841|0.9894|0.9894 |
| 8 | 0.7427|0.8992|0.9416|0.9576|0.9655|0.9708|0.9814|0.9841|0.9894|0.9894 |
| 9 | 0.7427|0.8992|0.9416|0.9576|0.9655|0.9708|0.9814|0.9841|0.9894|0.9894 |
| 10 | 0.7427|0.8992|0.9416|0.9576|0.9655|0.9708|0.9814|0.9841|0.9894|0.9894 |
| 11 | 0.7427|0.8992|0.9416|0.9576|0.9655|0.9708|0.9814|0.9841|0.9894|0.9894 |
| 12 | 0.7427|0.8992|0.9416|0.9576|0.9655|0.9708|0.9814|0.9841|0.9894|0.9894 |
| 13 | 0.7427|0.8992|0.9416|0.9576|0.9655|0.9708|0.9814|0.9841|0.9894|0.9894 |
| 14 | 0.7427|0.8992|0.9416|0.9576|0.9655|0.9708|0.9814|0.9841|0.9894|0.9894 |
| 15 | 0.7427|0.8992|0.9416|0.9576|0.9655|0.9708|0.9814|0.9841|0.9894|0.9894 |
| 16 | 0.7427|0.8992|0.9416|0.9576|0.9655|0.9708|0.9814|0.9841|0.9894|0.9894 |
| 17 | 0.7427|0.8992|0.9416|0.9576|0.9655|0.9708|0.9814|0.9841|0.9894|0.9894 |
| 18 | 0.7427|0.8992|0.9416|0.9576|0.9655|0.9708|0.9814|0.9841|0.9894|0.9894 |
| 19 | 0.7427|0.8992|0.9416|0.9576|0.9655|0.9708|0.9814|0.9841|0.9894|0.9894 |
| 20 | 0.7427|0.8992|0.9416|0.9576|0.9655|0.9708|0.9814|0.9841|0.9894|0.9894 |
| 21 | 0.7427|0.8992|0.9416|0.9576|0.9655|0.9708|0.9814|0.9841|0.9894|0.9894 |
| 22 | 0.7427|0.8992|0.9416|0.9576|0.9655|0.9708|0.9814|0.9841|0.9894|0.9894 |
| 23 | 0.7427|0.8992|0.9416|0.9576|0.9655|0.9708|0.9814|0.9841|0.9894|0.9894 |
| 24 | 0.7427|0.8992|0.9416|0.9576|0.9655|0.9708|0.9814|0.9841|0.9894|0.9894 |
| 25 | 0.7427|0.8992|0.9416|0.9576|0.9655|0.9708|0.9814|0.9841|0.9894|0.9894 |
| 26 | 0.7427|0.8992|0.9416|0.9576|0.9655|0.9708|0.9814|0.9841|0.9894|0.9894 |
| 27 | 0.7427|0.8992|0.9416|0.9576|0.9655|0.9708|0.9814|0.9841|0.9894|0.9894 |
| 28 | 0.7427|0.8992|0.9416|0.9576|0.9655|0.9708|0.9814|0.9841|0.9894|0.9894 |
| 29 | 0.7427|0.8992|0.9416|0.9576|0.9655|0.9708|0.9814|0.9841|0.9894|0.9894 |
| 30 | 0.7427|0.8992|0.9416|0.9576|0.9655|0.9708|0.9814|0.9841|0.9894|0.9894 |
| 31 | 0.7427|0.8992|0.9416|0.9576|0.9655|0.9708|0.9814|0.9841|0.9894|0.9894 |
| 32 | 0.7427|0.8992|0.9416|0.9576|0.9655|0.9708|0.9814|0.9841|0.9894|0.9894 |
| 33 | 0.7427|0.8992|0.9416|0.9576|0.9655|0.9708|0.9814|0.9841|0.9894|0.9894 |
| 34 | 0.7427|0.8992|0.9416|0.9576|0.9655|0.9708|0.9814|0.9841|0.9894|0.9894 |
