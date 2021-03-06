from .database import Database, dec_to_float_converter
import re


def main():
    db = Database({'conv': dec_to_float_converter()})

    # Populate Array with all mobile values from Phoenix DB
    result = db.query(
        "SELECT * FROM dosomething.field_data_field_mobile WHERE field_mobile_value is NOT NULL")

    # Regex Checker to only allow numbers.
    check_for_num = re.compile('^[0-9]+$')

    for row in result:
        raw_phone_number = row['field_mobile_value'].replace(
            "-", "").replace("(", "").replace(")", "").replace(".", "").replace(" ", "")
        if (len(raw_phone_number.strip()) == 11 and raw_phone_number.startswith('1') and check_for_num.match(raw_phone_number) is not None):
            sanitized_phone_number = raw_phone_number[1:11]
            sanitized_phone_number_lookup = "SELECT * FROM users_and_activities.mobile_user_lookup as mu WHERE mu.us_phone_number = (\"{0}\")".format(
                sanitized_phone_number)
            mobile_query_result = db.query(sanitized_phone_number_lookup)
            if not mobile_query_result:
                print("No matching record for this phone number.")
            else:
                uid_check = mobile_query_result[0]['uid']
                if uid_check is None:
                    uid = row['entity_id']
                    update_query = "update users_and_activities.mobile_user_lookup set uid={0} where us_phone_number=\"{1}\"".format(
                        uid, sanitized_phone_number)
                    print(update_query)
                    db.query(update_query)
                else:
                    print("Already updated uid %s" % uid_check)
        elif (len(raw_phone_number.strip()) == 10 and check_for_num.match(raw_phone_number) is not None):
            sanitized_phone_number = raw_phone_number
            sanitized_phone_number_lookup = "SELECT * FROM users_and_activities.mobile_user_lookup as mu WHERE mu.us_phone_number = (\"{0}\")".format(
                sanitized_phone_number)
            mobile_query_result = db.query(sanitized_phone_number_lookup)
            if not mobile_query_result:
                print("No matching record for this phone number.")
            else:
                uid_check = mobile_query_result[0]['uid']
                if uid_check is None:
                    uid = row['entity_id']
                    update_query = "update users_and_activities.mobile_user_lookup set uid={0} where us_phone_number=\"{1}\"".format(
                        uid, sanitized_phone_number)
                    print(update_query)
                    db.query(update_query)
                else:
                    print("Already updated uid %s" % uid_check)
        else:
            print("%s is not a valid phone number" % raw_phone_number)

    db.disconnect()


if __name__ == "__main__":
    main()
