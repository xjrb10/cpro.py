from setuptools import find_packages, setup

setup(
    name="cpro.py",
    packages=find_packages(include=["cpro"]),
    version="0.0.1",
    description="Clear and concise CoinsPro API library written in Python for coins.ph",
    author="xjrb10",
    license="GPLv3",
    install_requires=[
        "aiohttp~=3.8.5",
        "dataclasses-json~=0.5.14"
    ],
    extras_require={
        "test": [
            "pytest==7.4.0",
            "pytest-dotenv==0.5.2",
            "pytest-asyncio==0.21.1",
            "pytest-runner==6.0.0"
        ]
    }
)
