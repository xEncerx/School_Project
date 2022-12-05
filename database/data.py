import sqlite3


class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()
        print("The database is connected successfully")

    def add_client(self, ID, time, username):
        with self.connection:
            try:
                self.cursor.execute("INSERT INTO 'client' VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (ID, 0, "client", time, "", "", "", username))
            except: pass

    def get_client_data(self, ID):
        return self.cursor.execute("SELECT * FROM 'client' WHERE user_id = ?", (ID,)).fetchmany()[0]

    def client_exist(self, ID):
        with self.connection:
            if str(ID).isdigit():
                result = self.cursor.execute("SELECT * FROM 'client' WHERE user_id = ?", (ID,)).fetchmany(1)
            else:
                result = self.cursor.execute("SELECT * FROM 'client' WHERE username = ?", (ID,)).fetchmany(1)
            if not bool(len(result)):
                return False
            return True

    def update_data(self, ID, data, value, table: str = "client", place: str = "user_id"):
        with self.connection:
            self.cursor.execute(f"""UPDATE {table} SET {data} = ? WHERE {place} = ?""", (value, ID))

    def add_shop_value(self, name: str, price: int):
        with self.connection:
            try:
                self.cursor.execute("INSERT INTO 'shop' VALUES (?, ?)", (name, price,))
            except: pass

    def get_shop_list(self):
        with self.connection:
            return self.cursor.execute("SELECT * FROM 'shop'").fetchall()

    def get_product_price(self, name):
        with self.connection:
            return self.cursor.execute("SELECT price FROM 'shop' WHERE name = ?", (name,)).fetchone()[0]

    def getAdmins(self):
        with self.connection:
            array = self.cursor.execute("SELECT user_id FROM 'client' WHERE role=?", ("admin",)).fetchall()
            return list(i[0] for i in array)

    def add_task_data(self, data, value):
        with self.connection:
            try:
                if self.cursor.execute("SELECT status FROM 'tasks' WHERE id=?", (self.cursor.execute("SELECT id FROM tasks").fetchall()[-1][0],)).fetchone()[0] != "published":
                    if len(self.cursor.execute("SELECT * FROM 'tasks' WHERE id=?", (self.cursor.execute("SELECT id FROM tasks").fetchall()[-1][0],)).fetchall()) >= 1:
                        self.cursor.execute(f"""UPDATE 'tasks' SET {data} = ? WHERE id=?""", (value, self.cursor.execute("SELECT id FROM tasks").fetchall()[-1][0],))
                    else:
                        self.cursor.execute(f"""INSERT INTO 'tasks' ({data}) VALUES (?)""", (value,))
                else:
                    self.cursor.execute(f"""INSERT INTO 'tasks' ({data}) VALUES (?)""", (value,))
            except: self.cursor.execute(f"""INSERT INTO 'tasks' ({data}) VALUES (?)""", (value,))

    def get_task_data(self, data, id: int = None):
        with self.connection:
            if id is not None:
                return self.cursor.execute(
                    f"""SELECT {data} FROM 'tasks' WHERE id={id}""").fetchone()[0]
            else:
                return self.cursor.execute(f"""SELECT {data} FROM 'tasks' WHERE id={self.cursor.execute("SELECT id FROM tasks").fetchall()[-1][0]}""").fetchone()[0]

    def delete_task(self):
        with self.connection:
            self.cursor.execute(f"""DELETE FROM 'tasks' WHERE id={self.cursor.execute("SELECT id FROM tasks").fetchall()[-1][0]}""")

    def get_all_users(self, limit):
        with self.connection:
            if limit is not None:
                return self.cursor.execute(f"""SELECT user_id FROM 'client' WHERE class=?""", (limit,)).fetchall()
            else:
                return self.cursor.execute(f"""SELECT user_id FROM 'client'""").fetchall()

    def get_last_task(self):
        with self.connection:
            return self.cursor.execute("SELECT id FROM tasks").fetchall()[-1][0]

    def get_leaderboard_data(self, data):
        with self.connection:
            return self.cursor.execute(f"""SELECT * FROM 'leaderboard' WHERE class={data}""").fetchall()
