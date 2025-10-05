from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS

# Inicialização do app Flask
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = SQLALCHEMY_TRACK_MODIFICATIONS
app.secret_key = "smartcitysecretkey"

db = SQLAlchemy(app)

# Dicionário movido para o escopo global para ser acessível em todo o app
mapa_criticidade = {
    "Baixa": "baixo",
    "Media": "médio", 
    "Média": "médio",
    "Alta": "alto" 
}

# ---------- MODELOS ----------
class Sensor(db.Model):
    __tablename__ = "sensor"
    id_sensor = db.Column(db.Integer, primary_key=True)
    id_tipo_sensor = db.Column(db.Integer)
    id_rua = db.Column(db.Integer)
    status = db.Column(db.String)
    data_instalacao = db.Column(db.Date)

class Camera(db.Model):
    __tablename__ = "camera"
    id_camera = db.Column(db.Integer, primary_key=True)
    modelo = db.Column(db.String)
    id_rua = db.Column(db.Integer)
    resolucao = db.Column(db.String)
    status = db.Column(db.String)

# No seu app.py, substitua a classe Ocorrencia antiga por esta:

class Ocorrencia(db.Model):
    __tablename__ = "ocorrencia"
    id_ocorrencia = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(255))
    descricao = db.Column(db.Text)
    status = db.Column(db.String)
    timestamp_ocorrencia = db.Column(db.DateTime(timezone=True)) # Adicionado timezone=True para corresponder a timestamptz
    nivel_criticidade = db.Column(db.String)
    
    # --- Campos que estavam faltando ---
    id_sensor = db.Column(db.Integer)
    id_camera = db.Column(db.Integer)
    latitude = db.Column(db.Numeric(10, 7))
    id_protocolo_associado = db.Column(db.Integer)
    id_localizacao = db.Column(db.Integer)

class ServicoExecutado(db.Model):
    __tablename__ = "servico_executado"
    id_servico_executado = db.Column(db.Integer, primary_key=True)
    id_tipo_servico = db.Column(db.Integer)
    data_inicio = db.Column(db.Date)
    data_fim = db.Column(db.Date)
    status = db.Column(db.String)
    observacoes = db.Column(db.String)

# ---------- ROTAS ----------
@app.route("/")
def index():
    total_sensores = Sensor.query.count()
    total_cameras = Camera.query.count()
    total_ocorrencias = Ocorrencia.query.count()
    total_servicos = ServicoExecutado.query.count()
    return render_template("index.html",
                           total_sensores=total_sensores,
                           total_cameras=total_cameras,
                           total_ocorrencias=total_ocorrencias,
                           total_servicos=total_servicos)

@app.route("/sensores")
def sensores():
    sensores = Sensor.query.limit(20).all()
    return render_template("sensores.html", sensores=sensores)

@app.route("/cameras")
def cameras():
    cameras = Camera.query.limit(20).all()
    return render_template("cameras.html", cameras=cameras)

@app.route("/servicos")
def servicos():
    servicos = ServicoExecutado.query.limit(20).all()
    return render_template("servicos.html", servicos=servicos)

# ---------- OCORRÊNCIAS ----------
@app.route("/ocorrencias")
def listar_ocorrencias():
    ocorrencias = Ocorrencia.query.order_by(Ocorrencia.timestamp_ocorrencia.desc()).all()
    return render_template("ocorrencias.html", ocorrencias=ocorrencias)

@app.route("/ocorrencias/nova", methods=["GET", "POST"])
def nova_ocorrencia():
    if request.method == "POST":
        titulo = request.form.get("titulo")
        descricao = request.form.get("descricao")
        # pega o valor do formulário e transforma em valor válido do ENUM
        nivel_criticidade = mapa_criticidade.get(request.form.get("nivel_criticidade"), "baixa")
        status = "aberta"

        nova = Ocorrencia(
            titulo=titulo,
            descricao=descricao,
            nivel_criticidade=nivel_criticidade,
            status=status,
            timestamp_ocorrencia=datetime.now()
        )
        db.session.add(nova)
        db.session.commit()

        flash("Ocorrência criada com sucesso!", "success")
        return redirect(url_for("listar_ocorrencias"))

    return render_template("ocorrencia_form.html")

# ---------- EXECUÇÃO ----------
if __name__ == "__main__":
    app.run(debug=True)