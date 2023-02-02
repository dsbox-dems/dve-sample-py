#!/usr/bin/env python
# coding: utf-8

# In[1]:

import numpy as np
import pandas as pd

import time
import os
import os.path
import re
import glob
import sys
from collections import namedtuple
import argparse
from datetime import datetime
from typing import Optional

# In[2]:

from vce.common.util.trace import trace_logger
from vce.config.data import cfd
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

trc = trace_logger("fbx")

# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# In[3]:

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
in_data = None
out_data = None
df = None
sentence = None
dat = None

# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# In[4]:


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


def get_argv(argv=None):
    if argv is not None:
        return argv
    if in_notebook():
        return ARGV_NOTEBOOK
    if len(sys.argv) > 1:
        return sys.argv[1:]
    return ARGV_DEFAULT


def argparser(options=None):
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


def is_core_parallel():
    slots = os.getenv("X_CORE_SLOTS")
    if not slots:
        return False
    return int(slots) > 0


def is_core_simple():
    return not is_core_parallel()


def is_core_mode(mode):
    if is_core_simple:
        return False
    env_mode = os.getenv("X_CORE_MODE")
    if not env_mode:
        return False
    return int(env_mode) == mode


def is_core_worker():
    if is_core_simple:
        return True
    return is_core_mode(0)


def is_core_distributor():
    return is_core_mode(1)


def is_core_collector():
    return is_core_mode(2)


def slot_idx():
    slot = os.getenv("X_CORE_SLOT")
    if not slot:
        return 0
    return int(slot)


def slots_num():
    slots = os.getenv("X_CORE_SLOTS")
    if not slots:
        return 1
    return int(slots)


def jobid():
    jobid = os.getenv("X_CORE_JOBID")
    if not jobid:
        return TIME_START.isoformat()
    return jobid


# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# In[5]:

Model = namedtuple("Model", ["finbert", "tokenizer"])


def retrieve_model():
    global model
    finbert = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")
    tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
    model = Model(finbert, tokenizer)
    return model


# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# In[6]:

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
    return slot_idx()


def arg_slotnum(args):
    return slots_num()


def config_data() -> DataConf:
    global dd_conf, args

    dd_jobid = arg_jobid(args)
    dd_slot = arg_slotid(args)
    dd_slots = arg_slotnum(args)
    dd_group = arg_group(args)
    dd_filename = arg_filename(args)
    dd_path = f"{cfd().DATA_HOME}/{dd_group}"
    dd_temp = f"{cfd().DATA_TEMP}/{__name__}/{dd_jobid}/{dd_slots}"
    dd_indir = "Output R"
    dd_outdir = "Output Python"

    if is_core_parallel():
        if is_core_collector():
            dd_part = f"{dd_temp}/{{dd_slot}}/"
            dd_infile = f"{dd_path}/{dd_indir}/{dd_filename}"
            dd_outfile = f"{dd_part}/{dd_indir}/{dd_filename}"
        elif is_core_worker():
            dd_part = f"{dd_temp}/{dd_slot}/"
            dd_infile = f"{dd_part}/{dd_indir}/{dd_filename}"
            dd_outfile = f"{dd_temp}/{dd_outdir}/{dd_filename}"
        elif is_core_collector():
            dd_part = f"{dd_temp}/{{dd_slot}}/"
            dd_infile = f"{dd_part}/{dd_outdir}/{dd_filename}"
            dd_outfile = f"{dd_path}/{dd_outdir}/{dd_filename}"
        else:
            raise ValueError("is_core_parallel")
    elif is_core_simple():
        dd_part = f"{dd_temp}/_/"
        dd_infile = f"{dd_path}/{dd_indir}/{dd_filename}"
        dd_outfile = f"{dd_path}/{dd_outdir}/{dd_filename}"
    else:
        raise ValueError("is_core_what")

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


def load_data(dd_conf=dd_conf):
    global df
    dd_infile = dd_conf.dd_infile
    df = pd.read_csv(dd_infile, sep=";")
    # print (df)
    return df


# In[8]:

InputData = namedtuple("InputData", ["df", "id", "sentence", "dat"])


def prepare_data(df=df, model=model):
    global sentence, dat, in_data
    tokenizer = model.tokenizer
    sentence = df["text"]
    dat = df["created_at"]
    id = df["id"]
    # print(*sentence,sep="\n")
    # print(dat)
    alert = 0
    i = 0
    t11 = time.time()
    for ind in range(len(sentence)):
        inputs2 = tokenizer(sentence[ind], return_tensors="pt", padding=True)
        if len(inputs2["input_ids"][0]) >= 512:
            alert = 1
            i = ind

    if alert == 1:
        print(
            "Attenzione la stringa n  "
            + str(i)
            + " con id numero "
            + str(id[i])
            + " produce troppi indici"
        )
    else:
        print("ok")

    t12 = time.time()
    print(t12 - t11)

    in_data = InputData(df=df, id=id, sentence=sentence, dat=dat)
    return in_data


