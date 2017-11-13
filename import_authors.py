import csv
import sys
import utils.db_util as db_util


def main():
    """
    Import author and n_number from csv to sqlite
    :return:
    """
    conn = db_util.create_connection(sys.argv[1])
    with open("csv/vivo_author_nnumber.csv", "rb") as authors_file:
        reader = csv.reader(authors_file)
        for row in reader:
            insert_person(conn, row)
    conn.commit()


def insert_person(conn, person):
    person_values = (person[0], person[2])
    sql = ''' INSERT INTO person(full_name, n_number)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, person_values)


if __name__ == '__main__':
    main()



