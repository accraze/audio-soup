import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import wave

from app import app
from extensions import db
from models import *


app.config.from_object(os.environ['APP_SETTINGS'])

#db = db.init_app(app)

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


@manager.command
def load_dataset(dataset_dirpath, dataset_name, dataset_url):
    print('loading dataset {}'.format(dataset_name))
    ds = Dataset(name=dataset_name, url=dataset_url)
    db.session.add(ds)
    db.session.commit()
    sub_dirs = [x for x in os.walk(dataset_dirpath)][1:]
    #labels = [sd.split('/')[1]for sd[0] in sub_dirs]
    counter=  0
    for sd in sub_dirs:
        # create label
        label_name = sd[0].split('/')[1]
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

if __name__ == '__main__':
    manager.run()
