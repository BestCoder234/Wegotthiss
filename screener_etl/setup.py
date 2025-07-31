from setuptools import find_packages, setup

setup(
    name="screener_etl",
    packages=find_packages(exclude=["screener_etl_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud"
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
