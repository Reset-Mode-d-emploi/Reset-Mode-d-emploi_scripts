# Scripts for Reset Mode d'emploi

> Various scripts to get and process data for the project Reset Mode d'emploi 

**N.B**: overpass_query, geojson_to_csv, csv_to_json and conflate scripts are designed to be generic,
so they can be used for other projects than Reset Mode d'emploi

## Installation

I recommend you to install a Python environment with conda, virtualenv or pipenv.

### With Conda
For example with conda, 
[download and install miniconda](https://docs.conda.io/en/latest/miniconda.html)

Create a conda environment

```
conda create -n reset_mode_emploi python
```

Activate the conda environment

```
activate reset_mode_emploi
```

OR according your operating system

```
conda activate reset_mode_emploi
```

Install the requirement packages

```
pip install -r requirements.txt
```

## Usage

For each script, you have a running example in [.vscode/launch.json](.vscode/launch.json) and you can it with the following command to get the documentation

```
python src/<script>.py -h
```

The pipeline run overpass_query, then geojson_to_csv and finally conflate scripts.


## License

The project has an [Apache-2.0 License](LICENSE).
