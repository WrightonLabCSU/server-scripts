import pandas as pd
import io
import shlex
import os
from pathlib import Path
from filter_hits.__main__ import filter_hits


IS_WINDOWS = os.name == "nt"

def split_shell_command(cmd: str):
    """
    split shell command for passing to python subproccess.
    This should correctly split commands like "echo 'Hello, World!'"
    to ['echo', 'Hello, World!'] (2 items) and not ['echo', "'Hello,", "World!'"] (3 items)

    It also works for posix and windows systems appropriately
    """
    return shlex.split(cmd, posix=not IS_WINDOWS)

def test_main_function():
    input_file = Path(__file__).parent / "data/mmseqs_test.m8"
    num_hits = 5
    bitscore = 300

    filtered_df = filter_hits(
        input=input_file,
        bitscore=bitscore,
        num_hits=num_hits
    )

    # Expected output data
    expected_data = """seq1      prot001     99.12   302     2         0        1       302   5       306   1.2e-120  602.5
seq1      prot002     97.88   300     4         1        2       301   7       306   2.5e-118  597.0
seq1      prot003     96.55   295     5         0        1       295   12      306   4.1e-115  585.4
seq1      prot004     95.00   280     8         1        3       282   15      296   9.7e-110  565.2
seq1      prot005     90.33   250     15        2        10      259   20      269   5.5e-100  540.7
seq2      prot020     98.22   310     3         0        1       310   2       311   3.6e-125  620.1
seq2      prot021     92.44   298     10        1        4       301   10      307   5.1e-105  545.9
seq2      prot022     88.00   285     18        1        6       291   8       298   2.4e-95   505.7
seq3      prot030     99.80   280     1         0        1       280   4       283   2.2e-110  575.3
seq3      prot031     98.55   278     3         0        1       278   5       282   1.0e-108  570.0
seq3      prot032     97.42   275     4         1        3       277   6       281   7.2e-107  560.2
seq3      prot033     95.33   270     8         1        5       274   8       280   4.0e-104  550.8
seq3      prot034     92.10   265     12        1        10      274   11      280  1.2e-100  538.9
seq4      prot040     97.70   300     5         1        1       300   2       301   3.2e-115  585.9
seq4      prot041     91.20   290     13        1        5       295   8       302   2.8e-100  540.4
seq5      prot050     99.05   310     3         0        1       310   1       310   1.1e-125  622.8
"""

    # Read the in the expected data compare
    expected_df = pd.read_csv(io.StringIO(expected_data), sep='\s+', header=None)

    pd.testing.assert_frame_equal(filtered_df, expected_df)
