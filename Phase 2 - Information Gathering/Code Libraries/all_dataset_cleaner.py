import json
import pandas as pd
from pyproj import Proj, Transformer
import re
from shapely.wkt import loads, dumps
from shapely.geometry import Point, LineString
import pyproj
import os
from trentino_trasporti import urbano, extraurbano


def process_point(wkt):
    # Loads the Point
    point = loads(wkt)

    # Setup for position conversion
    transformer = Transformer.from_crs("EPSG:32632", "EPSG:4326", always_xy=True)

    # Convert the point to lat/lon
    lon, lat = transformer.transform(point.x, point.y)

    # Format the point with the Google Maps precision
    return f"{lat:.7f}", f"{lon:.7f}"


def process_linestring(wkt):
    proj_in = pyproj.CRS("EPSG:32632")
    proj_out = pyproj.CRS("EPSG:4326")

    # Loads the Linestring
    line = loads(wkt)

    # Remove duplicated points of the Linestring
    unique_points = list(dict.fromkeys(line.coords))

    # Compute the mean point
    x_coords, y_coords = zip(*unique_points)
    mean_x = sum(x_coords) / len(x_coords)
    mean_y = sum(y_coords) / len(y_coords)
    mean_point = Point(mean_x, mean_y)

    # Convert the mean Point in lat/lon
    transformer = pyproj.Transformer.from_crs(proj_in, proj_out, always_xy=True)
    lat, lon = transformer.transform(mean_point.x, mean_point.y)

    # Format the point with the Google Maps precision
    return f"{lat:.7f}", f"{lon:.7f}"


def bike_sharing():
    input_csv = "../Datasets/raw datasets/bike_sharing.csv"
    output_csv = "../Datasets/cleaned datasets/_bike_sharing.csv"

    # Setup for position conversion
    transformer = Transformer.from_crs("EPSG:32632", "EPSG:4326", always_xy=True)

    # Loads the CSV files
    df = pd.read_csv(input_csv, delimiter=';')

    df.rename(columns={
        "desc": "description",
        "cicloposteggi": "capacity",
    }, inplace=True)

    # Extracts lat/lon
    df['longitude'], df['latitude'] = transformer.transform(df['WKT'].str.extract(r'POINT \(([^ ]+) ([^ ]+)\)')[0], df['WKT'].str.extract(r'POINT \(([^ ]+) ([^ ]+)\)')[1])

    # Select only wanted columns
    df = df[['id', 'description', 'capacity', 'latitude', 'longitude']]

    # Save in CSV format
    df.to_csv(output_csv, sep=';', index=False)
    print(f"File saved as {output_csv}")


def scooter_sharing():
    input_csv = "../Datasets/raw datasets/monopattini_agevolata.csv"
    output_csv = "../Datasets/cleaned datasets/_monopattini_agevolata.csv"

    # Loads the CSV files
    df = pd.read_csv(input_csv, delimiter=';')

    # Extracts lat/lon
    df['latitude'], df['longitude'] = zip(*df['WKT'].apply(process_point))

    # Select only wanted columns
    df = df[['id', 'note', 'latitude', 'longitude']]

    # Save in CSV format
    df.to_csv(output_csv, sep=';', index=False)
    print(f"File saved as {output_csv}")


def taxi():
    input_csv = "../Datasets/raw datasets/taxi.csv"
    output_csv = "../Datasets/cleaned datasets/_taxi.csv"

    # Loads the CSV files
    df = pd.read_csv(input_csv, delimiter=';')

    df.rename(columns={
        "x": "latitude",
        "y": "longitude",
        "nome": "name",
    }, inplace=True)

    # Hand-crafted id
    df["id"] = pd.Series(range(1, df.size))

    # Select only wanted columns
    df = df[['id', 'name', 'latitude', 'longitude']]

    # Save in CSV format
    df.to_csv(output_csv, sep=';', index=False)
    print(f"File saved as {output_csv}")


def car_sharing():
    input_csv = "../Datasets/raw datasets/car_sharing.csv"
    output_csv = "../Datasets/cleaned datasets/_car_sharing.csv"

    # Loads the CSV files
    df = pd.read_csv(input_csv, delimiter=';')

    # Extracts lat/lon
    df['latitude'], df['longitude'] = zip(*df['WKT'].apply(process_point))
    df["description"] = df["via"].apply(lambda item: re.search(r'\((.*?)\)', item).group(1))

    df.rename(columns={
        "auto": "capacity",
    }, inplace=True)

    # Hand-crafted id
    df["id"] = pd.Series(range(1, df.size))

    # Select only wanted columns
    df = df[['id', 'description', 'capacity', 'latitude', 'longitude']]

    # Save in CSV format
    df.to_csv(output_csv, sep=';', index=False)
    print(f"File saved as {output_csv}")


