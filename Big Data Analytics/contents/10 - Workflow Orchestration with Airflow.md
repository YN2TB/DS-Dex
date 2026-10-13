---
subject: Big Data Analytics
chapter: 10
tags: [ds, airflow, orchestration, dag, scheduling, data-pipelines]
source: "No source in documents/. Based on the user's Overview (mid-term: Apache Airflow) and standard Apache Airflow 2.x concepts."
---

# Workflow Orchestration with Airflow

> [!warning] No textbook for this chapter
> Neither book in `documents/` covers Airflow. This note uses standard Apache Airflow 2.x concepts. Check it against the lecture slides if they become available.

## 📘 Main Knowledge

### 1. Why orchestration

A data platform runs many dependent jobs: ingest from APIs and databases, land files in the lake, run Spark transformations, train models, refresh dashboards. An **orchestrator** decides **when** each job runs, in **what order**, retries failures, records what happened, and lets you rerun past periods. Cron alone cannot express dependencies, retries, backfills or monitoring.

**Apache Airflow** (created at Airbnb in 2014, Apache top-level project 2019) defines workflows **as Python code**. Airflow orchestrates; it should not do the heavy data processing itself. It triggers Spark, SQL engines, or containers that do the work.

### 2. Core concepts

| Concept | Meaning |
|---|---|
| **DAG** | a directed acyclic graph of tasks with a schedule; one Python file can define one or more DAGs |
| **Task** | one node of the DAG, an instance of an operator |
| **Operator** | a template for a kind of work: `BashOperator`, `PythonOperator`, `SparkSubmitOperator`, `SQLExecuteQueryOperator`, `KubernetesPodOperator`, `EmailOperator`… |
| **Sensor** | an operator that waits for a condition (a file appears, a partition exists, another DAG finishes) |
| **DAG run** | one execution of a DAG for a specific data interval |
| **Task instance** | one execution of a task within a DAG run; has a state (queued, running, success, failed, up_for_retry, skipped, upstream_failed) |
| **XCom** | small messages passed between tasks (IDs, file paths), not datasets |
| **Connection / Variable** | stored credentials and configuration, kept out of DAG code |
| **Hook** | the client code an operator uses to talk to an external system |

"Acyclic" matters: tasks cannot depend on themselves directly or indirectly, so there is always an order (a topological sort) in which to run them.

### 3. Architecture

- **Scheduler**: parses DAG files, creates DAG runs when their schedule is due, and queues task instances whose dependencies are met.
- **Executor**: decides where tasks run: `SequentialExecutor` (one at a time, testing), `LocalExecutor` (parallel processes on one machine), `CeleryExecutor` (a pool of workers via a message queue), `KubernetesExecutor` (a pod per task).
- **Workers**: run the tasks.
- **Metadata database** (PostgreSQL/MySQL): stores DAG runs, task states, XComs, connections.
- **Web server (UI)**: graph and grid views, logs, manual triggers, clearing tasks for reruns.

### 4. Writing a DAG

```python
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

default_args = {"owner": "data-team", "retries": 2, "retry_delay": timedelta(minutes=5)}

def check_quality(ds, **_):
    print(f"checking partition {ds}")      # ds = logical date as YYYY-MM-DD

with DAG(
    dag_id="daily_sales",
    start_date=datetime(2026, 1, 1),
    schedule="@daily",                       # cron also works: "0 2 * * *"
    catchup=False,
    default_args=default_args,
) as dag:
    ingest = BashOperator(task_id="ingest",
        bash_command="python ingest.py --date {{ ds }}")
    transform = SparkSubmitOperator(task_id="transform",
        application="/jobs/sales_etl.py", application_args=["--date", "{{ ds }}"],
        conn_id="spark_default")
    quality = PythonOperator(task_id="quality_check", python_callable=check_quality)
    publish = BashOperator(task_id="publish", bash_command="echo publish {{ ds }}")

    ingest >> transform >> quality >> publish
```

- Dependencies: `a >> b` (b after a), `a >> [b, c]` (fan-out), `[b, c] >> d` (fan-in).
- **Templating** (Jinja): `{{ ds }}` (logical date), `{{ data_interval_start }}`, `{{ data_interval_end }}` insert the run's dates into commands, so each run processes its own partition.
- **TaskFlow API** (Airflow 2): decorate Python functions with `@task`; return values pass via XCom automatically.

