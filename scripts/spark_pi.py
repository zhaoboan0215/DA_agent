# Spark-PI example script for Da Agent
# sc (SparkContext) is injected by the DAG callable — do NOT create it here.
import random

count = sc.parallelize(range(500_000)).filter(lambda _: random.random() ** 2 + random.random() ** 2 < 1).count()  # noqa: F821
print(f"[DA] Pi \u2248 {4.0 * count / 500_000:.6f}")
