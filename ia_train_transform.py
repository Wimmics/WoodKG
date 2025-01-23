import pandas as pd
import numpy as np
import pymongo


def dataframe_transform(df, collection):
    data = []

    for row in df.index:
        sample_id = df["id_sample"][row]
        accepted_id = df["accepted_id"][row]

        for feature in df.columns[8:]:
            feature_value = f"IFC-{feature}"
            if int(df[feature][row]) == 0:
                continue
            feature_presence = feature_values[int(df[feature][row])]
            data.append([sample_id, accepted_id, "WoodKG", "", feature_value, feature_presence, "", ""])
            collection.insert_one({"sample_id": sample_id,
                               "accepted_id": accepted_id,
                               "collection": "WoodKG",
                               "observed_property": "",
                               "feature_value": feature_value,
                               "feature_presence": feature_presence,
                               "FOI": "",
                               "original_data": ""})

    return data

def extract_taxonomy(df, collection):
    data = []

    for row in df.index:
        accepted_id = df["accepted_id"][row]
        family = df["powo_family"][row]
        genus = df["powo_genus"][row]
        taxa = df["powo_taxon"][row]
        collection.insert_one({
            "plant_name_id": accepted_id,
            "family": family,
            "genus": genus,
            "species": taxa,
            "taxon_name": taxa
        })
        data.append([accepted_id, family, genus, taxa, taxa])

    return data


if __name__ == "__main__":

    mongoDB = pymongo.MongoClient("mongodb://localhost:27017/")
    charcoalDB = mongoDB["Charcoal"]

    letters = ["A", "B", "C", "D"]
    types = ["family","genus"]
    DIR_PATH = "export_train_test/export_"
    feature_values = {3: "IFV-2", 2: "IFV-3", 1: "IFV-4", 0: ""}
    label = ["sample_id", "taxon_id", "collection", "observed_property", "feature_value", "feature_presence", "FOI", "original_data"]

    for letter in letters:
        for t in types:
            df = pd.read_csv(f"{DIR_PATH}{letter}/export_train_powo_{t}.csv", header=0, sep=";")
            data_feature = dataframe_transform(df, charcoalDB[f"Observation_{letter}_{t}"])
            pd.DataFrame(data_feature, columns=label).to_csv(f"feature_region{letter}_{t}.csv", encoding="utf-8", index=False, sep=";")
            data_taxonomy = extract_taxonomy(df, charcoalDB[f"Taxonomy_{letter}_{t}"])
            pd.DataFrame(data_taxonomy,
                         columns=["plant_name_id", "family", "genus", "species", "taxon_name"]
                         ).to_csv(f"taxonomy_region{letter}_{t}.csv", encoding="utf-8", index=False, sep=";")



