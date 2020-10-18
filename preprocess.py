# import glob
# import pandas as pd
#
# l = [pd.read_csv(filename) for filename in glob.glob("/path/*.txt")]
# df = pd.concat(l, axis=0)

import tensorflow as tf

import tensorflow_datasets as tfds

ds = tfds.load('speech_commands', split='train')
ds = ds.take(1)  # Only take a single example

for example in ds:  # example is `{'image': tf.Tensor, 'label': tf.Tensor}`
  print(list(example.keys()))
  audio = example["audio"]
  label = example["label"]
  print(audio.shape, audio)
