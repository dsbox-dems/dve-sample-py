---
title: Data readme
subtitle: dataset description
author: ..
date: 23/04/2020
---
Project DATA
============


Info
----

* `./data`: data directory, relative to project base directory
* `./data/int`: _"internal"_ data directory, committed to project repository
* `./data/ext`: _"external"_ data directory, not committed, link to external (shared) data
* `./data/tmp`: _"temporary"_ data directory, not committed, scratch (unshared) data
* `./data/def`: _"default"_ data directory, preconfigured defaut data directory, symlink to current data

Config
------

* `./data/.gitignore`: ignore all with exceptions


```

*

!.gitignore
!README.md

!int/



```



DATASETS
========


Test Dataset
------------


* `./data/int/test`: unit test data







