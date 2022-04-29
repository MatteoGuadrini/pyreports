from setuptools import setup
import __info__

with open("README.md") as fh:
    long_description = fh.read()

setup(
    name='pyreports',
    version=__info__.__version__,
    packages=['pyreports'],
    url=__info__.__homepage__,
    license='GNU General Public License v3.0',
    author=__info__.__author__,
    author_email=__info__.__email__,
    keywords='pyreports reports report csv yaml export excel database ldap dataset file executor book',
    maintainer='Matteo Guadrini',
    maintainer_email='matteo.guadrini@hotmail.it',
    install_requires=['ldap3', 'pymssql', 'mysql-connector-python',
                      'psycopg2-binary', 'tablib', 'tablib[all]', 'nosqlapi'],
    description='pyreports is a python library that allows you to create complex report from various sources',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
            "Operating System :: OS Independent",
        ],
    python_requires='>=3.7'
)
