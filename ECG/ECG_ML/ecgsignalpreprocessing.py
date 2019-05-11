# coding: utf-8

from filtering.filter import *
import wfdb
from statsmodels.tsa.stattools import levinson_durbin
from collections import OrderedDict

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Conventional training set
DS1 = ["101", "106", "108", "109", "112", "114", "115", "116", "118", "119", "122",
       "124", "201", "203", "205", "207", "208", "209", "215", "220", "223", "230"]



#The function extract_features will segregate the features of the ECG signal like what is the length of QRS, STT
#The data set contains signals where are tagged with many labels like N (Normal) and V (VEB) and others. In this we are considering only N and V and all others are not processed.
#As we have lot of samples, sample that are considered during processing are stored in variables sampfrom and sampto


# Check the paper for choosing the lengthes
length_qrs = 40
length_stt = 120

lst = list()

for i in DS1:
    rec_index = i
    # Tweak the use_filter param
    lst.extend(
        extract_features("MIT-BH/" + rec_index, length_qrs, length_stt, ar_order_qrs=3, ar_order_stt=3, use_filter=True)
    )

df = pd.DataFrame.from_dict(lst)
df.dropna(inplace=True)

# Features extracted are saved to features.csv
df.to_csv("./output/features.csv", index=False)
print("successfully extracted features")

