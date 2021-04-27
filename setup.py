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
        'pyhumps==1.6.1',
        'fastapi==0.63.0',
        'uvicorn==0.13.4',
        'pydantic==1.8.1',
        'psycopg2==2.8.6',
        'pandas==1.1.5',
        'sqlalchemy_utils==0.37.0',
        'pyod==0.8.8'
    ],

    entry_points='''
        [console_scripts]
        mlmonitoring=mlmonitoring.server.main:cli
    ''',
)
