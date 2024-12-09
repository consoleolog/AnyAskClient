from setuptools import setup, find_packages


setup(
    name="anyaskClient",
    version="0.0.1",
    packages=find_packages(include=['anyaskClient', 'anyaskClient.*']),
    install_requires=[
        'streamlit',
        'requests'
    ]
)