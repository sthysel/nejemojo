from glob import glob
from os.path import basename
from os.path import splitext

from setuptools import setup, find_packages

setup(
    name='nejemojo',
    version='0.0.1',
    entry_points={
        'console_scripts': [
            'nejemojo=cli:neje',
            'nejeview=cli:view',
        ]
    },
    install_requires=[
        'click',
        'pillow',
        'pyserial',
    ],
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
)
