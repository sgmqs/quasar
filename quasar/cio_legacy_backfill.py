from .database import Database
from .utils import strip_str


db = Database()


def update_users():
    backlog = db.query("SELECT * FROM cio.legacy_sub_backlog")
    for entry in backlog:
        nsid = db.query_str(''.join(("SELECT northstar_id FROM quasar.users "
                                     "WHERE northstar_id = %s")),
                            (entry[2],))
        if strip_str(nsid) != "":
            db.query_str(''.join(("UPDATE quasar.users SET "
                                  "customer_io_subscription_status = %s, "
                                  "customer_io_subscription_timestamp = %s "
                                  "WHERE northstar_id = %s")),
                         (entry[0], entry[1], entry[2]))
            db.query_str(''.join(("DELETE FROM cio.legacy_sub_backlog "
                                  "WHERE northstar_id = %s")),
                         (entry[2],))
            print("Northstar ID {} c.io status updated.".format(entry[2]))
        else:
            print("Northstar ID {} staying in backlog.".format(entry[2]))


def legacy_cio_backfill():
    update_users()
