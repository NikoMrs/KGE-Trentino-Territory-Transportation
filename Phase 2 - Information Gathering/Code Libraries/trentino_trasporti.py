import os
import pandas as pd


def routes(folder):
    input_csv = f"../Datasets/raw datasets/{folder}/routes.txt"
    output_csv = f"../Datasets/cleaned datasets/{folder}/_routes.csv"

    # Loads the CSV files
    df = pd.read_csv(input_csv)

    to_remove = ["route_color", "route_text_color"]
    df = df.drop(columns=[column for column in to_remove if column in df.columns])

    # df.rename(columns={"route_id": "line_id"}, inplace=True)
    # df.rename(columns={"agency_id": "organization_id"}, inplace=True)
    # df.rename(columns={"route_short_name": "short_name"}, inplace=True)
    # df.rename(columns={"route_long_name": "long_name"}, inplace=True)
    # df.rename(columns={"route_type": "type"}, inplace=True)

    # Save in CSV format
    df.to_csv(output_csv, sep=';', index=False)
    print(f"File saved as {output_csv}")


def stops(folder):
    input_csv = f"../Datasets/raw datasets/{folder}/stops.txt"
    output_csv = f"../Datasets/cleaned datasets/{folder}/_stops.csv"

    # Loads the CSV files
    df = pd.read_csv(input_csv)

    # Remove columns
    to_remove = ["stop_code", "stop_desc", "zone_id"]
    df = df.drop(columns=[column for column in to_remove if column in df.columns])

    # TODO modificare?
    # Replace all empty field with the value 0 that means Not Available or Not Specified
    if folder == "Urbano":
        df['wheelchair_boarding'] = df['wheelchair_boarding'].replace("", 0).fillna(0)
    else:
        df["wheelchair_boarding"] = 0
    df['wheelchair_boarding'] = df['wheelchair_boarding'].astype(int)

    # df.rename(columns={"stop_lat": "latitude"}, inplace=True)
    # df.rename(columns={"stop_lon": "longitude"}, inplace=True)
    # df.rename(columns={"wheelchair_boarding": "wheelchair_accessible"}, inplace=True)
    # df.rename(columns={"stop_name": "name"}, inplace=True)

    # Save in CSV format
    df.to_csv(output_csv, sep=';', index=False)
    print(f"File saved as {output_csv}")

def extract_days(row):
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    return "["+ ', '.join([day for day, value in row.items() if value == 1]) + "]"

def calendar(folder):
    input_csv = f"../Datasets/raw datasets/{folder}/calendar.txt"
    output_csv = f"../Datasets/cleaned datasets/{folder}/_calendar.csv"

    # Loads the CSV files
    df = pd.read_csv(input_csv)

    df['byDay'] = df.apply(extract_days, axis=1)
    df = df[['service_id', 'byDay', 'start_date', 'end_date']]

    # Save in CSV format
    df.to_csv(output_csv, sep=';', index=False)
    print(f"File saved as {output_csv}")


def special_schedule(folder):
    input_csv = f"../Datasets/raw datasets/{folder}/calendar_dates.txt"
    output_csv = f"../Datasets/cleaned datasets/{folder}/_calendar_dates.csv"

    # Loads the CSV files
    df = pd.read_csv(input_csv)

    # df.rename(columns={
    #     "service_id": "special_schedule_id",
    #     "exception_type": "service_available",
    # }, inplace=True)

    # df["service_available"] = df["service_available"].replace({1: False, 2: True})

    # Save in CSV format
    df.to_csv(output_csv, sep=';', index=False)
    print(f"File saved as {output_csv}")


def trips(folder):
    input_csv = f"../Datasets/raw datasets/{folder}/trips.txt"
    output_csv = f"../Datasets/cleaned datasets/{folder}/_trips.csv"

    routes_csv = f"../Datasets/raw datasets/{folder}/routes.txt"

    # Loads the CSV files
    df = pd.read_csv(input_csv)
    routes_df = pd.read_csv(routes_csv)
    join = pd.merge(df, routes_df, on='route_id', how='left') 

    # Remove columns
    to_remove = ["shape_id"]
    df = df.drop(columns=[column for column in to_remove if column in df.columns])

    # df.rename(columns={
    #     "route_id": "line_id",
    #     "service_id": "schedule_id",
    #     "schedule_id": "schedule_id",
    #     "trip_headsign": "headsign",
    #     "direction_id": "direction",
    # }, inplace=True)
    # df["service_available"] = df["service_available"].replace({1: False, 2: True})

    # TODO modificare?
    # Replace all empty field with the value 0 that means Not Available or Not Specified
    df["bike_slots"] = 0
    if folder == "Urbano":
        df["wheelchair_accessible"] = df["wheelchair_accessible"].fillna(0)
    else:
        df["wheelchair_accessible"] = 0
        df.loc[join['route_type'] == 2, 'bike_slots'] = 6
        
    df["wheelchair_accessible"] = df["wheelchair_accessible"].astype(int)

    # Put the trip_id in the first column
    # df = df[['trip_id', 'line_id', 'schedule_id', 'headsign', 'direction', 'wheelchair_accessible']]
    df = df[['trip_id', 'route_id', 'service_id', 'trip_headsign', 'direction_id', 'wheelchair_accessible', 'bike_slots']]

    # Save in CSV format
    df.to_csv(output_csv, sep=';', index=False)
    print(f"File saved as {output_csv}")


def stop_times(folder):
    input_csv = f"../Datasets/raw datasets/{folder}/stop_times.txt"
    output_csv = f"../Datasets/cleaned datasets/{folder}/_stop_times.csv"

    # Loads the CSV files
    df = pd.read_csv(input_csv)

    # Reorder columns
    df = df[['trip_id', 'stop_id', 'arrival_time', 'departure_time', 'stop_sequence']]

    # Save in CSV format
    df.to_csv(output_csv, sep=';', index=False)
    print(f"File saved as {output_csv}")


def urbano():

    dir = "../Datasets/cleaned datasets/Urbano"

    if not os.path.exists(dir):
        os.makedirs(dir)

    routes("Urbano")
    stops("Urbano")
    calendar("Urbano")
    special_schedule("Urbano")
    trips("Urbano")
    stop_times("Urbano")


def extraurbano():

    dir = "../Datasets/cleaned datasets/Extraurbano"

    if not os.path.exists(dir):
        os.makedirs(dir)

    routes("Extraurbano")
    stops("Extraurbano")
    calendar("Extraurbano")
    special_schedule("Extraurbano")
    trips("Extraurbano")
    stop_times("Extraurbano")


if __name__ == '__main__':
    urbano()
    extraurbano()
