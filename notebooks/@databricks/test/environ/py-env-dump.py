# Databricks notebook source
import sys

print(sys.version)

# COMMAND ----------

import platform

print(platform.python_version())

# COMMAND ----------

import numpy as np

print(np.__version__)


# COMMAND ----------

import pandas as pd

print(pd.__version__)

# COMMAND ----------

import pyspark

print(pyspark.__version__)

from pyspark.sql import SparkSession
