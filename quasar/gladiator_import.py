import sys

from .config import config
from .database import Database
from .scraper import Scraper
from .utils import strip_str, QuasarException, Duration


class GladiatorDB:
    def __init__(self):
        db_opts = {'use_unicode': True, 'charset': 'utf8'}
        self.db = Database(db_opts)

    def teardown(self):
        self.db.disconnect()

    def _save_competition(self, *competition):
        self.db.query_str("REPLACE INTO gladiator.competitions (id,\
                          leaderboard_msg_day, rules, created_at, updated_at,\
                          competition_dates_start, competition_dates_end,\
                          contest_id) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",
                          (strip_str(competition[0]),
                           strip_str(competition[1]),
                           competition[2],
                           strip_str(competition[3]),
                           strip_str(competition[4]),
                           strip_str(competition[5]),
                           strip_str(competition[6]),
                           strip_str(competition[7])))

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

    def _save_messages(self, *messages):
        self.db.query_str("REPLACE INTO gladiator.messages (id,\
                          contest_id, label, subject, body, signoff,\
                          protip, show_images, created_at, updated_at,\
                          type_name, type_key) VALUES(%s,%s,%s,%s,%s,%s,\
                          %s,%s,%s,%s,%s,%s)",
                          (strip_str(messages[0]),
                           strip_str(messages[1]),
                           messages[2],
                           messages[3],
                           messages[4],
                           messages[5],
                           messages[6],
                           messages[7],
                           strip_str(messages[8]),
                           strip_str(messages[9]),
                           strip_str(messages[10]),
                           strip_str(messages[11])))

    def _save_user(self, *user):
        self.db.query_str("REPLACE INTO gladiator.users (user_id,\
                          contest_id, campaign_id, subscribed,\
                          unsubscribed, waiting_room_id) \
                          VALUES(%s,%s,%s,%s,%s,%s)",
                          (user[0],
                           user[1],
                           user[2],
                           user[3],
                           user[4],
                           user[5]))

    def _save_waiting_room(self, *waiting_room):
        self.db.query_str("REPLACE INTO gladiator.waiting_room (id,\
                           open, created_at, updated_at, contest_id,\
                           signup_date_start, signup_date_end) \
                           VALUES (%s,%s,%s,%s,%s,%s,%s)",
                          (waiting_room[0],
                           waiting_room[1],
                           waiting_room[2],
                           waiting_room[3],
                           waiting_room[4],
                           waiting_room[5],
                           waiting_room[6]))


def get_competitions():
    duration = Duration()
    db = GladiatorDB()
    scraper = Scraper(config.gladiator_uri)
    start_page = 1
    end_page = scraper.getJson(
        '/api/v2/contests')['meta']['pagination']['total_pages']
    while start_page <= end_page:
        try:
            page = scraper.getJson('/api/v2/contests',
                                   params={'page': start_page})
            db._save_contest(page['data'][0]['id'],
                             page['data'][0]['campaign_id'],
                             page['data'][0]['campaign_run_id'],
                             page['data'][0]['created_at'],
                             page['data'][0]['updated_at'],
                             page['data'][0]['sender']['name'],
                             page['data'][0]['sender']['email'])
            for competition in page['data'][0]['competitions']['data']:
                db._save_competition(competition['id'],
                                     competition['leaderboard_msg_day'],
                                     competition['rules'],
                                     competition['created_at'],
                                     competition['updated_at'],
                                     competition['competition_dates'][
                                         'start_date'],
                                     competition['competition_dates'][
                                         'end_date'],
                                     page['data'][0]['id'])
                for user in competition['users']:
                    db._save_user(user,
                                  page['data'][0]['id'],
                                  page['data'][0]['campaign_id'],
                                  1, None, None)
                for user in competition['unsubscribed_users']:
                    db._save_user(user,
                                  page['data'][0]['id'],
                                  page['data'][0]['campaign_id'],
                                  None, 1, None)
            for user in page['data'][0]['waitingRoom']['data']['users']:
                db._save_user(user,
                              page['data'][0]['id'],
                              page['data'][0]['campaign_id'],
                              None, None,
                              page['data'][0]['waitingRoom']['data']['id'])
            for messages in page['data'][0]['messages']['data']:
                db._save_messages(messages['id'],
                                  page['data'][0]['id'],
                                  messages['label'],
                                  messages['subject'],
                                  messages['body'],
                                  messages['signoff'],
                                  messages['pro_tip'],
                                  messages['show_images'],
                                  messages['created_at'],
                                  messages['updated_at'],
                                  messages['type']['name'],
                                  messages['type']['key'])
            db._save_waiting_room(page['data'][0]['waitingRoom']['data']['id'],
                                  page['data'][0]['waitingRoom']['data']['open'],
                                  page['data'][0]['waitingRoom']['data']['created_at'],
                                  page['data'][0]['waitingRoom']['data']['updated_at'],
                                  page['data'][0]['id'],
                                  page['data'][0]['waitingRoom']['data']['signup_dates']['start'],
                                  page['data'][0]['waitingRoom']['data']['signup_dates']['end'])
        except:
            QuasarException(sys.exc_info()[0])
        start_page += 1
    db.teardown()
    duration.duration()

if __name__ == "__main__":
    get_competitions()
