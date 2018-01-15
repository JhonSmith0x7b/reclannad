#-*- coding:utf-8 -*-
import sqlite3



def main():
    old_db = sqlite3.connect('/Users/jhonsmith/develop/workspace/python_workspace/reclannad/app/tiebasearch/static/db/tiebadata_db.db')
    old_cursor = old_db.cursor()
    old_db.text_factory = bytes 
    old_data = old_cursor.execute('select * from tiebadata_table')
    new_db = sqlite3.connect('/Users/jhonsmith/develop/workspace/python_workspace/reclannad/app/tiebasearch/static/db/new_tiebadata_db.db')
    create_table_sql = """
    CREATE TABLE tiebadata_table (id  INTEGER,author TEXT, date TEXT, href TEXT, times INTEGER, title TEXT)
    """
    new_cursor = new_db.cursor()
    new_cursor.execute(create_table_sql)
    new_db.commit()
    for row in old_data:
        try:
            new_cursor.execute('insert into tiebadata_table(id, author, date, href, times, title) values(?, ?, ?, ?, ?, ? )',
                            (row[0], 
                            row[1].decode('gbk'), 
                            row[2].decode('gbk'), 
                            row[3].decode('gbk'), 
                            row[4], 
                            row[5].decode('gbk'),))
            new_db.commit()
        except Exception as e:
            print(str(e))
            print(row)










if __name__ == '__main__':
    main()