# ДЗ №9: MLflow experiments і метрики у Grafana

<!-- TODO: 2-3 речення - що робить цей проєкт і навіщо (своїми словами,
     орієнтуючись на людину, яка бачить репозиторій вперше). -->

## Архітектура

<!-- TODO: намалюйте текстову схему (як у прикладі на занятті):
     train_and_push.py → MLflow → Postgres / MinIO
                        → PushGateway → Prometheus → Grafana
     Git (lesson-9) → Argo CD → Kubernetes

     Додайте 2-3 речення: чому MLflow сам нічого не зберігає, і навіщо
     потрібен саме PushGateway, а не прямий /metrics endpoint. -->

## Структура проєкту

<!-- TODO: коротке дерево каталогів + одне речення на кожен верхньорівневий
     каталог (argocd/, experiments/, best_model/, tests/). -->

## Розгортання через Argo CD

<!-- TODO: команди, якими ви перевіряли, що Application-и створені і
     синхронізовані (kubectl apply -f ..., kubectl get applications, ...).
     Додайте, у якому namespace шукати under - infra-tools/application/monitoring. -->

```bash
# TODO
```

## Локальний доступ через port-forward

<!-- TODO: по одній команді kubectl port-forward на кожен сервіс
     (MLflow, MinIO, PushGateway, Grafana) і порт, на якому він з'явиться. -->

```bash
# TODO
```

## Запуск експериментів

<!-- TODO: як встановити залежності (pip install -r experiments/requirements.txt),
     скопіювати .env.example → .env, і запустити python experiments/train_and_push.py.
     Що студент повинен побачити в консолі при успішному запуску? -->

```bash
# TODO
```

## Перевірка результату

<!-- TODO: як переконатись, що все спрацювало:
     - MLflow UI: скільки runs, де подивитись параметри й метрики;
     - best_model/: що там має з'явитись;
     - PushGateway: як подивитись /metrics і побачити mlflow_accuracy/mlflow_loss;
     - Grafana → Explore → Prometheus: який запит (PromQL) ввести. -->

## Скріншоти

<!-- TODO: додайте посилання на скріншоти в assets/ - MLflow UI зі списком
     runs, і Grafana Explore з графіком mlflow_accuracy / mlflow_loss. -->

- MLflow UI: `assets/<TODO>.png`
- Grafana Explore: `assets/<TODO>.png`

## Прибирання ресурсів

<!-- TODO: нагадайте собі й перевіряючому - які команди ви виконали, щоб
     видалити платні ресурси (terraform destroy / видалення Argo CD Applications),
     і що ви свідомо залишили (наприклад, S3-бакет для Terraform state). -->
