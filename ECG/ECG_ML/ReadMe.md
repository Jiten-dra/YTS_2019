# ECG - Classification of Arrhythmia

We will look some standard datasets for ECG signals, process the raw signals so that they can be used to classify Arrhythmia. We use Physionet - MIT DB Dataset.
This is present in MIT-DB Folder.

# Steps to follow

1. Install PyCharm Community Edition using the following link : [Download Link](https://download.jetbrains.com/python/pycharm-community-2019.1.2.exe)
2. Create a new project in PyCharm.
3. Open Terminal and write : "pip install -r requirements.txt"

## The Preprocessing Part
#### ecgSignalPreprocessing.py
The function extract_features will segregate the features of the ECG signal like what is the length of QRS, STT. The input to this function is a complete ecg signal. It processes the dat files, annotation files and hea files for this signal and returns a dictionary of the features.

## ML Part
[Introduction to Neural Networks](https://www.youtube.com/watch?v=aircAruvnKk)
In this step, we will build a machine learning based classifier for predicting if given signal is a normal heartbeat or a VEB heartbeat.  
The following models have been trained on the processed data :

#### Network :
1.  Input : 8
2.  Layer 1 : 128 Neurons + Relu activation
3.  Layer 2 : 32 Neurons + Relu activation
4.  Output Layer : 1 Neuron + Sigmoid activation\
Loss : 'binary_crossentropy'
optimizer='adam'