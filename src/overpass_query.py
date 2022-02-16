"""
Execute an overpass query and save the result in geojson

2022, Nicolas Grosjean, worked during the Grenoble CivicLab

Licensed under the Apache License, Version 2.0 (the « License »); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an « AS IS » BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
"""

import argparse
import json
import requests


OVERPASS_ENDPOINT = "http://overpass-api.de/api/interpreter"


def get_args():
    parser = argparse.ArgumentParser(
        description="Execute an overpass query and save the result in geojson"
    )
    parser.add_argument(
        "query_path", type=str, help="Path of the file containing the query to execute"
    )
    parser.add_argument(
        "output_path",
        type=str,
        help="Path of the file containing the result of the query",
    )
    return parser.parse_args()


def main(query_path: str, output_path: str):
    with open(query_path, "r") as f:
        query_lines = f.readlines()
    query = ""
    for query_line in query_lines:
        i = 0
        while query_line[i] == " " or query_line[i] == "\t":
            i += 1
        compressed_query_line = query_line[i:].replace("\n", "")
        if not compressed_query_line.startswith("//"):
            query += compressed_query_line
    r = requests.get(OVERPASS_ENDPOINT, {"data": query})
    with open(output_path, "w") as outfile:
        json.dump(r.json(), outfile, indent=2)


if __name__ == "__main__":
    args = get_args()
    main(args.query_path, args.output_path)
