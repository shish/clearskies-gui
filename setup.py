import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()
CHANGES = ""  # open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'clearskies',
]

setup(
    name='csgui',
    version="0.0.0",
    description='A simple GUI for ClearSkies',
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
        "Programming Language :: Python",
    ],
    author='Shish',
    author_email='shish+clsk@shishnet.org',
    url='https://github.com/shish/csgui',
    keywords='clearskies',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    test_suite='csgui',
    install_requires=requires,
    entry_points="""\
    [console_scripts]
    csgui = csgui:main
    """,
)
