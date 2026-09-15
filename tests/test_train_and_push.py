"""Юніт-тести для чистої логіки select_best (без мережі, без MLflow-сервера)."""

from experiments.train_and_push import RunResult, select_best


def test_select_best_prefers_accuracy() -> None:
    run1 = RunResult(run_id="run-1", accuracy=0.85, loss=0.30)
    run2 = RunResult(run_id="run-2", accuracy=0.90, loss=0.40)

    best = select_best([run1, run2])

    assert best == run2


def test_select_best_uses_loss_as_tiebreaker() -> None:
    run1 = RunResult(run_id="run-1", accuracy=0.90, loss=0.30)
    run2 = RunResult(run_id="run-2", accuracy=0.90, loss=0.20)

    best = select_best([run1, run2])

    assert best == run2


def test_select_best_single_run() -> None:
    run = RunResult(run_id="run-1", accuracy=0.90, loss=0.20)

    best = select_best([run])

    assert best == run