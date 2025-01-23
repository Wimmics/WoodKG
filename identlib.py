PREFIX = """prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
prefix owl: <http://www.w3.org/2002/07/owl#>
prefix iawa:<https://www.iawa-website.org/core#>
prefix skos: <http://www.w3.org/2004/02/skos/core#>
prefix pl_tax: <http://www.plant-taxonomy-kg.com/core#>
prefix sosa: <http://www.w3.org/ns/sosa/>
prefix wcvp: <http://www.wcvp-core.com/class#>
prefix txrfp: <http://taxref.mnhn.fr/lod/property/>
"""
new_line = '\n'


def get_sample_id(features_list, subgraph):
    return f"""{PREFIX}
select (str(?s) as ?sample) where {{
    ?s pl_tax:hasObservation {f',{new_line}'.join(features_list)}.
    {'FILTER(?s = <https://www.wood-sample-observation.com/sample/TSW-1>)' if subgraph else ''}
}}  
"""

def get_sample_by_name(name, samples):
    return f"""{PREFIX}
select (str(?s) as ?sample) where {{
    ?s pl_tax:identifiedTaxon ?taxon.
  ?taxon skos:prefLabel \"{name}\".
  FILTER(str(?s) in ({', '.join(samples)}))
}}
"""

def get_insert_sample(features_list):
    return f"""{PREFIX}
    insert {{ <https://www.wood-sample-observation.com/sample/TSW-1> pl_tax:hasObservation {f',{new_line}'.join(features_list)}.}} where {{}}   """

def delete_triple():
    return f"""{PREFIX}
        delete where {{ <https://www.wood-sample-observation.com/sample/TSW-1> pl_tax:hasObservation ?obs }} """

#SELECT  ?sample ?family_name ?label ?mismatch ?origin WHERE
def get_sample_by_mismatch(sample, binding, nb_mismatch, limit):
    return f"""{PREFIX}
SELECT DISTINCT ?{binding} WHERE {{
    {{
        SELECT DISTINCT ?sample ?family_name ?genus_name ?label ?mismatch ?origin WHERE {{
            ?classes txrfp:hasReferenceName ?taxon;
                rdfs:subClassOf ?genus.
            ?genus rdfs:label ?genus_name;
            rdfs:subClassOf ?family.
            ?family rdfs:label ?family_name.
    
            {{ SELECT ?sample ?label ?taxon ((?origin - COUNT(?feature)) as ?mismatch) ?origin WHERE {{
                    {{ SELECT ?feature WHERE {{<{sample}> pl_tax:hasObservation [sosa:hasResult [rdf:value ?feature]]. }} }}
                    {{ SELECT (COUNT(?feature) as ?origin) WHERE {{<{sample}> pl_tax:hasObservation [sosa:hasResult [rdf:value ?feature]]. }} }}
                    ?sample pl_tax:hasObservation [ sosa:hasResult [ rdf:value ?feature]];
                        pl_tax:identifiedTaxon ?taxon.
                    ?taxon skos:prefLabel ?label.
                    FILTER (?sample != <{sample}>)
                    }}
                    GROUP BY ?sample ?origin ?label ?taxon
                    ORDER BY ?mismatch 
            }}
        FILTER( ?mismatch <= {nb_mismatch})
    }}
    ORDER BY ?mismatch
}}
}}LIMIT {limit}
"""


def get_sample_by_mismatch_with_double(sample):
    return f"""{PREFIX}
SELECT DISTINCT ?sample ?family_name ?genus_name ?label ?mismatch ?origin WHERE {{
    ?classes txrfp:hasReferenceName ?taxon;
        rdfs:subClassOf ?genus.
    ?genus rdfs:label ?genus_name;
    rdfs:subClassOf ?family.
    ?family rdfs:label ?family_name.

    {{ SELECT ?sample ?label ?taxon ((?origin - COUNT(?feature)) as ?mismatch) ?origin WHERE {{
            {{ SELECT ?feature WHERE {{<{sample}> pl_tax:hasObservation [sosa:hasResult [rdf:value ?feature]]. }} }}
            {{ SELECT (COUNT(?feature) as ?origin) WHERE {{<{sample}> pl_tax:hasObservation [sosa:hasResult [rdf:value ?feature]]. }} }}
            ?sample pl_tax:hasObservation [ sosa:hasResult [ rdf:value ?feature]];
                pl_tax:identifiedTaxon ?taxon.
            ?taxon skos:prefLabel ?label.
            FILTER (?sample != <{sample}>)
            }}
            GROUP BY ?sample ?origin ?label ?taxon
            ORDER BY ?mismatch 
    }}
}}
ORDER BY ?mismatch
"""

def extract_feature_list(df, row, data):
    features_list = []
    feature_values = {3: "IFV-2", 2: "IFV-3", 1: "IFV-4", 0: ""}
    for features in df.columns[8:]:
        if int(features) > 163:
            break
        if df[features][row] != 0:
            data[int(features)] = 1
            features_list.append(
                f"""[sosa:hasResult[rdf:value <https://www.iawa-website.org/features/IFC-{features}>;
                pl_tax:presence <https://www.iawa-website.org/features/{feature_values[int(df[features][row])]}>]]""")
    return features_list


def build_header_report(file_path):
    with open(file_path, "w") as file_report:
        file_report.write(f"# File report of identification taxa with inside wood protocol\n\n")
        file_report.write(f"Request used to retrieve samples :\n\n")
        file_report.write(f"""```sparql
    SELECT DISTINCT ?family_name ?mismatch ?origin WHERE {{
        ?classes txrfp:hasReferenceName ?taxon;
            rdfs:subClassOf/rdfs:subClassOf ?family.
        ?family rdfs:label ?family_name.

        {{ select ?sample ?label ?taxon ((?origin - COUNT(?feature)) as ?mismatch) ?origin where {{
            	{{SELECT ?feature WHERE {{<sample> pl_tax:hasObservation [sosa:hasResult [rdf:value ?feature; pl_tax:presence ?presence]].}} }}
            	{{SELECT (COUNT(?feature) as ?origin) WHERE {{<sample> pl_tax:hasObservation [sosa:hasResult [rdf:value ?feature; pl_tax:presence ?presence]].}} }}
                ?sample pl_tax:hasObservation [ sosa:hasResult [ rdf:value ?feature; pl_tax:presence ?presence]];
                	pl_tax:identifiedTaxon ?taxon.
                ?taxon skos:prefLabel ?label.
                FILTER (?sample != <sample>)
            }}
            GROUP BY ?sample ?origin ?label ?taxon
            ORDER BY ?mismatch        
        }}
    }}
    ORDER BY ?mismatch
    ```\n\n""")

def get_label_list_distinct(result, binding, k):
    labels = []
    for elt in result:
        if int(elt["mismatch"]["value"]) <= k:
            label = elt[binding]["value"]
            if label not in labels:
                labels.append(label)
    return labels

def get_label_list_distinct_i(result, binding, k, i):
    labels = []
    for elt in result:
        if len(labels) == i:
            break
        if int(elt["mismatch"]["value"]) <= k:
            label = elt[binding]["value"]
            if label not in labels:
                labels.append(label)
    return labels