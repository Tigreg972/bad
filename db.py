import mysql.connector
import hashlib

class Database:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def connect(self):
        return mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )

    def log(self, request):
        try:
            auth = request.authorization
            if not auth:
                return {"message": "Aucune information d'authentification fournie"}, 401

            username = auth.username
            password = auth.password

            if self.is_sql_injection(username) or self.is_sql_injection(password):
                if username not in self.attempt_tracker:
                    self.attempt_tracker[username] = 1
                    return {"message": "Essaye encore"}, 403
                else:
                    self.attempt_tracker[username] += 1
                    attempt_count = self.attempt_tracker[username]

                    if attempt_count == 2:
                        return {"message": "Tu y es presque"}, 403
                    elif attempt_count == 3:
                        return {"message": "La prochaine est la bonne"}, 403
                    elif attempt_count >= 4:
                        return {"message": "Dommage, tu y étais presque mais tu ne pourras pas rentrer"}, 403

            password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()

            with self.connect() as conn:
                with conn.cursor() as cursor:
                    query = "SELECT * FROM user WHERE login = %s AND password = %s"
                    cursor.execute(query, (username, password_hash))
                    data = cursor.fetchone()

            if data:
                if username in self.attempt_tracker:
                    del self.attempt_tracker[username]
                return data
            else:
                return 401

        except Exception as e:
            print(f"Erreur dans log : {e}")
            return {"message": "Erreur serveur, veuillez réessayer plus tard"}, 500

    @staticmethod
    def is_sql_injection(value):
        injection_patterns = ["'", '"', ";", "--", "/*", "*/", "OR 1=1", "DROP", "SELECT", "INSERT", "UPDATE", "DELETE"]
        for pattern in injection_patterns:
            if pattern in value.upper():
                return True
        return False

    def readAll(self):
        conn = self.connect()
        cursor = conn.cursor()
        query = "SELECT * FROM etudiant"
        cursor.execute(query)
        data = cursor.fetchall()
        conn.close()
        return data

    def readOne(self, id):
        conn = self.connect()
        cursor = conn.cursor()
        query = "SELECT * FROM etudiant WHERE idetudiant = %s"
        cursor.execute(query, (id,))
        data = cursor.fetchone()
        conn.close()
        return data

    def addEtudiant(self, nom, prenom, email, telephone):
        conn = self.connect()
        cursor = conn.cursor()
        query = """
        INSERT INTO etudiant (nom, prenom, email, telephone) 
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (nom, prenom, email, telephone))
        conn.commit()
        last_id = cursor.lastrowid
        conn.close()
        return last_id

    def updateEtudiant(self, id, nom, prenom, email, telephone):
        conn = self.connect()
        cursor = conn.cursor()
        query = """
        UPDATE etudiant
        SET nom = %s, prenom = %s, email = %s, telephone = %s
        WHERE idetudiant = %s
        """
        cursor.execute(query, (nom, prenom, email, telephone, id))
        conn.commit()
        affected_rows = cursor.rowcount
        conn.close()
        return affected_rows

    def deleteEtudiant(self, id):
        conn = self.connect()
        cursor = conn.cursor()
        query = "DELETE FROM etudiant WHERE idetudiant = %s"
        cursor.execute(query, (id,))
        conn.commit()
        rows_deleted = cursor.rowcount
        conn.close()
        return rows_deleted

    def authorized(self, request):
        try:
            auth = request.authorization
            if not auth:
                return False

            username = auth.username
            password = auth.password
            password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()

            with self.connect() as conn:
                with conn.cursor() as cursor:
                    query = "SELECT password FROM user WHERE login = %s"
                    cursor.execute(query, (username,))
                    data = cursor.fetchone()

            if data:
                return password_hash == data[0]
            return False
        except Exception as e:
            print(f"Erreur dans authorized : {e}")
            return False
