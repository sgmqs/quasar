import time

from .config import config
from .database import Database
from .scraper import Scraper
from .utils import strip_str

class GladitorDB:

	def __init__(self):
		db_opts = {'use_unicode': True, 'charset': 'utf8'}
		self.db = Database(db_opts)

	def teardown(self):
		self.db.disconnect()

	def _save_competition(self, competition):
		db.querystr(table, competition)
		#STUB

	def _save_contest(self, *contest):
		self.db.query_str("REPLACE INTO gladiator.contest (id,\
						  campaign_id, campaign_run_id, created_at,\
						  updated_at, sender_name, sender_email) \
			         	  VALUES(%s,%s,%s,%s,%s,%s,%s)",
			         	  (strip_str(contest[0]),
			          	   strip_str(contest[1]),
			               strip_str(contest[2]),
			               strip_str(contest[3]),
			               strip_str(contest[4]),
			               strip_str(contest[5]),
			               strip_str(contest[6])))

	def _save_messages(self, messages):
		db.querystr(table, messages)
		#STUB

	def _save_user(self, user):
		db.querystr(table, user)
		#STUB

	def _save_waiting_room(self, waiting_room):
		db.querystr(table, waiting_room)
		#STUB

def get_competitions():
	db = GladitorDB()
	scraper = Scraper(config.gladiator_uri)
	start_page = 1
	end_page = scraper.getJson('/api/v2/contests')['meta']['pagination']['total_pages']
	while start_page <= end_page:
		if start_page == 22 or start_page == 37:
			pass
		else:
			page = scraper.getJson('/api/v2/contests', params={'page': start_page})
			db._save_contest(page['data'][0]['id'],
							 page['data'][0]['campaign_id'],
							 page['data'][0]['campaign_run_id'],
							 page['data'][0]['created_at'],
							 page['data'][0]['updated_at'],
							 page['data'][0]['sender']['name'],
							 page['data'][0]['sender']['email'])

		start_page += 1

if __name__ == "__main__":
    get_competitions()