import ujson as json

import pandas as pd
import atexit
import subprocess
from time import sleep, time
import matplotlib.pyplot as plt
from operator import itemgetter
from identlib import *
from py4j.java_gateway import JavaGateway
from ordered_set import OrderedSet

# Start java gateway
java_process = subprocess.Popen(
    ['java', '-jar', '-Dfile.encoding=UTF-8', 'corese-library-python-4.4.1.jar'])
sleep(1)
gateway = JavaGateway()

# Stop java gateway at the enf od script
def exit_handler():
    gateway.shutdown()
    print('\n' * 2)
    print('Gateway Server Stop!')

atexit.register(exit_handler)
# Import of class
Graph = gateway.jvm.fr.inria.corese.core.Graph
Load = gateway.jvm.fr.inria.corese.core.load.Load
Transformer = gateway.jvm.fr.inria.corese.core.transform.Transformer
QueryProcess = gateway.jvm.fr.inria.corese.core.query.QueryProcess
RDF = gateway.jvm.fr.inria.corese.core.logic.RDF
RESULTFORMAT = gateway.jvm.fr.inria.corese.core.print.ResultFormat
coreseFormat = gateway.jvm.fr.inria.corese.sparql.api.ResultFormatDef

def sparqlQuery(graph, query):
    """Run a query on a graph

    :param graph: the graph on which the query is executed
    :param query: query to run
    :returns: query result
    """
    exec = QueryProcess.create(graph)
    return exec.query(query)


def convert_sparql_to_json(mapping_object):
    """
    Transform sparql Java object map into standard JSON response
    :param mapping_object:
    :return:
    """
    sparql_formater = RESULTFORMAT.create(mapping_object)
    sparql_formater.setSelectFormat(coreseFormat.JSON_FORMAT)

    # Convert string to JSON
    json_convert = json.loads(sparql_formater.toString())
    return json_convert


def load(graph ,path):
    """Load a graph from a local file or a URL

    :param path: local path or a URL
    :returns: the graph load
    """

    ld = Load.create(graph)
    ld.parse(path)

    return graph



