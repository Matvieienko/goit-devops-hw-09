"""Юніт-тести для чистої логіки select_best (без мережі, без MLflow-сервера)."""

from experiments.train_and_push import RunResult, select_best


def test_select_best_prefers_accuracy() -> None:
    run1 = RunResult(
        run_id="run-1",
        c=0.1,
        max_iter=100,
        accuracy=0.85,
        loss=0.30,
    )
    run2 = RunResult(
        run_id="run-2",
        c=1.0,
        max_iter=300,
        accuracy=0.90,
        loss=0.40,
    )

    best = select_best([run1, run2])

    assert best == run2


def test_select_best_uses_loss_as_tiebreaker() -> None:
    run1 = RunResult(
        run_id="run-1",
        c=0.5,
        max_iter=200,
        accuracy=0.90,
        loss=0.30,
    )
    run2 = RunResult(
        run_id="run-2",
        c=1.0,
        max_iter=300,
        accuracy=0.90,
        loss=0.20,
    )

    best = select_best([run1, run2])

    assert best == run2


def test_select_best_single_run() -> None:
    run = RunResult(
        run_id="run-1",
        c=10.0,
        max_iter=500,
        accuracy=0.90,
        loss=0.20,
    )

    best = select_best([run])

    assert best == run