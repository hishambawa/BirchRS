from setuptools import setup

setup(
    name='birchrs',
    version='1.0.0',
    packages=['birchrs'],
    package_dir={'':'src'},
    install_requires=[
        'numpy',
        'pandas==2.2.3',
        'scikit-learn==1.5.2',
        'structlog==24.4.0'
    ],
)