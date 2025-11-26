import psycopg2
from pymongo import MongoClient
from datetime import datetime

# --- CONFIGURAÇÕES ---
PG_CONFIG = {
    "host": "localhost",
    "database": "cidade",
    "user": "criador",
    "password": "senha123"
}

MONGO_URI = "mongodb://admin:senha_segura@localhost:27017/"

def buscar_dados_hibridos():
    try:
        print(" Conectando ao PostgreSQL...")
        pg_conn = psycopg2.connect(**PG_CONFIG)
        pg_cursor = pg_conn.cursor()

        query_pg = """
            SELECT s.id_sensor, ts.nome as tipo, r.nome as rua, b.nome as bairro
            FROM sensor s
            JOIN tipo_sensor ts ON s.id_tipo_sensor = ts.id_tipo_sensor
            JOIN rua r ON s.id_rua = r.id_rua
            JOIN bairro b ON r.id_bairro = b.id_bairro
            WHERE s.status = 'ativo'
            LIMIT 1;
        """
        pg_cursor.execute(query_pg)
        sensor_pg = pg_cursor.fetchone()

        if not sensor_pg:
            print(" Nenhum sensor encontrado no PostgreSQL.")
            return

        id_sensor, tipo_sensor, rua, bairro = sensor_pg
        print(f" Sensor encontrado no PG: ID {id_sensor} | Tipo: {tipo_sensor}")
        print(f" Localização: {rua}, {bairro}")

        print("\n Conectando ao MongoDB...")
        mongo_client = MongoClient(MONGO_URI)
        db_mongo = mongo_client['cidade_db']
        collection = db_mongo['leituras']

        print(f" Buscando leituras no Mongo para o sensor_id {id_sensor}...")
        
        leituras = collection.find(
            {"sensor_id": id_sensor} 
        ).sort("timestamp", -1).limit(3)

        count = 0
        print("\n Últimas leituras recebidas:")
        print("-" * 50)
        for leitura in leituras:
            count += 1
            data = leitura['timestamp'].strftime('%d/%m/%Y %H:%M:%S')
            valor = leitura['valor_bruto'] # O JSON que está no Mongo
            print(f" {data} | 🌡️ Dados: {valor}")
        
        if count == 0:
            print("Nenhuma leitura encontrada no Mongo para este ID de sensor.")
            print("(Dica: O script gerador criou dados para IDs 1 a 5. Verifique se o sensor do PG tem um desses IDs)")

    except Exception as e:
        print(f"\nErro: {e}")
    finally:
        if 'pg_conn' in locals(): pg_conn.close()
        if 'mongo_client' in locals(): mongo_client.close()

if __name__ == "__main__":
    buscar_dados_hibridos()
