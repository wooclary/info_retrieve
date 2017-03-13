import sys
from setuptools import setup, find_packages

install_requires = [
    'beautifulsoup4',
    'Flask',
    'Flask-WTF',
    'Flask-Script',
    'Flask-Bootstrap',
    'scikit-learn',
    'numpy',
    'requests',
    'lxml'
]
if sys.version_info < (3, 2):
    install_requires.append('futures')

setup(
    name="info-retrieve",
    version="1.0.0",
    license='Private',
    description="link extraction research",
    packages=find_packages('.'),
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'tagger = tagger.manage:main',
        ],
    },
)