# Filter hits from mmseqs or BLAST output

This script filters hits from mmseqs (BLAST-style) or BLAST output based on bit-score and number of hits per query sequence. This will retain the top n hits (based on bitscore) per  sequence with a bit-score above the specified threshold.

## Install

Install the conda environment from the main environment file if the environment is not already installed:

```
curl -o environment.yml https://raw.githubusercontent.com/WrightonLabCSU/server-scripts/refs/heads/main/environment.yaml
conda env create -f environment.yaml
conda activate server_scripts # Don't forget this step
```

If the environment is already installed, you can update it with:

```
curl -o environment.yml https://raw.githubusercontent.com/WrightonLabCSU/server-scripts/refs/heads/main/environment.yaml
conda env update -f environment.yaml --prune
conda activate server_scripts # Don't forget this step
```

optionally delete the environment file:

```
rm environment.yml
```


Install filter_hits from GitHub:
```
pip install "git+https://github.com/WrightonLabCSU/server-scripts.git@main#subdirectory=filter_hits"
```

## Use

First use `--help` to see all options. You can filter based on a minimum bitscore,
and take the top n hits per query sequence, as well as specify what column contains bitscorew and query sequence ID.

Example usage:

```
filter_hits -i <INPUT> -o <OUTDIR> -n <NUM-HITS> -b <BITSCORE>
```