### 5. Scheduling semantics

- A DAG run covers a **data interval**. For `@daily` with `start_date = 2026-01-01`, the first run covers [Jan 1, Jan 2) and **starts after the interval ends**, i.e. on Jan 2. Its logical date (`ds`) is Jan 1.
- Presets: `@hourly`, `@daily`, `@weekly`, `@monthly`, `None` (manual only); or cron: `minute hour day-of-month month day-of-week` (`0 2 * * *` = 02:00 every day; `*/15 * * * *` = every 15 minutes; `0 6 * * 1` = Mondays 06:00).
- **catchup=True**: when a DAG is turned on, Airflow creates runs for every missed interval since `start_date`. **catchup=False**: only the latest interval.
- **Backfill**: deliberately run a DAG for a past date range (`airflow dags backfill -s 2025-12-01 -e 2025-12-31 daily_sales`), e.g. after fixing a bug.
- Concurrency limits: `max_active_runs` per DAG, `max_active_tasks`, pools for shared resources.

### 6. Reliability practices

- **Idempotent tasks**: running a task twice for the same interval must give the same result. Write to a partition for `{{ ds }}` with overwrite, not append. Then retries, reruns and backfills are safe.
- **Atomic outputs**: write to a temporary location and move/commit at the end, so downstream never sees half-written data.
- **Retries** with delays for transient failures (network, busy cluster); alerts (`on_failure_callback`, email, Slack) for persistent ones; `sla`/timeouts for jobs that hang.
- **Trigger rules**: by default a task runs when all upstream tasks succeed (`all_success`); alternatives include `all_done` (cleanup tasks), `one_failed` (alerting), `none_failed`.
- Keep tasks small and focused; pass references (paths, table names) through XCom, not data.
- Keep DAG files light: top-level code runs every time the scheduler parses the file.
- Separate environments and keep credentials in Connections or a secrets backend.

### 7. Airflow in a big data platform

A typical daily batch pipeline:

1. Sensor waits for source files or for an upstream DAG.
2. Ingest raw data into the lake (bronze layer).
3. `SparkSubmitOperator` cleans and joins data into curated tables (silver/gold), partitioned by date ([[07 - Data Sources and File Formats]]).
4. Data-quality checks; fail the run if row counts or null rates are off.
5. Refresh warehouse tables / BI extracts, train or score models ([[11 - MLlib Pipelines and Feature Engineering]]).

Streaming jobs ([[09 - Stream Processing and Kafka]]) run continuously and are usually not scheduled by Airflow; Airflow can still deploy them, monitor them, or run batch jobs over what they write. Lineage and catalogs ([[02 - Data Architectures]]) can be fed from Airflow metadata.

Alternatives: Luigi, Prefect, Dagster, cloud services (AWS Step Functions, Google Cloud Composer is managed Airflow, Azure Data Factory).

## ✏️ Exercises

> [!example]- **1.** *(Easy) Read cron*
> What schedules are these? (a) `0 2 * * *` (b) `*/15 * * * *` (c) `0 6 * * 1` (d) `30 0 1 * *`
>
> ---
> (a) Every day at 02:00. (b) Every 15 minutes. (c) Every Monday at 06:00. (d) At 00:30 on the first day of every month.

> [!example]- **2.** *(Easy–medium) Order of execution*
> Tasks: `extract_orders`, `extract_customers`, `join` (needs both extracts), `quality` (needs join), `publish` (needs quality), `notify` (needs publish). Write the dependencies and give one valid execution order. Which tasks can run in parallel?
>
> ---
> `[extract_orders, extract_customers] >> join >> quality >> publish >> notify`. A valid order: extract_orders, extract_customers, join, quality, publish, notify. The two extracts can run in parallel; everything after is sequential. If `join` fails, downstream tasks get state `upstream_failed` and do not run.

