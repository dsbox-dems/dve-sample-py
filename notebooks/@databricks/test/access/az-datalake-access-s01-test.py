# Databricks notebook source
def mountData(mountPoint):
  if any([x.mountPoint == mountPoint for x in dbutils.fs.mounts()]):
    print("mount: {} already mounted, skip".format(mountPoint))
    return
  print("mount: {} mounting, ...".format(mountPoint))
  dbutils.fs.mount(
  source = "wasbs://b01@rs0sa0xt0si740d01.blob.core.windows.net",
  mount_point = mountPoint,
  extra_configs = {"fs.azure.account.key.rs0sa0xt0si740d01.blob.core.windows.net":dbutils.secrets.get(scope = "databricks-default-secret-scope", key = "DbksStorageKey29365")})
  print("mount: {} mounting, done".format(mountPoint))

mountData("/mnt/data/b01")
#display(dbutils.fs.mounts())
  

# COMMAND ----------

df = spark.read.options(header='True', inferSchema='True', delimiter=',').csv("/mnt/data/b01/test/basic/load/raw/Iris.csv")

# COMMAND ----------

df.printSchema()
df.cache()
df.count()

# COMMAND ----------

import pandas as pd
import numpy as np
import seaborn as sns

df1= df.drop("Id").toPandas()
df1.head()
sns.pairplot(data=df1, hue="Species")

# COMMAND ----------

display(df)
