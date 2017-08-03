import time
from .database import Database


def main():
    db = Database({'db': 'phoenix_user_snapshots'})

    snapshot_time = str(int(time.time()))

    # Create Table Schema Snapshot
    run_query = "CREATE TABLE IF NOT EXISTS phoenix_users_snapshot_" + \
        snapshot_time + """ LIKE dosomething.users"""
    db.query(run_query)

    # Insert Daily Data from DS Users Table
    run_query = "INSERT phoenix_users_snapshot_" + \
        snapshot_time + """ SELECT * FROM dosomething.users"""
    db.query(run_query)

    # Close Cursor and Connection
    db.disconnect

if __name__ == "__main__":
    main()
