from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///university.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Professor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

class Disciplina(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(10), unique=True, nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    carga_horaria = db.Column(db.Integer, nullable=False)

class Aptidao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    professor_id = db.Column(db.Integer, db.ForeignKey('professor.id'), nullable=False)
    disciplina_id = db.Column(db.Integer, db.ForeignKey('disciplina.id'), nullable=False)

class Turma(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    professor_id = db.Column(db.Integer, db.ForeignKey('professor.id'), nullable=False)
    disciplina_id = db.Column(db.Integer, db.ForeignKey('disciplina.id'), nullable=False)
    codigo_turma = db.Column(db.String(10), nullable=False)
    semestre = db.Column(db.String(10), nullable=False)
    numero_alunos = db.Column(db.Integer, nullable=False)
    horario = db.Column(db.String(10), nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

# Professores
@app.route('/professores')
def listar_professores():
    professores = Professor.query.all()
    return render_template('professores.html', professores=professores)

@app.route('/professor/novo', methods=['GET', 'POST'])
def novo_professor():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        professor = Professor(nome=nome, email=email)
        db.session.add(professor)
        db.session.commit()
        return redirect(url_for('listar_professores'))
    return render_template('form_professor.html')

# Disciplinas
@app.route('/disciplinas')
def listar_disciplinas():
    disciplinas = Disciplina.query.all()
    return render_template('disciplinas.html', disciplinas=disciplinas)

@app.route('/disciplina/nova', methods=['GET', 'POST'])
def nova_disciplina():
    if request.method == 'POST':
        codigo = request.form['codigo']
        nome = request.form['nome']
        carga_horaria = request.form['carga_horaria']
        disciplina = Disciplina(codigo=codigo, nome=nome, carga_horaria=carga_horaria)
        db.session.add(disciplina)
        db.session.commit()
        return redirect(url_for('listar_disciplinas'))
    return render_template('form_disciplina.html')

# Aptidões
@app.route('/aptidoes')
def listar_aptidoes():
    aptidoes = Aptidao.query.all()
    return render_template('aptidoes.html', aptidoes=aptidoes)

@app.route('/aptidao/nova', methods=['GET', 'POST'])
def nova_aptidao():
    if request.method == 'POST':
        professor_id = request.form['professor_id']
        disciplina_id = request.form['disciplina_id']
        aptidao = Aptidao(professor_id=professor_id, disciplina_id=disciplina_id)
        db.session.add(aptidao)
        db.session.commit()
        return redirect(url_for('listar_aptidoes'))
    professores = Professor.query.all()
    disciplinas = Disciplina.query.all()
    return render_template('form_aptidao.html', professores=professores, disciplinas=disciplinas)

# Turmas
@app.route('/turmas')
def listar_turmas():
    turmas = Turma.query.all()
    return render_template('turmas.html', turmas=turmas)

@app.route('/turma/nova', methods=['GET', 'POST'])
def nova_turma():
    if request.method == 'POST':
        professor_id = request.form['professor_id']
        disciplina_id = request.form['disciplina_id']
        codigo_turma = request.form['codigo_turma']
        semestre = request.form['semestre']
        numero_alunos = request.form['numero_alunos']
        horario = request.form['horario']
        turma = Turma(professor_id=professor_id, disciplina_id=disciplina_id, codigo_turma=codigo_turma, semestre=semestre, numero_alunos=numero_alunos, horario=horario)
        db.session.add(turma)
        db.session.commit()
        return redirect(url_for('listar_turmas'))
    professores = Professor.query.all()
    disciplinas = Disciplina.query.all()
    return render_template('form_turma.html', professores=professores, disciplinas=disciplinas)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
