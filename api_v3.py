from flask import Flask, jsonify, request
from db import Database

app = Flask(__name__)

db = Database("127.0.0.1", "root", "", "ciel2025")


@app.route('/login', methods=['GET'])
def login():
    try:
        response = db.log(request)

        if isinstance(response, dict) and "message" in response:
            return jsonify(response), 403

        elif isinstance(response, tuple):
            user = {
                "id": response[0],
                "username": response[1]
            }
            return jsonify(user), 200

        elif response == 401:
            return jsonify({"message": "Accès non autorisé"}), 401

        else:
            return jsonify({"message": "Erreur serveur, veuillez réessayer plus tard"}), 500

    except Exception as e:
        print(f"Erreur dans /login : {e}")
        return jsonify({"message": "Erreur serveur, veuillez réessayer plus tard"}), 500


@app.route('/v3/etudiants/', methods=['GET'])
def getEtudiants():
    if not db.authorized(request):
        return jsonify({"message": "Accès non autorisé"}), 401

    try:
        etudiants = []
        result = db.readAll()
        for row in result:
            etudiant = {
                "idetudiant": row[0],
                "nom": row[1],
                "prenom": row[2],
                "email": row[3],
                "telephone": row[4]
            }
            etudiants.append(etudiant)
        return jsonify(etudiants), 200
    except Exception as e:
        return jsonify({"message": f"Erreur lors de la récupération des étudiants : {str(e)}"}), 500


@app.route('/v3/etudiants/<int:id>', methods=['GET'])
def getEtudiant(id):
    if not db.authorized(request):
        return jsonify({"message": "Accès non autorisé"}), 401

    try:
        row = db.readOne(id)
        if row is None:
            return jsonify({"message": "Étudiant non trouvé"}), 404

        etudiant = {
            "idetudiant": row[0],
            "nom": row[1],
            "prenom": row[2],
            "email": row[3],
            "telephone": row[4]
        }
        return jsonify(etudiant), 200
    except Exception as e:
        return jsonify({"message": f"Erreur lors de la récupération de l'étudiant : {str(e)}"}), 500


@app.route('/v3/etudiants/', methods=['POST'])
def addEtudiant():
    if not db.authorized(request):
        return jsonify({"message": "Accès non autorisé"}), 401

    data = request.get_json()
    nom = data.get('nom')
    prenom = data.get('prenom')
    email = data.get('email')
    telephone = data.get('telephone')

    if not (nom and prenom and email and telephone):
        return jsonify({"message": "Tous les champs sont obligatoires"}), 400

    try:
        new_id = db.addEtudiant(nom, prenom, email, telephone)
        return jsonify({"message": "Étudiant ajouté", "id": new_id}), 201
    except Exception as e:
        return jsonify({"message": f"Erreur lors de l'ajout de l'étudiant : {str(e)}"}), 500


@app.route('/v3/etudiants/<int:id>', methods=['DELETE'])
def deleteEtudiant(id):
    if not db.authorized(request):
        return jsonify({"message": "Accès non autorisé"}), 401

    try:
        rows_deleted = db.deleteEtudiant(id)
        if rows_deleted == 0:
            return jsonify({"message": f"Aucun étudiant trouvé avec l'ID {id}"}), 404

        return jsonify({"message": f"Étudiant avec l'ID {id} a été supprimé avec succès."}), 200
    except Exception as e:
        return jsonify({"message": f"Erreur lors de la suppression de l'étudiant : {str(e)}"}), 500


@app.route('/v3/etudiants/<int:id>', methods=['PUT'])
def updateEtudiant(id):
    if not db.authorized(request):
        return jsonify({"message": "Accès non autorisé"}), 401

    data = request.get_json()
    nom = data.get('nom')
    prenom = data.get('prenom')
    email = data.get('email')
    telephone = data.get('telephone')

    if not (nom and prenom and email and telephone):
        return jsonify({"message": "Tous les champs sont obligatoires"}), 400

    try:
        affected_rows = db.updateEtudiant(id, nom, prenom, email, telephone)
        if affected_rows == 0:
            return jsonify({'message': 'Étudiant non trouvé'}), 404

        return jsonify({'message': 'Étudiant mis à jour avec succès'}), 200
    except Exception as e:
        return jsonify({"message": f"Erreur lors de la mise à jour de l'étudiant : {str(e)}"}), 500

if __name__ == "__main__":
    cert_file = "certs/www.monsite.fr.crt"
    key_file = "certs/www.monsite.fr.key"
    app.run(host="0.0.0.0", port=5000, debug=True, ssl_context=(cert_file, key_file))