if __name__ == '__main__':

    taxon = "genus"
    letter = "C"
    KG = "subkg"
    binding = "genus_name"
    subgraph = True

    print(get_sample_by_mismatch("https://www.wood-sample-observation.com/sample/TSW-1", binding, 50, 5000))

    FILE_DATASET_RESULT = f"export_train_test/export_{letter}/export_test_powo_{taxon}.csv"
    FILE_REPORT = f"report_{taxon}_{letter}_{KG}.md"
    # FILE_REPORT = "report_genus_D_full_KG.md"
    # binding = "?genus_name"

    global_prec_at_n = []
    global_prec_at_mismatch = []
    global_prec_at_n_first_mismatch = []
    global_prec_at_n_first_mismatch_and_m_line = []

    lines_check = [1, 3, 5, 7, 9, 10, 13, 15, 17, 20]

    print("loading graphs...")
    alpha = time()
    graph = Graph()
    graph = load(graph, "Dataset/result_iawa.ttl")

    if subgraph:
        graph = load(graph, f"Dataset/result_sub_taxonomy_{letter.lower()}_{taxon}.ttl")
        graph = load(graph, f"Dataset/result_observations_{letter.lower()}_{taxon}.ttl")
    else:
        graph = load(graph, "Dataset/result_taxonomy.ttl")
        graph = load(graph, "Dataset/result_observations.ttl")

    print(f"graphs loaded in {time() - alpha}")

    test_df = pd.read_csv(FILE_DATASET_RESULT, sep=";", header=0, encoding="utf-8")
    data = [0 for x in range(163)]
    build_header_report(FILE_REPORT)
    counter = 1

    for row in test_df.index:
        alpha = time()

        data = [0 for x in range(163)]
        original_label = test_df["powo_taxon"][row]

        features_list = extract_feature_list(test_df, row, data)

        if subgraph:
            sparqlQuery(graph, get_insert_sample(features_list))
        res = [x.getValue("?sample") for x in sparqlQuery(graph, get_sample_id(features_list, subgraph)).getMappingList()]
        if len(res) == 0:
            print("WTF")
        if len(res) > 1:
            print("2 sample has the same feature (check presence value of features)")
            print(', '.join([x.toString() for x in res]))
            res = [x.getValue("?sample") for x in
                   sparqlQuery(graph, get_sample_by_name(original_label, [x.toString() for x in res])).getMappingList()]
            if len(res) == 0 or len(res) > 2:
                print(f"Error, duplicate label or no value found for {original_label} for family {test_df['powo_family'][row]}")
                res = [x.getValue("?sample") for x in sparqlQuery(graph, get_sample_id(features_list, subgraph)).getMappingList()]

        sample = str(res[0]).replace("\"", "")
        if not subgraph:
            original_taxon = [x.getValue(f"?{taxon}_label") for x in sparqlQuery(graph, get_sample_id(features_list, subgraph)).getMappingList()][0]
        else:
            original_taxon = test_df[f"powo_{taxon}"][row]
        print(sample)

        try:
            precision_at_k = []
            precision_at_k_mismatch = []
            precision_at_k_first_mismatch = []
            precision_at_k_first_mismatch_and_i_line = []

            # Precision at N row
            # K here is the number of row
            result = convert_sparql_to_json(sparqlQuery(graph, get_sample_by_mismatch(sample, binding, 50, 5000)))["results"]["bindings"]
            for k in range(1, 50):
                good_sample = False
                i = 0
                while i < k and i < len(result):
                    taxa = result[i][binding]["value"]
                    if taxa == original_taxon:
                        good_sample = True
                        precision_at_k.append((k, 1))
                        break
                    i += 1
                if not good_sample:
                    precision_at_k.append((k, 0))

            global_prec_at_n.append(precision_at_k)

            # K ici est le nombre de mismatchs maximal
            result = convert_sparql_to_json(sparqlQuery(graph, get_sample_by_mismatch_with_double(sample)))["results"]["bindings"]
            for k in range(0, 50):
                current_k = []
                labels = get_label_list_distinct(result, binding, k)

                for label in labels:
                    if label == original_taxon:
                        current_k.append(1)
                    else:
                        current_k.append(0)

                if not current_k:
                    precision_at_k_mismatch.append((k,
                        0,
                        0,
                        0
                    ))
                else:
                    precision_at_k_mismatch.append((k,
                                                1 if sum(current_k) >= 1 else 0,
                                                len(current_k),
                                                sum(current_k)
                                                ))
            global_prec_at_mismatch.append(precision_at_k_mismatch)

            # Précision at k firt mismatch
            # The main idea is to use the fact that result are sorted on mismatch.
            # Therefore, the first mismatch are the top rows of the table.
            try :

                first_mm = int(result[0]["mismatch"]["value"])
                for k in range(first_mm, 50):
                    current_k = []
                    labels = get_label_list_distinct(result, binding, k)

                    for label in labels:
                        if label == original_taxon:
                            current_k.append(1)
                        else:
                            current_k.append(0)

                    if 1 in current_k:
                        precision_at_k_first_mismatch.append((k,
                                                              1,
                                                              len(current_k),
                                                              sum(current_k)
                                                              ))
                    else:
                        precision_at_k_first_mismatch.append((k,
                                                              0,
                                                              len(current_k),
                                                              sum(current_k)
                                                              ))
                global_prec_at_n_first_mismatch.append(precision_at_k_first_mismatch)

            except Exception as e:
                print("No result")

            # Précision at k firt mismatch
            # The main idea is to use the fact that result are sorted on mismatch.
            # Therefore, the first mismatch are the top rows of the table.
            # We add the display of line in this one for application purpose.
            # User won't check over 15 lines
            try:
                first_mm = int(result[0]["mismatch"]["value"])
                for i in lines_check:
                    for k in range(first_mm, 50):
                        current_k = []
                        labels = get_label_list_distinct_i(result,binding, k, i)

                        for label in labels:
                            if label == original_taxon:
                                current_k.append(1)
                            else:
                                current_k.append(0)

                        "(allowed_mismatch, relevant(T,F), number_of_sample, number_of_relevant, number_of_line_max)"
                        if 1 in current_k:
                            precision_at_k_first_mismatch_and_i_line.append((k,
                                                                             1,
                                                                             len(current_k),
                                                                             sum(current_k),
                                                                             i
                                                                             ))
                        else:
                            precision_at_k_first_mismatch_and_i_line.append((k,
                                                                             0,
                                                                             len(current_k),
                                                                             sum(current_k),
                                                                             i
                                                                             ))
                global_prec_at_n_first_mismatch_and_m_line.append(precision_at_k_first_mismatch_and_i_line)

            except Exception as e:
                print("No result")

            counter += 1
            if subgraph:
                sparqlQuery(graph, delete_triple())
            print(f"Computed in {time() - alpha} - remaining: {len(test_df.index) - counter}")

        except Exception as e:
            print(e)
            print(f"{original_taxon} {original_label}")
            print(get_sample_by_mismatch(sample, binding, 50, k))
            exit()

    with open(FILE_REPORT, "a") as file_report:
        result_precision_n_row = []
        result_precision_n_mismatch = []
        result_precision_n_first_mismatch = []
        result_precision_n_first_mismatch_m_line = []

        for k in range(0,49):
            prec_i = sum(map(lambda x: x[k][1], global_prec_at_n)) / len(global_prec_at_n)
            result_precision_n_row.append((k, prec_i))

        for k in range(0, 50):
            prec_i_mismatch = sum(map(lambda x: x[k][1], global_prec_at_mismatch)) / len(global_prec_at_mismatch)
            # moyenne des nombres de résultats
            moy_i_result = sum(map(lambda x: x[k][2], global_prec_at_mismatch)) / len(global_prec_at_mismatch)
            ecart_type = (sum(
                map(lambda x: (x[k][2] - moy_i_result)**2, global_prec_at_mismatch)) / len(global_prec_at_mismatch)
                          )**0.5
            result_precision_n_mismatch.append((k, prec_i_mismatch, moy_i_result, ecart_type))

        minimal_number_of_mismatch = min(list(map(lambda x: len(x), global_prec_at_n_first_mismatch)))
        for p in range(minimal_number_of_mismatch):
            prec_i_first_mismatch = sum(
                map(lambda x: x[p][1], global_prec_at_n_first_mismatch)) / len(global_prec_at_n_first_mismatch)
            result_precision_n_first_mismatch.append((p, prec_i_first_mismatch))


        for i in lines_check:
            only_i_result = list(map(lambda x : list(filter(lambda y : y[4] == i, x)),
                                     global_prec_at_n_first_mismatch_and_m_line))
            minimal_number_of_mismatch_for_n_line = min(list(
                map(lambda x: len(x), only_i_result)))
            for p in range(minimal_number_of_mismatch_for_n_line):
                sum_sample = sum(map(lambda x: x[p][1],only_i_result))
                prec_i_first_mismatch_n_line = sum_sample / len(only_i_result)
                result_precision_n_first_mismatch_m_line.append((p, prec_i_first_mismatch_n_line, i))

        file_report.write(f"## Precision at n first result: \n")
        line = '\n'.join([f'- {n + 1} row(s): precision {p}' for n,p in result_precision_n_row])
        file_report.write(f"{line}")

        file_report.write(f"\n\n## Precision at n mismatch: \n")
        file_report.write(f"| Mismatch | Precision | Average Nb of Row | Standard deviation |\n")
        file_report.write(f"|---|---|---|---|\n")
        line = '\n'.join([f'|{n}|{p:.4f}|{r:.4f}|{s:.4f}|' for n,p,r,s in result_precision_n_mismatch])
        file_report.write(f"{line}")

        file_report.write(f"\n\n## Precision at n first mismatch: (note: *it can be 0 mismatch*)\n")
        line = '\n'.join([f'- {n + 1} first mismatch: precision {p:.4f}' for n,p in result_precision_n_first_mismatch])
        file_report.write(f"{line}")

        file_report.write(
            f"\n\n## Precision at n first mismatch with limited result number: (note: *it can be 0 mismatch*)\n")
        file_report.write(
            f"| N-first mismatch/Number of line | {'|'.join(list(map(lambda x: str(x),lines_check)))} | \n")
        file_report.write(f"|{'---'} {'| --- '*len(lines_check)} | \n")
        for i in range(34):
            transform = [f"{elt[1]:.4f}" for elt in list(filter(lambda x: x[0] == i,
                                                                result_precision_n_first_mismatch_m_line))]
            file_report.write(f"| {i + 1} | {'|'.join(transform) } |\n")
