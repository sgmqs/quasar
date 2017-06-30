from setuptools import setup, find_packages


setup(
    name="quasar",
    version="0.1.0",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'moco_update = quasar.etl.mobile_commons_campaign_scraper:main'
        ],
    },
    author="",
    author_email="",
    description="",
    license="MIT",
    keywords=[],
    url="",
    classifiers=[
    ],
)