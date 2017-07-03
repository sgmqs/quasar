import logging

from .QuasarCampaignActivityParsing import RogueEtl

def main():
    log_format = "%(asctime)s - %(levelname)s: %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_format)

    CampaignActivityETL = RogueEtl()
    CampaignActivityETL.full_backfill()


if __name__ == "__main__":
    main():
