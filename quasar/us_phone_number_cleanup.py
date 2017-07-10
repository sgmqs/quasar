import sys
from .config import config
from . import database


def main():
    db, cur = database.connect({'conv': database.dec_to_float_converter()})

    # Get all records missing a us_phone_number value
    cur.execute(
        "SELECT * FROM users_and_activities.mobile_user_lookup WHERE us_phone_number IS NULL")
    result = cur.fetchall()

    for row in result:
        test_number = row['phone_number']

        # We're only interested in numbers where we can strip out a prepended
        # "1" and end up with a ten-digit number.
        if len(test_number.strip()) == 11 and test_number.startswith('1'):
            us_phone_number = test_number[1:11]
            print("Updating %s" % us_phone_number)
            insert_statement = "UPDATE users_and_activities.mobile_user_lookup SET us_phone_number=\"{0}\" WHERE phone_number=\"{1}\"".format(
                us_phone_number, test_number)
            cur.execute(insert_statement)
            db.commit()
        else:
            print("Skipping {0}: Can't format as US number".format(test_number))

    cur.close()
    db.close()

if __name__ == "__main__":
    main()
