import logging

from QuasarCampaignActivityParsing import RogueEtl

if __name__ == "__main__":
    log_format = "%(asctime)s - %(levelname)s: %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_format)

    CampaignActivityETL = RogueEtl()
    CampaignActivityETL.backfill_since(sys.argv[1])
