from flask import Flask, jsonify, request
import mysql.connector
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

# Configurações do MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'students'

# Inicializa a conexão com o MySQL
mysql = mysql.connector.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    database=app.config['MYSQL_DB']
)

# ... (restante do seu código)

# Listar todos os estudantes
@app.route('/estudantes', methods=['GET'])
def listar_estudantes():
    """
    Rota para listar todos os estudantes.
    ---
    responses:
      200:
        description: Lista de estudantes
    """
    cur = mysql.cursor(dictionary=True)
    cur.execute("SELECT * FROM estudantes")
    estudantes = cur.fetchall()
    cur.close()
    return jsonify(estudantes)

# Obter um estudante pelo ID
@app.route('/estudantes/<int:id>', methods=['GET'])
def obter_estudante(id):
    """
    Rota para obter um estudante pelo ID.
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID do estudante a ser obtido
    responses:
      200:
        description: Informações do estudante
      404:
        description: Estudante não encontrado
    """
    cur = mysql.cursor(dictionary=True)
    cur.execute("SELECT * FROM estudantes WHERE id=%s", (id,))
    estudante = cur.fetchone()
    cur.close()
    if estudante:
        return jsonify(estudante)
    else:
        return jsonify({'message': 'Estudante não encontrado'}), 404

# Adicionar um novo estudante
@app.route('/estudantes', methods=['POST'])
def adicionar_estudante():
    """
    Rota para adicionar um novo estudante.
    ---
    parameters:
      - name: novo_estudante
        in: body
        required: true
        schema:
          type: object
          properties:
            nome:
              type: string
              description: Nome do estudante
            idade:
              type: integer
              description: Idade do estudante
            notaPrimeiroSemestre:
              type: number
              description: Nota do primeiro semestre
            notaSegundoSemestre:
              type: number
              description: Nota do segundo semestre
            nomeProfessor:
              type: string
              description: Nome do professor
            numeroSala:
              type: integer
              description: Número da sala
    responses:
      201:
        description: Estudante adicionado com sucesso
    """
    novo_estudante = request.get_json()
    cur = mysql.cursor()
    cur.execute("INSERT INTO estudantes (nome, idade, notaPrimeiroSemestre, notaSegundoSemestre, nomeProfessor, numeroSala) VALUES (%s, %s, %s, %s, %s, %s)",
                (novo_estudante['nome'], novo_estudante['idade'], novo_estudante['notaPrimeiroSemestre'], novo_estudante['notaSegundoSemestre'], novo_estudante['nomeProfessor'], novo_estudante['numeroSala']))
    mysql.commit()
    novo_estudante['id'] = cur.lastrowid
    cur.close()
    return jsonify(novo_estudante), 201

# Atualizar um estudante pelo ID
@app.route('/estudantes/<int:id>', methods=['PUT'])
def atualizar_estudante(id):
    """
    Rota para atualizar um estudante pelo ID.
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID do estudante a ser atualizado
      - name: dados_atualizados
        in: body
        required: true
        schema:
          type: object
          properties:
            nome:
              type: string
              description: Novo nome do estudante
            idade:
              type: integer
              description: Nova idade do estudante
            notaPrimeiroSemestre:
              type: number
              description: Nova nota do primeiro semestre
            notaSegundoSemestre:
              type: number
              description: Nova nota do segundo semestre
            nomeProfessor:
              type: string
              description: Novo nome do professor
            numeroSala:
              type: integer
              description: Novo número da sala
    responses:
      200:
        description: Estudante atualizado com sucesso
      404:
        description: Estudante não encontrado
    """
    cur = mysql.cursor(dictionary=True)
    cur.execute("SELECT * FROM estudantes WHERE id=%s", (id,))
    estudante = cur.fetchone()
    cur.close()
    if estudante:
        dados_atualizados = request.get_json()
        cur = mysql.cursor()
        cur.execute("UPDATE estudantes SET nome=%s, idade=%s, notaPrimeiroSemestre=%s, notaSegundoSemestre=%s, nomeProfessor=%s, numeroSala=%s WHERE id=%s",
                    (dados_atualizados['nome'], dados_atualizados['idade'], dados_atualizados['notaPrimeiroSemestre'], dados_atualizados['notaSegundoSemestre'], dados_atualizados['nomeProfessor'], dados_atualizados['numeroSala'], id))
        mysql.commit()
        cur.close()
        return jsonify(dados_atualizados)
    else:
        return jsonify({'message': 'Estudante não encontrado'}), 404

# Deletar um estudante pelo ID
@app.route('/estudantes/<int:id>', methods=['DELETE'])
def deletar_estudante(id):
    """
    Rota para deletar um estudante pelo ID.
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID do estudante a ser deletado
    responses:
      204:
        description: Estudante deletado com sucesso
      404:
        description: Estudante não encontrado
    """
    cur = mysql.cursor()
    cur.execute("DELETE FROM estudantes WHERE id=%s", (id,))
    mysql.commit()
    cur.close()
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
