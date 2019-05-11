from scipy.signal import butter, lfilter, filtfilt
import wfdb
from statsmodels.tsa.stattools import levinson_durbin
from collections import OrderedDict

def butter_lowpass (cutoff_freq, sampling_freq, order) :
   nyquist_freq = sampling_freq / 2
   normalized_cutoff = cutoff_freq / nyquist_freq
   b, a = butter (order, normalized_cutoff, "lowpass", analog=False)    # 'b' is the numerator, 'a' the denominator
   return b, a

def butter_highpass (cutoff_freq, sampling_freq, order) :
   nyquist_freq = sampling_freq / 2
   normalized_cutoff = cutoff_freq / nyquist_freq
   b, a = butter (order, normalized_cutoff, "highpass", analog=False)    # 'b' is the numerator, 'a' the denominator
   return b, a

def butter_bandpass (low_cutoff_freq, high_cutoff_freq, sampling_freq, order) :
   nyquist_freq = sampling_freq / 2
   normalized_low = low_cutoff_freq / nyquist_freq
   normalized_high = high_cutoff_freq / nyquist_freq
   b, a = butter (order, [normalized_low, normalized_high], "bandpass", analog=False)    # 'b' is the numerator, 'a' the denominator
   return b, a

def butter_bandstop (low_cutoff_freq, high_cutoff_freq, sampling_freq, order) :
   nyquist_freq = sampling_freq / 2
   normalized_low = low_cutoff_freq / nyquist_freq
   normalized_high = high_cutoff_freq / nyquist_freq
   b, a = butter (order, [normalized_low, normalized_high], "bandstop", analog=False)    # 'b' is the numerator, 'a' the denominator
   return b, a

def apply_butter (x, b, a, linear_phase=False):
   if linear_phase:
       return filtfilt (b, a, x)    # See the doc for hint on performance improvement
   else:
       return lfilter (b, a, x)


def butter_filter (x, filter_type, cutoff_freqs, sampling_freq=360, order=3, linear_phase=False):
   assert(isinstance(cutoff_freqs, list))
   assert(cutoff_freqs[0] <= cutoff_freqs[-1])

   if filter_type == "highpass":
       b, a = butter_highpass (cutoff_freqs[0], sampling_freq, order)
   elif filter_type == "lowpass":
       b, a = butter_lowpass (cutoff_freqs[0], sampling_freq, order)
   elif filter_type == "bandpass":
       b, a = butter_bandpass (cutoff_freqs[0], cutoff_freqs[-1], sampling_freq, order)
   elif filter_type == "bandstop":
       b, a = butter_bandstop (cutoff_freqs[0], cutoff_freqs[-1], sampling_freq, order)
   else:
       raise ValueError("Non-recognized filter type !")

   return apply_butter (x, b, a, linear_phase)


def extract_features(record_path, length_qrs, length_stt, ar_order_qrs, ar_order_stt, sampfrom=0, sampto=-1,
                     use_filter=True):
    """
    A list holding tuples with values 'N' or 'VEB', and the length in samples of each corresponding QRS
    and ST/T complexes, plus the length in samples of pre- and post-RR
    """
    qrs_stt_rr_list = list()

    #These signals are read using library of wfdb (waveform database). It uses rdsamp function inorder to read the sample file. Input to this function is path of file channel in which recording was done, and start point of sample index from which we need to read the files
    #Likewise the corresponding atr file is also read using rdann function. This function will return the corresponding annotations

    if sampto < 0:
        raw_signal, _ = wfdb.rdsamp(record_path, channels=[0], sampfrom=sampfrom)
        annotations = wfdb.rdann(record_path, extension="atr", sampfrom=sampfrom, sampto=None)
    else:
        raw_signal, _ = wfdb.rdsamp(record_path, channels=[0], sampfrom=sampfrom, sampto=sampto)
        annotations = wfdb.rdann(record_path, extension="atr", sampfrom=sampfrom, sampto=sampto)


    #Here reshape is used to change 2D array to single array. That is it will bring 2D array to 1D array of row major side.

    raw_signal = raw_signal.reshape(-1)

    # Filtering
    if use_filter:
        filter_1 = butter_filter(raw_signal, filter_type="highpass", order=3, cutoff_freqs=[1],
                                 sampling_freq=annotations.fs)
        filter_2 = butter_filter(filter_1, filter_type="bandstop", order=3, cutoff_freqs=[58, 62],
                                 sampling_freq=annotations.fs)
        signal = butter_filter(filter_2, filter_type="lowpass", order=4, cutoff_freqs=[25],
                               sampling_freq=annotations.fs)
    else:
        signal = raw_signal

    annotation2sample = list(zip(annotations.symbol, annotations.sample))

    for idx, annot in enumerate(annotation2sample):
        beat_type = annot[0]  # "N", "V", ... etc.
        r_peak_pos = annot[1]  # The R peak position
        pulse_start_pos = r_peak_pos - int(length_qrs / 2) + 1  # The sample postion of pulse start (start of QRS)

        # We treat only Normal, VEB, and SVEB signals (See the paper)
        if beat_type == "N" or beat_type == "S" or beat_type == "V":
            qrs = signal[pulse_start_pos: pulse_start_pos + length_qrs]
            stt = signal[pulse_start_pos + length_qrs + 1: pulse_start_pos + length_qrs + length_stt]

            if qrs.size > 0:
                _, qrs_arcoeffs, _, _, _ = levinson_durbin(qrs, nlags=ar_order_qrs, isacov=False)
            else:
                qrs_arcoeffs = None

            if stt.size > 0:
                _, stt_arcoeffs, _, _, _ = levinson_durbin(stt, nlags=ar_order_stt, isacov=False)
            else:
                stt_arcoeffs = None

            pre_rr_length = annotation2sample[idx][1] - annotation2sample[idx - 1][1] if idx > 0 else None
            post_rr_length = annotation2sample[idx + 1][1] - annotation2sample[idx][
                1] if idx + 1 < annotations.ann_len else None

            _type = 1 if beat_type == "V" else 0

            beat_list = list()
            beat_list = [("record", record_path.rsplit(sep="/", maxsplit=1)[-1]), ("type", _type),
                         ("pre-RR", pre_rr_length), ("post-RR", post_rr_length)
                         ]
            for idx, coeff in enumerate(qrs_arcoeffs):
                beat_list.append(("qrs_ar{}".format(idx), coeff))
            for idx, coeff in enumerate(stt_arcoeffs):
                beat_list.append(("stt_ar{}".format(idx), coeff))

            beat_dict = OrderedDict(beat_list)

            qrs_stt_rr_list.append(beat_dict)
    return qrs_stt_rr_list
