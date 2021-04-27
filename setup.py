'''
Setup file for MLmonitoring
'''

from setuptools import setup, find_packages
import mlmonitoring

setup(
    name='mlmonitoring',
    packages=find_packages(exclude=["tests", "tests.*"]),
    author='Rodrigo Azevedo',
    version='0.1',
    description='A Python module for monitoring machine learning models.',
    # long_description=open('README.md').read(),

    # Project's main homepage.
    url='https://github.com/rodrigoazs/monitoring',
    download_url="https://github.com/rodrigoazs/monitoring/archive/0.1.tar.gz",

    # Relevant keywords
    keywords='machine-learning artificial-intelligence data-science',

    # install_requires = ['sklearn', 'numpy', 'pandas', 'deap', 'joblib']

    install_requires=[
        'Click',
        'fastapi',
        'uvicorn==0.13.4',
        'pydantic==1.8.1',
        'llvmlite==0.31.0',
        'sqlalchemy',
        'sqlalchemy_utils',
        'psycopg2-binary',
        'pyod'
    ],

    entry_points='''
        [console_scripts]
        mlmonitoring=mlmonitoring.server.main:cli
    ''',
)
