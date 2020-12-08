[![GitHub release (latest
SemVer)](https://img.shields.io/github/v/release/accraze/audio-soup)](https://github.com/accraze/audio-soup/releases)
[![GitHub](https://img.shields.io/github/license/accraze/audio-soup)](https://github.com/accraze/audio-soup/blob/master/LICENSE)
[![Docker
Pulls](https://img.shields.io/docker/pulls/accraze/audio-soup)](https://hub.docker.com/r/accraze/audio-soup)

# audio-soup
Sample review and feature selection for audio datasets.

<img src="https://imgur.com/FFqIscH.gif" width="600">

View the demo: https://audio-soup.herokuapp.com/

## Quick Start
First make sure Docker is installed on your local machine.
Now build the required containers:
```
make start
```
Next, apply the database schema:
```
make upgrade
```
The application should now be available at 0.0.0.0:5000

## Loading a dataset
You can load your own dataset by adding the dataset within the
`src/static/dataset/` directory. The dataset should resemble the following format:
```
src/static/dataset
├── label-1
│   ├── file1.wav
│   ├── file2.wav
│   └── file-n.wav
├── label-2
│   ├── file-foo.wav
│   └── file-n.wav
└── label n...
    ├── 0a7c2a8d_null_0.wav
    └── 0a7c2a8d_null_1.wav
```
Once you have placed your dataset in the required directory, make sure you have
built the containers and then load the dataset using the following
```
make seed  'dataset_dir' 'dataset_name' 'dataset_url'
```
