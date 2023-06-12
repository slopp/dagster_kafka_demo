from setuptools import find_packages, setup

setup(
    name="kafkademo",
    packages=find_packages(exclude=["kafkademo_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud",
        "kafka-python"
    ],
    extras_require={"dev": ["dagit", "pytest"]},
)
