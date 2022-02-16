"""
Convert the result of an overpass query with "out center" from GeoJSON to CSV

2022, Nicolas Grosjean, worked during the Grenoble CivicLab

Licensed under the Apache License, Version 2.0 (the « License »); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an « AS IS » BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
"""

import argparse
import json
import numpy as np
import pandas as pd

FIRST_TAGS = [
    "service:bicycle:diy",
    "service:bicycle:repair",
    "service:bicycle:second_hand",
    "shop",
    "repair",
]


def get_args():
    parser = argparse.ArgumentParser(
        description="Convert the OSM GeoJSON input file into CSV"
    )
    parser.add_argument("input_file", type=str, help="Path of the file to convert")
    return parser.parse_args()


def main(input: str):
    # Read geojson file
    with open(input, "r", encoding="utf-8") as f:
        data = json.load(f)

    # List and order the tags
    tag_occurences = dict()
    for element in data["elements"]:
        for tag in element["tags"].keys():
            if tag in FIRST_TAGS:
                # Some tags will be first
                continue
            if tag in tag_occurences:
                tag_occurences[tag] += 1
            else:
                tag_occurences[tag] = 1
    sorted_tags = [e[0] for e in sorted(tag_occurences.items(), key=lambda x: -x[1])]
    sorted_tags.insert(1, "lat")
    sorted_tags.insert(2, "lon")
    for i in range(len(FIRST_TAGS)):
        sorted_tags.insert(i + 3, FIRST_TAGS[i])

    # Store data in dataframe
    df = pd.DataFrame(columns=sorted_tags, index=np.arange(len(data["elements"])))
    for i in range(len(data["elements"])):
        element = data["elements"][i]

        # Store tags
        for tag, value in element["tags"].items():
            df.loc[i, tag] = value

        # Store coordinates
        if element["type"] == "node":
            geo = element
        else:
            geo = element["center"]
        df.loc[i, "lat"] = geo["lat"]
        df.loc[i, "lon"] = geo["lon"]

        # Store type and id
        df.loc[i, "type"] = element["type"]
        df.loc[i, "id"] = element["id"]

        # TODO Query Nominatim to get adress if necessary

    # Export data to CSV
    df.to_csv(input.replace(".geojson", ".csv"), index=None, encoding="utf-8")


if __name__ == "__main__":
    args = get_args()
    main(args.input_file)
