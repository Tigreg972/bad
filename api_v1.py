from flask import Flask , jsonify , request
import mysql.connector

mydb = mysql.connector.connect(
    host = "127.0.0.1",
    user = "root",
    password = "",
    database = "ciel2025"
)
cursor = mydb.cursor()

    

app = Flask(__name__)


@app.route('/v1/etudiants/<int:id>', methods=['GET'])
def getEtudiants(id):
    req = f"SELECT * FROM etudiant WHERE idetudiant = " + str(id)
    print (req)
    cursor.execute(req)
    row = cursor.fetchone()
    etudiant = {
        "idetudiant": row[0],
        "nom": row[1],
        "prenom": row[2],
        "email": row[3],
        "telephone": row[4],
    }
    return jsonify(etudiant), 200

@app.route('/v1/etudiants/', methods=['GET'])
def getAllEtudiants():
    cursor.execute(f"SELECT * FROM etudiant")
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

@app.route('/v1/etudiants/', methods=['POST'])
def addEtudiant():
    nom = request.json['nom']
    prenom = request.json['prenom']
    email = request.json['email']
    telephone = request.json['telephone']
    req = f"INSERT INTO etudiant (nom, prenom, email, telephone) \
        VALUES ('{nom}','{prenom}','{email}','{telephone}')"
    cursor.execute(req)
    mydb.commit()
    return req , 201

@app.route('/v1/etudiants/<int:id>', methods=['PUT'])
def updateEtudiant(id):
    data = request.json
    nom = data.get('nom')
    prenom = data.get('prenom')
    email = data.get('email')
    telephone = data.get('telephone')
    
    req = f"""
        UPDATE etudiant 
        SET nom = %s, prenom = %s, email = %s, telephone = %s
        WHERE idetudiant = %s
    """
    cursor.execute(req, (nom, prenom, email, telephone, id))
    mydb.commit()
    
    if cursor.rowcount == 0:
        return jsonify({'message': 'Étudiant non trouvé'}), 404
    
    return jsonify({'message': 'Étudiant mis à jour avec succès'}), 200

@app.route('/v1/etudiants/<int:id>', methods=['DELETE'])
def deleteEtudiant(id):
    cursor.execute(f"SELECT * FROM etudiant WHERE idetudiant = %s", (id,))
    row = cursor.fetchone()
    
    if row is None:
        return jsonify({'message': 'Étudiant non trouvé'}), 404 

    cursor.execute(f"DELETE FROM etudiant WHERE idetudiant = %s", (id,))
    mydb.commit()

    return jsonify({'message': 'Étudiant supprimé avec succès'}), 200

if __name__ == "__main__":
    app.run(host= "0.0.0.0", debug=True)