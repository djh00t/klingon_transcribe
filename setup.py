from setuptools import setup, find_packages

setup(
    name='klingon_transcribe',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'boto3',
        'click',
        'cython',
        'fastapi',
        'flake8',
        'hydra-core',
        'librosa',
        'nemo_toolkit[all]',
        'numba',
        'numpy',
        'pandas',
        'pdoc',
        'onnx==1.16.1',
        'protobuf<=3.20.2',
        'pytest>=7.2.0',
        'python-dotenv',
        'pytorch-lightning>=1.6.0',
        'requests',
        'torch',
        'torchaudio',
        'torchvision',
        'uvicorn',
        'youtokentome',
        'einops'
    ],
    entry_points={
        'console_scripts': [
            'klingon_transcribe=klingon_transcribe.cli:cli',
        ],
    },
)
