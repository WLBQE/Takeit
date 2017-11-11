from app import db


def run_sql_file(filename):
    with open(filename, 'r') as sqlfile:
        sql = " ".join(sqlfile.readlines())
        connection = db.connect()
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
        connection.close()

if __name__ == '__main__':
    run_sql_file('create.sql')
    run_sql_file('fake_data.sql')
