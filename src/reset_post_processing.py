"""
Execute a post processing own to Reset Mode d'emploi

2022, Nicolas Grosjean, worked during the Grenoble CivicLab

Licensed under the Apache License, Version 2.0 (the « License »); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an « AS IS » BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
"""

import argparse
import pandas as pd

OUTPUT_COLUMNS = [
    "name",
    "Nom structure",
    "Sites",
    "alt_name",
    "description",
    "Objets",
    "Action",
    "repair_oneself",
    "repair_pro",
    "sell",
    "give",
    "opening_hours",
    "Adresse",
    "addr:housenumber",
    "addr:housename",
    "addr:street",
    "addr:city",
    "addr:postcode",
    "contact:website",
    "website",
    "Site Web",
    "contact:phone",
    "phone",
    "contact:email",
    "email",
    "contact:facebook",
    "wheelchair",
    "lat",
    "Latitude",
    "lon",
    "Longitude",
    "type",
    "id"
]


def get_args():
    parser = argparse.ArgumentParser(
        description="Execute a post processing own to Reset Mode d'emploi"
    )
    parser.add_argument(
        "-input_path",
        type=str,
        help="Path of the file in which post processing will be applied",
        default="data/merge.csv",
    )
    parser.add_argument(
        "-output_path",
        type=str,
        help="Path of the pipeline result",
        default="data/merge.csv",
    )
    return parser.parse_args()


def reset_post_processing(input_path: str, output_path: str):
    df = pd.read_csv(input_path, encoding="utf-8")

    # Add objects which can be repaired by oneself
    df["repair_oneself"] = ""
    df.loc[df["service:bicycle:diy"] == "yes", "repair_oneself"] = "bicycle"
    df.loc[df["repair"] == "assisted_self_service", "repair_oneself"] = "electronics"

    # Add objects which can be repaired by professionnal
    df["repair_pro"] = ""
    df.loc[df["service:bicycle:repair"] == "yes", "repair_pro"] = "bicycle"

    # Add objects which can be sold
    df["sell"] = ""
    df.loc[df["shop"] == "second_hand", "sell"] = "yes"
    df.loc[df["second_hand"] == "yes", "sell"] = "yes"
    df.loc[
        (df["service:bicycle:second_hand"] == "yes") & (~pd.isnull(df["shop"])), "sell"
    ] = "bicycle"

    # Add objects which can be given
    df["give"] = ""
    df.loc[df["shop"] == "charity", "give"] = "yes"
    df.loc[df["service:bicycle:second_hand"] == "yes", "give"] = "bicycle"
    df.loc[df["amenity"] == "public_bookcase", "give"] = "book"

    # Export according defined columns
    df[OUTPUT_COLUMNS].to_csv(output_path, index=None, encoding="utf-8")


if __name__ == "__main__":
    args = get_args()
    reset_post_processing(args.input_path, args.output_path)
