import pandas as pd
import click
from pathlib import Path


@click.command(context_settings={'show_default': True})
@click.version_option()
@click.option(
    "-i",
    "--input",
    type=click.Path(exists=True, file_okay=True, dir_okay=False, path_type=Path),
    help="Path to input file from mmseqs or blast to filter.",
)
@click.option(
    "-o",
    "--output",
    type=click.Path(exists=False, file_okay=True, dir_okay=False, path_type=Path),
    help="Output file to save to.",
)
@click.option(
    "-n",
    "--num-hits",
    type=int,
    default=100,
    help="Number of hits to retain per sequence.",
)
@click.option(
    "-b", "--bitscore", type=int, default=300, help="Minimum bit-score to filter hits."
)
@click.option(
    "-qcol", "--qseqid-col", type=int, default=1, help="Query sequence ID column."
)
@click.option("-bcol", "--bitscore-col", type=int, default=-1, help="Bitscore column.")
def main(
    input: Path,
    output: Path,
    num_hits: int,
    bitscore: int,
    qseqid_col: int,
    bitscore_col: int,
):
    """Filter hits from mmseqs (BLAST-style) or BLAST output based on bit-score
    and number of hits per query sequence. This will retain the top n hits
    (based on bitscore) per query sequence with a bit-score above the specified
    threshold."""
    filter_hits(input, num_hits, bitscore, qseqid_col, bitscore_col).to_csv(
        output, sep="\t", header=False, index=False
    )


def filter_hits(
    input: Path,
    num_hits: int,
    bitscore: int,
    qseqid_col: int = 1,
    bitscore_col: int = -1,
):
    qseqid_col -= 1  # Convert to 0-indexed
    # Read the input file
    df = pd.read_csv(input, sep="\t", header=None)

    # Assuming the bit-score is in column 11 (0-indexed 10)
    df = df.loc[df.iloc[:, bitscore_col] >= bitscore]

    df = (
        (
            df.sort_values(df.columns[bitscore_col], ascending=False)
            .groupby(df.columns[qseqid_col], group_keys=False)
            .head(num_hits)
        )
        .sort_index()
        .reset_index(drop=True)
    )

    return df


if __name__ == "__main__":
    main()
