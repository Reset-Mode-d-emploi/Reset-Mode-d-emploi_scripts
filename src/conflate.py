"""
Merge 2 dataset according geographical coordinates

2022, Nicolas Grosjean, worked during the Grenoble CivicLab

Licensed under the Apache License, Version 2.0 (the « License »); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an « AS IS » BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
"""

import argparse
from haversine import haversine
from typing import List
import pandas as pd

POSSIBLE_LAT_COL_NAME = ["Latitude", "latitude", "lat", "Lat"]
POSSIBLE_LON_COL_NAME = ["Longitude", "longitude", "lon", "Lon"]
POSSIBLE_NAME_COL_NAME = ["Name", "name", "Nom structure"]


def get_args():
    parser = argparse.ArgumentParser(
        description="Merge 2 dataset according geographical coordinates"
    )
    parser.add_argument("data1_path", type=str, help="Path of the first date CSV file")
    parser.add_argument("data2_path", type=str, help="Path of the second date CSV file")
    parser.add_argument(
        "-tol", type=int, help="Tolerance for merging in meters", default=80
    )
    parser.add_argument(
        "-output_path",
        type=str,
        help="Path of the merge result",
        default="data/merge.csv",
    )
    return parser.parse_args()


def get_column_names(columns: List[str], values_to_test: List[str]):
    """
    Test one by one values from values_to_test and return the first found in columns
    """
    for value in values_to_test:
        if value in columns:
            return value
    raise Exception(f"No values in {values_to_test} are in {columns}")


def conflate(data1_path: str, data2_path: str, tol: int, output_path: str):
    # Read data
    data1 = pd.read_csv(data1_path)
    lat_col_name_1 = get_column_names(data1.columns, POSSIBLE_LAT_COL_NAME)
    lon_col_name_1 = get_column_names(data1.columns, POSSIBLE_LON_COL_NAME)
    name_col_name_1 = get_column_names(data1.columns, POSSIBLE_NAME_COL_NAME)
    data2 = pd.read_csv(data2_path)
    lat_col_name_2 = get_column_names(data2.columns, POSSIBLE_LAT_COL_NAME)
    lon_col_name_2 = get_column_names(data2.columns, POSSIBLE_LON_COL_NAME)
    data2["coords"] = [
        tuple(coord) for coord in data2[[lat_col_name_2, lon_col_name_2]].values
    ]

    # Compute distance and get merged data according tolerance
    res = pd.DataFrame()
    not_found_ids = []
    data2_ids_inner = set()
    data1["dist"] = -1
    for i in range(len(data1)):
        if pd.isnull(data1.iloc[i][lat_col_name_1]) or pd.isnull(
            data1.iloc[i][lon_col_name_1]
        ):
            not_found_ids.append(i)
            print(
                f"No coordinates for {data1.iloc[i][name_col_name_1]} in first dataset"
            )
            continue
        coord1 = tuple(data1.iloc[i][[lat_col_name_1, lon_col_name_1]])
        dist_km = data2["coords"].apply(lambda coord2: haversine(coord1, coord2))
        if dist_km.min() < tol / 1000:
            data1.loc[i, "dist"] = dist_km.min()
            data2_id = dist_km.argmin()
            data2_ids_inner.add(data2_id)
            new_line = pd.concat([data1.iloc[i], data2.iloc[data2_id]], axis=0)
            res = pd.concat([res, new_line], axis=1, ignore_index=True)
        else:
            not_found_ids.append(i)

    # Add data1 not found to res
    for i in not_found_ids:
        new_line = pd.concat(
            [data1.iloc[i], pd.Series([""] * len(data2.columns))], axis=0
        )
        res = pd.concat([res, new_line], axis=1, ignore_index=True)

    # Add data2 not found to res
    for i in range(len(data2)):
        if i not in data2_ids_inner:
            new_line = pd.concat(
                [pd.Series([""] * len(data1.columns)), data2.iloc[i]], axis=0
            )
            res = pd.concat([res, new_line], axis=1, ignore_index=True)

    # Export result
    res.transpose().to_csv(output_path, index=None, encoding="utf-8")


if __name__ == "__main__":
    args = get_args()
    conflate(args.data1_path, args.data2_path, args.tol, args.output_path)
