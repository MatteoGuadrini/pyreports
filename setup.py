from setuptools import setup


__version__ = '1.6.0'
__author__ = 'Matteo Guadrini'
__email__ = 'matteo.guadrini@hotmail.it'
__homepage__ = 'https://github.com/MatteoGuadrini/pyreports'

with open("README.md") as rme, open("CHANGES.md") as ch:
    long_description = rme.read() + "\n" + ch.read()

setup(
    name='pyreports',
    version=__version__,
    packages=['pyreports'],
    url=__homepage__,
    license='GNU General Public License v3.0',
    author=__author__,
    author_email=__email__,
    keywords='pyreports reports report csv yaml export excel database ldap dataset file executor book',
    maintainer='Matteo Guadrini',
    maintainer_email='matteo.guadrini@hotmail.it',
    install_requires=['ldap3', 'pymssql', 'mysql-connector-python',
                      'psycopg2-binary', 'tablib', 'tablib[all]', 'nosqlapi', 'pyyaml'],
    description='pyreports is a python library that allows you to create complex report from various sources',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
            "Operating System :: OS Independent",
        ],
    entry_points={
        'console_scripts': [
            'reports = pyreports.cli:main'
        ]
    },
    python_requires='>=3.7'
)
