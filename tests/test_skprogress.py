import sys

from skprogress import ProgressIO

PRE_BEGIN = """----------
iter: 8
n_candidates: 2
n_resources: 5120
"""

BEGIN = "Fitting 5 folds for each of 2 candidates, totalling 10 fits"

ONE_FIT = "[CV] END ..........logisticregression__C=0.07354022437920146; total time=   0.1s"

ALL_FITS = """[CV] END ..........logisticregression__C=0.07354022437920146; total time=   0.1s
[CV] END ..........logisticregression__C=0.07354022437920146; total time=   0.1s
[CV] END ..........logisticregression__C=0.13173048156427555; total time=   0.1s
[CV] END ..........logisticregression__C=0.13173048156427555; total time=   0.1s
[CV] END ...........logisticregression__C=2.7577316041981197; total time=   0.1s
[CV] END ...........logisticregression__C=2.7577316041981197; total time=   0.1s
[CV] END ..........logisticregression__C=0.00915621079280798; total time=   0.1s
[CV] END ..........logisticregression__C=0.00915621079280798; total time=   0.1s
[CV] END ...........logisticregression__C=0.7214373394443109; total time=   0.1s
[CV] END ...........logisticregression__C=0.7214373394443109; total time=   0.1s
""".splitlines()


def test_get_fits():
    progress = ProgressIO(sys.stdout)
    assert progress._get_fits(BEGIN) == 10
    assert progress._get_fits(PRE_BEGIN + BEGIN) == 10
    assert progress._get_fits(ONE_FIT) is None
