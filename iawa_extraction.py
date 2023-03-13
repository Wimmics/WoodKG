import pandas as pd
import re
import time

label = ["family", "genus", "species", "taxon", "author", "status", "accepted_id", "plant_id", "continent", "region", "area"]

errors_label = ["taxon", "line"]
errors = []

def extract_iawa_information(row):
    family = ""
    original_string = df_iawa["Taxa"][row].replace("?", "")
    #print(original_string)
    for x in original_string.split("|"):
        x = x.replace("Synonym:", "")
        # family = re.search("(PRIMULACEAE|LEGUMINOSAE|MALVACEAE)*\s[A-Z][A-Z]+", original_string).group(0)
        family = re.search("[A-Z][A-Z]+\s[A-Z][A-Z]+|[A-Z][A-Z]+", x).group(0)
        genre = re.search("[A-Z][a-z]+\s[a-z]+|[A-Z][a-z]+", x).group(0)
        if re.search("\([A-Z][A-Z,\s]+\)", x):
            usual_name = re.search("\([A-Z][A-Z,\s]+\)", x).group(0)
        else:
            usual_name = ""
        return family, genre, usual_name, original_string



def get_id_by_taxon(taxon,df1,df2, org_str):
    matches = [" spp", " sp.", " spp.", " SPP", " SPP.", " SP.",  " group"]
    taxon = taxon.replace(" cf ", " ")
    category = "taxon_name"
    if any([x in taxon for x in matches]):
        for x in matches:
            taxon = taxon.replace(x, "")
        category = "genus"

    test1 = df1[df1[category].values == taxon.strip()]['accepted_plant_name_id'].tolist()
    test2 = df2[df2[category].values == taxon.strip()]['accepted_plant_name_id'].tolist()
    if not test1 and not test2:
        errors.append([taxon, org_str])
        return None
    if not test1:
        return test2[0]
    return test1[0]

def get_plantId_by_acceptedId(accepted_id, df1,df2):
    pass

def get_geolocalisation_by_id():
    pass

if __name__ == "__main__":
    # IAWA_Afrique_net
    print("Loading Dataframe...")
    alpha = time.time()
    df_iawa = pd.read_excel("IAWA_Africa_modernOnly.xlsx", sheet_name="IAWA_Afrique_net_modern", header=2)
    df_powoAP = pd.read_excel("wcvp_taxon_distri_anatomy_net.xlsx", sheet_name="Acan-Plum")
    df_powoPZ = pd.read_excel("wcvp_taxon_distri_anatomy_net.xlsx", sheet_name="Poac-Zigo")
    #df_dist1 = pd.read_excel("wcvp_taxon_distri_anatomy_net.xlsx", sheet_name="Distribution1_net")
    #df_dist2 = pd.read_excel("wcvp_taxon_distri_anatomy_net.xlsx", sheet_name="Distribution2_net")
    df_cepam = pd.read_excel("CEPAM_feature_net.xlsx", sheet_name="CEPAM")
    print(f"Dataframes loading time : {time.time() - alpha} seconds")

    extract_family = []
    extract_genre = []
    extract_usual_name = []

    print("Starting extraction")

    for row in df_iawa.index:
        family, genre, usual_name, original_string = extract_iawa_information(row)
        accepted_id = get_id_by_taxon(genre, df_powoAP, df_powoPZ, original_string)
        #print(accepted_id)

    print(errors)
    pd.DataFrame(errors, columns=errors_label).to_csv("errors.csv", index=False, encoding="utf-8")

    #print(to_extract)