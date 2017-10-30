import utils.db_util as db_util
import csv


def main():
    conn = db_util.create_connection("db/kakapo.db")
    with open("csv/vivo_author_nnumber.csv", "rb") as authors_file:
        reader = csv.reader(authors_file)
        for row in reader:
            insert_person(conn, row)
    conn.commit()


def insert_person(conn, person):
    person_values = (person[0], person[2])
    sql = ''' INSERT INTO PERSON(N_NUMBER,FULL_NAME)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, person_values)


if __name__ == '__main__':
    main()



