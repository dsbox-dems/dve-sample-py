#!/usr/bin/env python
# coding: utf-8

# In[1]:

import numpy as np
import pandas as pd

import time
import os
import os.path
import sys
from collections import namedtuple
import argparse
from datetime import datetime
from typing import Optional

# In[2]:

from vce.common.util.trace import trace_logger
from dve.config.data import cfd
import dve.cli as cli
from vce.cli import std_main, std_unknown

# In[3]:

import logging


def getLogger():
    logging.basicConfig(level=logging.DEBUG)  # TODO: config/verbose
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    # logget.setLevel(logging.INFO)
    return logger


log = getLogger()

trc = trace_logger("dmy")

# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# In[4]:

RC = 0

TIME_START = datetime.now()

TEST_CASE_1_TINY = "test_one-80.csv"
TEST_CASE_1_SMALL = "test_one-1k.csv"
TEST_CASE_1_MEDIUM = "test_one-2k.csv"
TEST_CASE_1_LARGE = "test_one-35k.csv"
TEST_CASE_DEFAULT = TEST_CASE_1_SMALL

ARGV_DEFAULT = [
    "--jobname",
    "_",
    "--group",
    "test",
    "--filename",
    TEST_CASE_DEFAULT,
]

ARGV_NOTEBOOK = ARGV_DEFAULT

# -----
args = None

# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# In[5]:


def in_notebook():
    try:
        from IPython import get_ipython

        if "IPKernelApp" not in get_ipython().config:  # pragma: no cover
            return False
    except ImportError:
        return False
    except AttributeError:
        return False
    return True


def get_argv(argv: Optional[list[str]] = None) -> list[str]:
    if argv is not None:
        return argv
    if in_notebook():
        return ARGV_NOTEBOOK
    if len(sys.argv) > 1:
        return sys.argv[1:]
    return ARGV_DEFAULT


def argparser(options=None):
    # """Parent Argument Parser."""
    # import dve.scripts.runner as auto_runner
    # parser = auto_runner.argparser(options)
    """Base Argument Parser."""
    parser = argparse.ArgumentParser(add_help=False, conflict_handler="resolve")

    parser.add_argument("-j", "--jobname", type=str, help="job name", default="_")
    parser.add_argument("-g", "--group", type=str, help="job group", default="_")
    parser.add_argument(
        "-f", "--filename", type=str, help="data file name", default="_"
    )
    return parser


def parse_args(argv=None):
    """Process command line arguments."""
    argv = get_argv(argv)
    global args
    parser = argparser()
    # args = parser.parse_args(argv)
    args, unknown = parser.parse_known_args(argv)
    return std_unknown(args, unknown)


# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////


def jobid():
    jobid = os.getenv("X_CORE_JOBID")
    if not jobid:
        return TIME_START.isoformat()
    return jobid


# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# In[6]:

Model = namedtuple("Model", ["spec", "parms"])

model: Optional[Model] = None


def retrieve_model():
    global model
    spec = dict()
    parms = dict()
    model = Model(spec, parms)
    return model


# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# In[7]:

DataConf = namedtuple(
    "DataConf",
    [
        "dd_jobid",
        "dd_slot",
        "dd_slots",
        "dd_group",
        "dd_filename",
        "dd_path",
        "dd_temp",
        "dd_part",
        "dd_indir",
        "dd_outdir",
        "dd_infile",
        "dd_outfile",
    ],
)

dd_conf: Optional[DataConf] = None


def arg_jobid(args):
    return jobid()


def arg_group(args):
    return args.group


def arg_filename(args):
    return args.filename


def arg_slotid(args):
    return 0


def arg_slotnum(args):
    return 1


def config_data() -> DataConf:
    global dd_conf, args

    dd_jobid = arg_jobid(args)
    dd_slot = arg_slotid(args)
    dd_slots = arg_slotnum(args)
    dd_group = arg_group(args)
    dd_filename = arg_filename(args)
    dd_path = f"{cfd().DATA_HOME}/{dd_group}"
    dd_temp = f"{cfd().DATA_TEMP}/{__name__}/{dd_jobid}/{dd_slots}"
    dd_indir = "in"
    dd_outdir = "out"

    dd_part = f"{dd_temp}/{{dd_slot}}/"
    dd_infile = f"{dd_path}/{dd_indir}/{dd_filename}"
    dd_outfile = f"{dd_part}/{dd_indir}/{dd_filename}"

    dd_conf = DataConf(
        dd_jobid=dd_jobid,
        dd_slot=dd_slot,
        dd_slots=dd_slots,
        dd_group=dd_group,
        dd_filename=dd_filename,
        dd_path=dd_path,
        dd_temp=dd_temp,
        dd_part=dd_part,
        dd_indir=dd_indir,
        dd_outdir=dd_outdir,
        dd_infile=dd_infile,
        dd_outfile=dd_outfile,
    )

    return dd_conf


# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# In[7]:


def ensure_path(filename):
    dir_name = os.path.dirname(filename)
    os.makedirs(dir_name, mode=0o775, exist_ok=True)
    return filename


def load_data(dd_conf: Optional[DataConf] = dd_conf):
    global df
    assert dd_conf is not None
    dd_infile = dd_conf.dd_infile
    df = pd.read_csv(dd_infile, sep=";")
    # print (df)
    return df


# In[8]:

InputData = namedtuple("InputData", ["df"])

in_data: Optional[InputData] = None


def prepare_data(df=df, model: Optional[Model] = model):
    global in_data
    assert model is not None
    spec = model.spec
    parms = model.parms

    in_data = InputData(df=df)
    return in_data


# In[9]:


def evaluate_model(
    limits, in_data=in_data, model=model, dd_conf: Optional[DataConf] = dd_conf
):
    t1 = time.time()
    assert model is not None
    assert dd_conf is not None
    spec, parms = model.spec, model.parms
    id, sentence, dat = in_data.id, in_data.sentence, in_data.dat
    labels = {0: "positive", 1: "negative", 2: "neutral"}
    results = pd.DataFrame(
        columns=[
            "id",
            "data",
            "sentence",
            "logit_positive",
            "logit_negative",
            "logit_neutral",
            "prediction",
            "sentiment_score",
        ]
    )

    rows = []

    for idk in range(limits):
        inputs = tokenizer(sentence[idk], return_tensors="pt", padding=True)
        # print(idk)
        with torch.no_grad():
            logits = softmax(np.array(finbert(**inputs)[0]))
            prediction = labels[np.argmax(logits)]
            sentiment_score = pd.Series(logits[:, 0] - logits[:, 1])
            first_result = {
                "id": id[idk],
                "data": dat[idk],
                "sentence": sentence[idk],
                "logit_positive": logits[0][0],
                "logit_negative": logits[0][1],
                "logit_neutral": logits[0][2],
                "prediction": prediction,
                "sentiment_score": sentiment_score,
            }
            rows.append(first_result)
            trc.update()

    results = results.append(rows, ignore_index=True, sort=False)
    t2 = time.time()
    print(t2 - t1)
    return results


OutputData = namedtuple(
    "OutputData",
    [
        "out",
    ],
)

out_data: Optional[OutputData] = None


def process_data(
    in_data=in_data, model=model, dd_conf: Optional[DataConf] = dd_conf
) -> OutputData:
    assert dd_conf is not None
    lim = len(in_data.sentence)
    with trc:
        out = evaluate_model(lim, in_data=in_data, model=model)
        global out_data
        out_data = OutputData(out=out)
        return out_data


# In[10]:


def save_data(
    out_data: Optional[OutputData] = out_data, dd_conf: Optional[DataConf] = dd_conf
):
    assert dd_conf is not None
    assert out_data is not None

    dd_outfile = dd_conf.dd_outfile
    ensure_path(dd_outfile)

    out = out_data.out
    out.to_csv(dd_outfile, sep=";", index=False, encoding="utf-8-sig")


# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# In[13]:


def pre_eval():
    model = retrieve_model()
    dd_conf = config_data()
    df = load_data(dd_conf=dd_conf)
    in_data = prepare_data(df=df, model=model)
    return in_data, model, dd_conf


def do_eval(in_data=in_data, model=model, dd_conf: Optional[DataConf] = dd_conf):
    out_data = process_data(in_data=in_data, model=model, dd_conf=dd_conf)
    return out_data


def post_eval(out_data=out_data, dd_conf: Optional[DataConf] = dd_conf):
    save_data(out_data=out_data, dd_conf=dd_conf)


def run_worker():
    in_data, model, dd_conf = pre_eval()
    out_data = do_eval(in_data=in_data, model=model)
    post_eval(out_data=out_data, dd_conf=dd_conf)
    return RC


@std_main(log=log, debug=True)
def main(argv=None):
    global args

    print(argv)
    print(__name__ + "main:" + str(argv))

    argv = get_argv(argv)

    log.info(">> ### " + __name__ + ".main(argv=" + str(argv) + ")")
    args = parse_args(argv)
    run_worker()

    log.info("<< ###" + __name__ + ".main => (rc=" + str(RC) + ")")
    return RC


# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# In[14]:

if __name__ == "__main__":
    main()