> [!example]- **3.** *(Medium) Catchup*
> A DAG has `start_date = 2026-01-01`, `schedule="@daily"`, `catchup=True`. It is first enabled on 2026-01-10 at 00:30. How many DAG runs are created, for which logical dates? What changes with `catchup=False`?
>
> ---
> Completed intervals: [Jan 1, Jan 2) … [Jan 9, Jan 10): 9 runs with logical dates Jan 1 to Jan 9. The interval [Jan 10, Jan 11) has not ended, so it is not run yet. With `catchup=False`, only the most recent completed interval (logical date Jan 9) runs.

> [!example]- **4.** *(Medium–hard) Make it idempotent*
> A task runs `INSERT INTO sales_daily SELECT * FROM staging WHERE sale_date = '{{ ds }}'`. The task fails after inserting, is retried, and succeeds. What goes wrong and how do you fix it?
>
> ---
> The retry inserts the same rows again: duplicates. Fix: make the write replace the interval's data, e.g. `INSERT OVERWRITE TABLE sales_daily PARTITION (sale_date='{{ ds }}') SELECT ...` or delete-then-insert in one transaction, or in Spark `df.write.mode("overwrite")` on the date partition (with dynamic partition overwrite). Running the task any number of times for the same `ds` then gives the same table.

> [!example]- **5.** *(Hard) Design a DAG*
> Every hour, clickstream files land in `s3://raw/clicks/YYYY/MM/DD/HH/`. Design a DAG that waits for the hour's files, runs a Spark job to aggregate clicks per page, checks that the output is not empty, and loads it into the warehouse; failures should retry 3 times and alert the team.
>
> ---
> - `schedule="@hourly"`, `catchup=True` (so missed hours are processed), `max_active_runs` limited (e.g. 3) to avoid overloading the cluster.
> - `S3KeySensor` on `raw/clicks/{{ data_interval_start.strftime('%Y/%m/%d/%H') }}/_SUCCESS` with `mode="reschedule"` and a timeout (doesn't hold a worker slot while waiting).
> - `SparkSubmitOperator` with the hour as an argument; the job writes to a partition for that hour with overwrite (idempotent).
> - A check task (e.g. SQL row count > 0) that raises an error if empty.
> - A load task into the warehouse, again overwriting that hour's partition.
> - `default_args={"retries": 3, "retry_delay": timedelta(minutes=5)}`, `on_failure_callback` sending an alert.
> - Dependencies: `sensor >> spark_aggregate >> check >> load`.

## 📝 Summary

- An orchestrator schedules dependent jobs, retries, records history and supports reruns; Airflow defines workflows in Python.
- Concepts: DAG, task, operator, sensor, DAG run, task instance, XCom, connections, hooks.
- Architecture: scheduler, executor (Sequential, Local, Celery, Kubernetes), workers, metadata DB, web UI.
- Dependencies with `>>`; templating with `{{ ds }}` and data-interval variables.
- A run covers a data interval and starts after it ends; catchup creates missed runs; backfill reruns history.
- Make tasks idempotent and atomic; use retries, alerts, trigger rules; Airflow triggers heavy work (Spark) rather than doing it.

## ⚠️ Important Notes

1. The run with logical date Jan 1 (`@daily`) executes on Jan 2, after its interval ends.
2. `catchup=True` with an old `start_date` can launch hundreds of runs at once.
3. Non-idempotent tasks (append inserts) create duplicates on retry or backfill.
4. XCom is for small values; passing DataFrames through it fills the metadata database.
5. Heavy computation inside a `PythonOperator` runs on the Airflow worker, not on Spark.
6. Top-level code in DAG files runs at every scheduler parse; keep it light.
7. Sensors in the default "poke" mode occupy a worker slot while waiting; use reschedule mode or deferrable sensors.
8. A DAG must be acyclic; circular dependencies are rejected.
9. Never hard-code passwords in DAG files; use Connections or a secrets backend.

> [!warning] Gaps in the source material
> - The whole chapter is beyond the provided sources (both books are about Spark). It reflects Airflow 2.x; details like `schedule` vs the older `schedule_interval` argument and operator import paths differ between versions.
> - Kafka and message buses, the other mid-term platform topics, are in [[09 - Stream Processing and Kafka]].

**Previous:** [[09 - Stream Processing and Kafka]] · **Next:** [[11 - MLlib Pipelines and Feature Engineering]]
