"""
Convert a CSV file to a JSON file

2022, Nicolas Grosjean, worked during the Grenoble CivicLab

Licensed under the Apache License, Version 2.0 (the « License »); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an « AS IS » BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
"""

import argparse
import pandas as pd


def get_args():
    parser = argparse.ArgumentParser(description="Convert a CSV file to a JSON file")
    parser.add_argument("input_file", type=str, help="Path of the file to convert")
    parser.add_argument(
        "-output_file",
        type=str,
        help="Path of the result. Default is the input file with .csv replaced by .json",
    )
    return parser.parse_args()


def csv_to_json(input_file: str, output_file: str = None):
    new_output_file = output_file
    if new_output_file is None:
        new_output_file = input_file.replace(".json", ".csv")
    df = pd.read_csv(input_file)
    df.to_json(new_output_file, orient="records")


if __name__ == "__main__":
    args = get_args()
    csv_to_json(args.input_file, args.output_file)
