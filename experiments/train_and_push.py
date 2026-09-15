"""Навчання серії моделей, MLflow tracking та експорт метрик у PushGateway."""

from __future__ import annotations

import os
import shutil
from dataclasses import dataclass
from pathlib import Path

import mlflow
import mlflow.sklearn
from dotenv import load_dotenv
from mlflow import MlflowClient
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, log_loss
from sklearn.model_selection import train_test_split


EXPERIMENT_NAME = "Iris Logistic Regression - lesson 9"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
BEST_MODEL_DIR = PROJECT_ROOT / "best_model"


@dataclass(frozen=True)
class RunResult:
    """Мінімальний набір даних для порівняння завершених runs."""

    run_id: str
    c: float
    max_iter: int
    accuracy: float
    loss: float


def require_setting(name: str, default: str | None = None) -> str:
    """Повернути значення змінної оточення або зупинити запуск."""

    value = os.getenv(name, default)

    if not value or not value.strip():
        raise RuntimeError(
            f"Environment variable '{name}' is not set. "
            f"Add it to the .env file or set it in the environment."
        )

    return value.strip()


def publish_metrics(pushgateway_url: str, result: RunResult) -> None:
    """Опублікувати accuracy і loss одного run у PushGateway."""

    registry = CollectorRegistry()

    accuracy_gauge = Gauge(
        "mlflow_accuracy",
        "Accuracy of MLflow run",
        labelnames=["run_id"],
        registry=registry,
    )

    loss_gauge = Gauge(
        "mlflow_loss",
        "Log loss of MLflow run",
        labelnames=["run_id"],
        registry=registry,
    )

    accuracy_gauge.labels(run_id=result.run_id).set(result.accuracy)
    loss_gauge.labels(run_id=result.run_id).set(result.loss)

    push_to_gateway(
        pushgateway_url,
        job="mlflow_experiments",
        registry=registry,
        grouping_key={"run_id": result.run_id},
    )


def select_best(results: list[RunResult]) -> RunResult:
    """Вибрати run з найбільшою accuracy; при нічиїй — з меншим loss."""

    if not results:
        raise ValueError("No completed runs available.")

    return max(results, key=lambda result: (result.accuracy, -result.loss))


def download_best_model(client: MlflowClient, best: RunResult) -> Path:
    """Завантажити артефакт найкращої моделі у best_model/."""

    BEST_MODEL_DIR.mkdir(parents=True, exist_ok=True)

    for item in BEST_MODEL_DIR.iterdir():
        if item.is_dir():
            shutil.rmtree(item)
        else:
            item.unlink()
    # if BEST_MODEL_DIR.exists():
    #     shutil.rmtree(BEST_MODEL_DIR)

    # BEST_MODEL_DIR.mkdir(parents=True, exist_ok=True)

    downloaded_path = client.download_artifacts(
        best.run_id,
        "model",
        str(BEST_MODEL_DIR),
    )

    return Path(downloaded_path)


def main() -> None:
    """Провести серію експериментів і зберегти найкращу модель."""

    load_dotenv(PROJECT_ROOT / ".env")

    tracking_uri = require_setting(
        "MLFLOW_TRACKING_URI",
        "http://127.0.0.1:5000",
    )
    pushgateway_url = require_setting(
        "PUSHGATEWAY_URL",
        "http://127.0.0.1:9091",
    )

    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment(EXPERIMENT_NAME)

    iris = load_iris()

    x_train, x_test, y_train, y_test = train_test_split(
        iris.data,
        iris.target,
        test_size=0.2,
        random_state=42,
        stratify=iris.target,
    )

    parameter_grid = [
        {"C": 0.1, "max_iter": 100},
        {"C": 0.5, "max_iter": 200},
        {"C": 1.0, "max_iter": 300},
        {"C": 10.0, "max_iter": 500},
    ]

    results: list[RunResult] = []

    for parameters in parameter_grid:
        with mlflow.start_run(
            run_name=f"C={parameters['C']}-iter={parameters['max_iter']}"
        ) as active_run:
            model = LogisticRegression(
                C=parameters["C"],
                max_iter=parameters["max_iter"],
                random_state=42,
            )

            model.fit(x_train, y_train)

            predictions = model.predict(x_test)
            probabilities = model.predict_proba(x_test)

            accuracy = accuracy_score(y_test, predictions)
            loss = log_loss(y_test, probabilities)

            result = RunResult(
                run_id=active_run.info.run_id,
                c=parameters["C"],
                max_iter=parameters["max_iter"],
                accuracy=accuracy,
                loss=loss,
            )

            mlflow.log_params(
                {
                    "C": parameters["C"],
                    "max_iter": parameters["max_iter"],
                    "random_state": 42,
                    "test_size": 0.2,
                }
            )

            mlflow.log_metrics(
                {
                    "accuracy": accuracy,
                    "loss": loss,
                }
            )

            mlflow.set_tags(
                {
                    "dataset": "iris",
                    "homework": "lesson-9",
                }
            )

            mlflow.sklearn.log_model(
                model,
                artifact_path="model",
            )

            results.append(result)

        publish_metrics(pushgateway_url, result)

        print(
            f"run_id={result.run_id} | "
            f"C={result.c} | "
            f"max_iter={result.max_iter} | "
            f"accuracy={result.accuracy:.4f} | "
            f"loss={result.loss:.4f}"
        )

    best = select_best(results)

    client = MlflowClient(tracking_uri=tracking_uri)

    client.set_tag(
        best.run_id,
        "stage",
        "best",
    )

    model_path = download_best_model(client, best)

    print("\nBest model:")
    print(f"run_id={best.run_id}")
    print(f"C={best.c}")
    print(f"max_iter={best.max_iter}")
    print(f"accuracy={best.accuracy:.4f}")
    print(f"loss={best.loss:.4f}")
    print(f"model_path={model_path}")


if __name__ == "__main__":
    main()