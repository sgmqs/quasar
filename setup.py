from setuptools import setup, find_packages


setup(
    name="quasar",
    version="0.1.0",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'campaign_activity_backfill_since = quasar.etl.campaign_activity:backfill_since',
            'campaign_activity_full_backfill = quasar.etl.campaign_activity:full_backfill',
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