# In[9]:


def softmax(x):
    """Compute softmax values for each sets of scores in x."""
    e_x = np.exp(x - np.max(x, axis=1)[:, None])
    return e_x / np.sum(e_x, axis=1)[:, None]


def evaluate_model(limits, in_data=in_data, model=model):
    t1 = time.time()
    finbert, tokenizer = model.finbert, model.tokenizer
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


def process_data(in_data=in_data, model=model):
    # lim = 1000
    lim = len(in_data.sentence)
    with trc:
        out = evaluate_model(lim, in_data=in_data, model=model)
        # print(out)
        # ciclo()
        # print(out.iloc[999,0:7])
        global out_data
        out_data = OutputData(out=out)
        return out_data


# In[10]:


def save_data(out_data=out_data, dd_conf=dd_conf):
    dd_outfile = dd_conf.dd_outfile
    ensure_path(dd_outfile)

    out = out_data.out
    out.to_csv(dd_outfile, sep=";", index=False, encoding="utf-8-sig")


# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# In[11]:


def distribute_data(dd_conf: Optional[DataConf] = dd_conf):
    assert dd_conf is not None

    num_chunks = dd_conf.dd_slots

    dd_infile = dd_conf.dd_infile
    dd_outfile = dd_conf.dd_outfile

    with open(dd_infile) as f:
        lines_count = sum(1 for _ in f)

    chunksize = lines_count // num_chunks
    i = 0
    with pd.read_csv(dd_infile, chunksize=chunksize) as reader:
        for chunk in reader:
            f = ensure_path(dd_outfile.format(dd_slot=i))
            chunk.to_csv(f)
            i = i + 1


# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# In[12]:


def collect_data(dd_conf: Optional[DataConf] = dd_conf):
    assert dd_conf is not None

    dd_temp = dd_conf.dd_temp
    dd_outdir = dd_conf.dd_outdir
    dd_outfile = dd_conf.dd_outfile
    ensure_path(dd_outfile)

    os.chdir(dd_temp)

    extension = "csv"
    all_csvfiles = [i for i in glob.glob("*.{}".format(extension))]
    all_outfiles = filter(lambda x: re.search(rf"{dd_outdir}", x), all_csvfiles)

    combined_csv = pd.concat([pd.read_csv(f) for f in all_outfiles])
    combined_csv.to_csv(dd_outfile, index=False, encoding="utf-8-sig")


# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# In[13]:


def pre_eval():
    model = retrieve_model()
    dd_conf = config_data()
    df = load_data(dd_conf=dd_conf)
    in_data = prepare_data(df=df, model=model)
    return in_data, model, dd_conf


def do_eval(in_data=in_data, model=model):
    out_data = process_data(in_data=in_data, model=model)
    return out_data


def post_eval(out_data=out_data, dd_conf=dd_conf):
    save_data(out_data=out_data, dd_conf=dd_conf)


def run_worker():
    in_data, model, dd_conf = pre_eval()
    out_data = do_eval(in_data=in_data, model=model)
    post_eval(out_data=out_data, dd_conf=dd_conf)


def do_distribute(dd_conf=dd_conf):
    distribute_data(dd_conf=dd_conf)


def run_distributor():
    dd_conf = config_data()
    do_distribute(dd_conf=dd_conf)
    return RC


def do_collect(dd_conf=dd_conf):
    collect_data(dd_conf=dd_conf)


def run_collector():
    dd_conf = config_data()
    do_collect(dd_conf=dd_conf)
    return RC


def main(argv=None, **kwargs):
    global args

    print(argv)
    print(__name__ + "main:" + str(argv))

    argv = get_argv(argv)

    log.info(">> ### " + __name__ + ".main(argv=" + str(argv) + ")")
    args = parse_args(argv, **kwargs)

    if is_core_parallel():
        if is_core_distributor():
            run_distributor()
        elif is_core_worker():
            run_worker()
        elif is_core_collector():
            run_collector()
        else:
            raise ValueError("is_core_parallel")
    elif is_core_simple():
        run_worker()
    else:
        raise ValueError("is_core_what")

    log.info("<< ###" + __name__ + ".main => (rc=" + str(RC) + ")")
    return RC


# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# In[14]:

if __name__ == "__main__":
    main()
