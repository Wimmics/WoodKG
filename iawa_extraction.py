import pandas as pd
import re

label = ["family", "genus", "species", "taxon", "author", "status", "accepted_id", "plant_id", "continent", "region", "area"]

if __name__ == "__main__":
    # IAWA_Afrique_net
    df_iawa = pd.read_excel("wcvp_taxon_distri_anatomy_net.xlsx", sheet_name="IAWA_Afrique_net")
    print(df_iawa)

    extract_family = []
    extract_genre = []
    extract_usual_name = []

    for row in df_iawa.index:
        family = ""
        original_string = df_iawa["Taxa"][row].replace("?","")
        print(original_string)
        for x in original_string.split("|"):
            x = x.replace("Synonym:","")
            #family = re.search("(PRIMULACEAE|LEGUMINOSAE|MALVACEAE)*\s[A-Z][A-Z]+", original_string).group(0)
            family = re.search("[A-Z][A-Z]+\s[A-Z][A-Z]+|[A-Z][A-Z]+", x).group(0)
            genre = re.search("[A-Z][a-z]+\s[a-z]+|[A-Z][a-z]+", x).group(0)
            if re.search("\([A-Z][A-Z,\s]+\)", x):
                usual_name = re.search("\([A-Z][A-Z,\s]+\)", x).group(0)
            else:
                usual_name = ""

            extract_family.append(family)
            extract_genre.append(genre)
            extract_usual_name.append(usual_name)

    extract_family = list(set(extract_family))
    extract_genre = list(set(extract_genre))
    print(f"Nombre de famille : {len(extract_family)}\nList: {extract_family}")
    print(f"Nombre de genre : {len(extract_genre)}\nList: {extract_genre}")
    print(f"Nombre d'author : {len(extract_usual_name)}\nList: {extract_usual_name}")

    #print(to_extract)