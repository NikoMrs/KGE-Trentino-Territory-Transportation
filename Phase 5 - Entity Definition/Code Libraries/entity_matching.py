import os
import pandas as pd


def merge_datasets():
    dir = "../Datasets/cleaned datasets/trentino_trasporti"

    if not os.path.exists(dir):
        os.makedirs(dir)

    for filename in os.listdir("../../Phase 2 - Information Gathering/Datasets/cleaned datasets/Extraurbano"):
        extraurbano = pd.read_csv(f"../../Phase 2 - Information Gathering/Datasets/cleaned datasets/Extraurbano/{filename}", delimiter=";")
        urbano = pd.read_csv(f"../../Phase 2 - Information Gathering/Datasets/cleaned datasets/Urbano/{filename}", delimiter=";")
        merge = pd.concat([urbano, extraurbano], ignore_index=True)
        merge.to_csv(f"../Datasets/cleaned datasets/trentino_trasporti/{filename}", sep=";", index=False)


def is_row_present(row, df, tolerance):
    return ((abs(df['latitude'] - row['latitude']) <= tolerance) & 
            (abs(df['longitude'] - row['longitude']) <= tolerance)).any()

def bike_sharng_conflict():
    TOLERANCE = 0.00005 

    source_1 = "../../Phase 2 - Information Gathering/Datasets/cleaned datasets/_bike_sharing.csv"
    source_2 = "../../Phase 2 - Information Gathering/Datasets/cleaned datasets/_centro_in_bici.csv"

    s1 = pd.read_csv(source_1, delimiter=";")
    s2 = pd.read_csv(source_2, delimiter=";")
    
    for _, row in s2.iterrows():
        if not is_row_present(row, s1, TOLERANCE):
            row["id"] = str(row["id"]) + "/centro"
            s1 = pd.concat([s1, pd.DataFrame([row])], ignore_index=True)
        else:
            print(row["id"])

    s1.to_csv("../Datasets/cleaned datasets/bike_sharing.csv", sep=";", index=False)

def bike_parking_conflict():
    TOLERANCE = 0.00005 

    source_1 = "../../Phase 2 - Information Gathering/Datasets/cleaned datasets/_rastrelliere.csv"
    source_2 = "../../Phase 2 - Information Gathering/Datasets/cleaned datasets/_parcheggio_protetto_bike.csv"

    s1 = pd.read_csv(source_1, delimiter=";")
    s2 = pd.read_csv(source_2, delimiter=";")
    
    for _, row in s2.iterrows():
        if not is_row_present(row, s1, TOLERANCE):
            row["id"] = str(row["id"]) + "/protetto"
            s1 = pd.concat([s1, pd.DataFrame([row])], ignore_index=True)
        else:
            print(row["id"])

    s1.to_csv("../Datasets/cleaned datasets/bicycle_parking.csv", sep=";", index=False)
    

if __name__ == '__main__':
    merge_datasets()
    bike_sharng_conflict()
    bike_parking_conflict()
