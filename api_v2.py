from flask import Flask, jsonify, request
import mysql.connector

mydb = mysql.connector.connect(
    host="",
    user="extern_user",
    password="bt5@c13l972",
    database="ciel2025"
)
cursor = mydb.cursor()

app = Flask(__name__)


class CustomErrorHandler(Exception):
    status_code = 500

    def __init__(self, message, status_code=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        return {'message': self.message}


@app.errorhandler(CustomErrorHandler)
def handle_custom_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"message": "Ressource non trouvée"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"message": "Erreur interne du serveur"}), 500


@app.route('/v2/etudiants/', methods=['GET'])
def getAllEtudiants():
    try:
        cursor.execute("SELECT * FROM etudiant")
        rows = cursor.fetchall()
        etudiants = []
        
        for row in rows:
            etudiant = {
                "idetudiant": row[0],
                "nom": row[1],
                "prenom": row[2],
                "email": row[3],
                "telephone": row[4],
            }
            etudiants.append(etudiant)
        
        return jsonify(etudiants), 200

    except mysql.connector.Error as e:
        raise CustomErrorHandler(f"Erreur de base de données : {str(e)}", 500)

@app.route('/v2/etudiants/<int:id>', methods=['GET'])
def getEtudiant(id):
    req = "SELECT * FROM etudiant WHERE idetudiant = %s"
    try:
        cursor.execute(req, (id,))
        row = cursor.fetchone()
        if row is None:
            raise CustomErrorHandler("Étudiant non trouvé", 404)
        
        etudiant = {
            "idetudiant": row[0],
            "nom": row[1],
            "prenom": row[2],
            "email": row[3],
            "telephone": row[4],
        }
        return jsonify(etudiant), 200
    
    except mysql.connector.Error as e:
        raise CustomErrorHandler(f"Erreur de base de données : {str(e)}", 500)

@app.route('/v2/etudiants/', methods=['POST'])
def addEtudiant():
    try:
        data = request.json
        nom = data.get('nom')
        prenom = data.get('prenom')
        email = data.get('email')
        telephone = data.get('telephone')

        if not all([nom, prenom, email, telephone]):
            raise CustomErrorHandler("Tous les champs sont requis.", 400)

        req = "INSERT INTO etudiant (nom, prenom, email, telephone) VALUES (%s, %s, %s, %s)"
        cursor.execute(req, (nom, prenom, email, telephone))
        mydb.commit()

        return jsonify({"message": "Étudiant ajouté avec succès."}), 201

    except mysql.connector.Error as e:
        raise CustomErrorHandler(f"Erreur de base de données : {str(e)}", 500)

@app.route('/v2/etudiants/<int:id>', methods=['PUT'])
def updateEtudiant(id):
    try:
        data = request.json
        nom = data.get('nom')
        prenom = data.get('prenom')
        email = data.get('email')
        telephone = data.get('telephone')

        req = """
            UPDATE etudiant 
            SET nom = %s, prenom = %s, email = %s, telephone = %s
            WHERE idetudiant = %s
        """
        cursor.execute(req, (nom, prenom, email, telephone, id))
        mydb.commit()

        if cursor.rowcount == 0:
            raise CustomErrorHandler("Étudiant non trouvé", 404)

        return jsonify({'message': 'Étudiant mis à jour avec succès'}), 200

    except mysql.connector.Error as e:
        mydb.rollback()
        raise CustomErrorHandler(f"Erreur de base de données : {str(e)}", 500)

@app.route('/v2/etudiants/<int:id>', methods=['DELETE'])
def deleteEtudiant(id):
    try:
        cursor.execute("SELECT * FROM etudiant WHERE idetudiant = %s", (id,))
        row = cursor.fetchone()

        if row is None:
            raise CustomErrorHandler("Étudiant non trouvé", 404)

        cursor.execute("DELETE FROM etudiant WHERE idetudiant = %s", (id,))
        mydb.commit()

        return jsonify({'message': 'Étudiant supprimé avec succès'}), 200

    except mysql.connector.Error as e:
        mydb.rollback()
        raise CustomErrorHandler(f"Erreur de base de données : {str(e)}", 500)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
