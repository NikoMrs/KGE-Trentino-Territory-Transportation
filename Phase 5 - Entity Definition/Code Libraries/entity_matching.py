import os
import pandas as pd


def merge_datasets():
    dir = "../Datasets/cleaned datasets/trentino_trasporti"

    if not os.path.exists(dir):
        os.makedirs(dir)

    urbano_dirs = [
        "../../Phase 2 - Information Gathering/Datasets/cleaned datasets/Urbano/_stop_times.csv",
        "../../Phase 2 - Information Gathering/Datasets/cleaned datasets/Urbano/_calendar.csv",
        "../../Phase 2 - Information Gathering/Datasets/cleaned datasets/Urbano/_stops.csv",
        "../../Phase 2 - Information Gathering/Datasets/cleaned datasets/Urbano/_calendar_dates.csv",
        "../../Phase 2 - Information Gathering/Datasets/cleaned datasets/Urbano/_trips.csv",
        "../../Phase 2 - Information Gathering/Datasets/cleaned datasets/Urbano/_routes.csv",
    ]

    extraurbano_dirs = [
        "../../Phase 2 - Information Gathering/Datasets/cleaned datasets/Extraurbano/_stop_times.csv",
        "../../Phase 2 - Information Gathering/Datasets/cleaned datasets/Extraurbano/_calendar.csv",
        "../../Phase 2 - Information Gathering/Datasets/cleaned datasets/Extraurbano/_stops.csv",
        "../../Phase 2 - Information Gathering/Datasets/cleaned datasets/Extraurbano/_calendar_dates.csv",
        "../../Phase 2 - Information Gathering/Datasets/cleaned datasets/Extraurbano/_trips.csv",
        "../../Phase 2 - Information Gathering/Datasets/cleaned datasets/Extraurbano/_routes.csv",
    ]

    output_dirs = [
        "../Datasets/cleaned datasets/trentino_trasporti/stop_events.csv",
        "../Datasets/cleaned datasets/trentino_trasporti/transportation_schedules.csv",
        "../Datasets/cleaned datasets/trentino_trasporti/stops.csv",
        "../Datasets/cleaned datasets/trentino_trasporti/transportation_special_schedules.csv",
        "../Datasets/cleaned datasets/trentino_trasporti/trips.csv",
        "../Datasets/cleaned datasets/trentino_trasporti/transportation_lines.csv",
    ]

    idx = 0
    for dir in extraurbano_dirs:
        extraurbano = pd.read_csv(dir, delimiter=";")
        urbano = pd.read_csv(urbano_dirs[idx], delimiter=";")
        if "stop" in dir:
            extraurbano["stop_id"] = extraurbano["stop_id"].apply(lambda x: "e_" + str(x)) 
            urbano["stop_id"] = urbano["stop_id"].apply(lambda x: "u_" + str(x)) 
        merge = pd.concat([urbano, extraurbano], ignore_index=True)
        merge.to_csv(output_dirs[idx], sep=";", index=False)
        idx+=1


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

    s1.to_csv("../Datasets/cleaned datasets/bike_parking.csv", sep=";", index=False)
    

if __name__ == '__main__':
    merge_datasets()
    bike_sharng_conflict()
    bike_parking_conflict()