def parking_facility():
    input_json = "../Datasets/raw datasets/parking.json"
    output_csv = "../Datasets/cleaned datasets/_parking_facility.csv"

    # Loads CSV from json
    f = open(input_json)
    data = json.load(f)
    df = pd.json_normalize(data["features"])

    # Extracts lat/lon
    df["longitude"] = df["geometry.coordinates"].apply(lambda x: x[0])
    df["latitude"] = df["geometry.coordinates"].apply(lambda x: x[1])

    df.rename(columns={
        "@id": "id",
        "properties.access": "access",
        "properties.capacity": "capacity",
        "properties.fee": "fee",
        "type": "something",
        "properties.parking": "type",
    }, inplace=True)

    df["capacity"] = df["capacity"].fillna(-1)
    df["type"] = df["type"].fillna("surface")
    df["access"] = df["access"].replace(to_replace="yes", value="public")
    df = df[df["access"] != "private"]
    df["fee"] = df["fee"].fillna("no")

    # Select only wanted columns
    df = df[["id", "access", "fee", "capacity", "type", "latitude", "longitude"]]

    # Save in CSV format
    df.to_csv(output_csv, sep=';', index=False)
    print(f"File saved as {output_csv}")


def bike_rack_1():
    input_json = "../Datasets/raw datasets/rastrelliere.csv"
    output_csv = "../Datasets/cleaned datasets/_rastrelliere.csv"

    # Loads the CSV files
    df = pd.read_csv(input_json, delimiter=";")

    # Extracts lat/lon
    df["longitude"], df["latitude"] = zip(*df['WKT'].apply(process_linestring))

    df.rename(columns={
        "tot_bici": "capacity",
        "Tipo_generale": "type",
    }, inplace=True)

    df["type"] = df["type"].apply(lambda x: x.split("_")[1])

    # Select only wanted columns
    df = df[["id", "type", "capacity", "latitude", "longitude"]]

    # Save in CSV format
    df.to_csv(output_csv, sep=';', index=False)
    print(f"File saved as {output_csv}")


def bike_rack_2():
    input_json = "../Datasets/raw datasets/parcheggio_protetto_bike.csv"
    output_csv = "../Datasets/cleaned datasets/_parcheggio_protetto_bike.csv"

    # Loads the CSV files
    df = pd.read_csv(input_json, delimiter=";")

    # Extracts lat/lon
    df["latitude"], df["longitude"] = zip(*df['WKT'].apply(process_point))

    df.rename(columns={
        "posti": "capacity",
    }, inplace=True)

    # Hand-crafted id
    df["id"] = pd.Series(range(1, df.size))
    df["type"] = "guarded"

    # Select only wanted columns
    df = df[["id", "type", "capacity", "latitude", "longitude"]]

    # Save in CSV format
    df.to_csv(output_csv, sep=';', index=False)
    print(f"File saved as {output_csv}")


def bike_rack_3():
    input_json = "../Datasets/raw datasets/centro_in_bici.csv"
    output_csv = "../Datasets/cleaned datasets/_centro_in_bici.csv"

    # Loads the CSV files
    df = pd.read_csv(input_json, delimiter=";")

    # Extracts lat/lon
    df["latitude"], df["longitude"] = zip(*df['WKT'].apply(process_point))

    df.rename(columns={
        "cicloposteggi": "capacity",
    }, inplace=True)

    # Hand-crafted id
    df["id"] = pd.Series(range(1, df.size))

    # Select only wanted columns
    df = df[["id", "capacity", "latitude", "longitude"]]

    # Save in CSV format
    df.to_csv(output_csv, sep=';', index=False)
    print(f"File saved as {output_csv}")


if __name__ == '__main__':

    dir = "../Datasets/cleaned datasets"

    if not os.path.exists(dir):
        os.makedirs(dir)

    bike_sharing()
    scooter_sharing()
    taxi()
    car_sharing()
    parking_facility()
    bike_rack_1()
    bike_rack_2()
    bike_rack_3()

    print("\nTrentino trasporti Urbano...")
    urbano()

    print("\nTrentino trasporti Extraurbano...")
    extraurbano()


