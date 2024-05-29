from setuptools import setup, find_packages

setup(
    name='klingon_transcribe',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'click',
        'fastapi',
        'uvicorn',
        'boto3',
        'requests',
        'nemo_toolkit',
        'pdoc',
        'pytest',
        'flake8',
        'python-dotenv',
        'protobuf<=3.20.1'
    ],
    entry_points={
        'console_scripts': [
            'klingon_transcribe=klingon_transcribe.cli:cli',
        ],
    },
)
