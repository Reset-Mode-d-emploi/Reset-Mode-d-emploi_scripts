"""
Execute the full pipeline of data getting and processing

2022, Nicolas Grosjean, worked during the Grenoble CivicLab

Licensed under the Apache License, Version 2.0 (the « License »); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an « AS IS » BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
"""

import argparse
import datetime
import os

from conflate import conflate
from geojson_to_csv import geojson_to_csv
from overpass_query import overpass_query


def get_args():
    parser = argparse.ArgumentParser(
        description="Execute the full pipeline of data getting and processing"
    )
    parser.add_argument(
        "query_path",
        type=str,
        help="Path of the file containing the overpass query to execute",
    )
    parser.add_argument(
        "data_path",
        type=str,
        help="Path of the CSV file which will be conflated to get data",
    )
    parser.add_argument(
        "-filter_file",
        type=str,
        help="Path of the file containing at each line a column to keep according wanted order",
    )
    parser.add_argument(
        "-tol", type=int, help="Tolerance for merging in meters", default=80
    )
    parser.add_argument(
        "-output_path",
        type=str,
        help="Path of the pipeline result",
        default="data/merge.csv",
    )
    return parser.parse_args()


def pipeline(
    query_path: str, data_path: str, filter_file: str, tol: int, output_path: str
):
    str_date = datetime.datetime.strftime(datetime.datetime.now(), "%Y_%m_%d")
    geojson_path = os.path.join("data", f"res_{str_date}.geojson")
    csv_path = os.path.join("data", f"res_{str_date}.csv")
    overpass_query(query_path, geojson_path)
    geojson_to_csv(geojson_path, filter_file)
    conflate(data_path, csv_path, tol, output_path)


if __name__ == "__main__":
    args = get_args()
    pipeline(
        args.query_path, args.data_path, args.filter_file, args.tol, args.output_path
    )
