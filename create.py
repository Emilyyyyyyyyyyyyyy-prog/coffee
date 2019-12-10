import sqlite3
from sqlite3 import Error


def sql_connection():
    try:
        con = sqlite3.connect('coffee.sqlite')
        return con
    except Error:
        print(Error)


def sql_table(con):
    cur = con.cursor()
    cur.execute("CREATE TABLE coffee(id integer PRIMARY KEY, sort text, roasting text,"
                " ground text, taste text, price integer, volume integer)")
    cur.execute("INSERT INTO coffee VALUES('1', 'Nescafe Gold', 'средняя',"
                " 'молотый', 'глубокий', '300', '200')")
    cur.execute("INSERT INTO coffee VALUES('2', 'Jardin', 'светлая',"
                " 'зерно', 'насыщенный', '700', '1000')")
    cur.execute("INSERT INTO coffee VALUES('3', 'Paulig', 'сильная',"
                " 'молотый', 'яркий', '500', '400')")
    con.commit()
    con.close()


con = sql_connection()
sql_table(con)
