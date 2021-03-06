# -*- coding: utf-8 -*-
"""Click commands."""
import os

import click

import wave
from flask.cli import with_appcontext

from .extensions import db
from .models import Dataset, Label, AudioFile


HERE = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.join(HERE, os.pardir)
TEST_PATH = os.path.join(PROJECT_ROOT, "tests")

@click.command()
@click.option(
    "-p",
    "--dataset-dirpath",
    default='/static/dataset',
    is_flag=False,
    help="Dataset directory path",
)
@click.option(
    "-n",
    "--dataset-name",
    default='',
    is_flag=False,
    help="Dataset name",
)
@click.option(
    "-u",
    "--dataset-url",
    default='',
    is_flag=False,
    help="Dataset URL",
)
@with_appcontext
def load_dataset(dataset_dirpath, dataset_name, dataset_url):
    """
    Load a dataset into the application DB.
    :param dataset_dirpath: The directory location of the dataset
    :type dataset_dirpath: str
    :param dataset_name: The name of the dataset
    :type dataset_name: str
    :param dataset_url: An associated URL for the dataset (optional)
    :type dataset_url: str
    """
    print('loading dataset {}'.format(dataset_name))
    ds = Dataset(name=dataset_name, url=dataset_url)
    db.session.add(ds)
    db.session.commit()
    sub_dirs = [x for x in os.walk(dataset_dirpath)][1:]
    print(sub_dirs)
    #labels = [sd.split('/')[1]for sd[0] in sub_dirs]
    counter = 0
    for sd in sub_dirs:
        # create label
        label_name = sd[0].split('/')[2]
        print('working on label {}'.format(label_name))
        label = Label(name=label_name)
        db.session.add(label)
        db.session.commit()
        files = sd[2]
        for f in files:
            counter += 1
            # get name
            fname = label_name + '/' + f
            # get sample rate
            try:
                with wave.open(dataset_dirpath + '/' + fname, 'r') as ff:
                    sr = ff.getframerate()
                    print('sr: {}'.format(sr))
            except wave.Error as e:
                print('error: {}'.format(e))
                sr = 0
            # now add file to DB
            print('adding {} to db'.format(fname))
            db.session.add(AudioFile(name=fname,
                                     sample_rate=sr, dataset_id=ds.id,
                                     label_id=label.id))
            db.session.commit()
    print('Total files added to dataset: {}'.format(counter))

