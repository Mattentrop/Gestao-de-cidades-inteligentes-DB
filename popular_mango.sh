#!/bin/bash

# Configurações
CONTAINER_NAME="mongo-cidade"
MONGO_USER="admin"
MONGO_PASS="senha_segura"
DB_NAME="cidade_db"


sudo docker exec -i $CONTAINER_NAME mongosh -u $MONGO_USER -p $MONGO_PASS --quiet <<EOF

db = db.getSiblingDB('$DB_NAME');


const sensores = [
    { id: 1, tipo: "Temperatura", local_id: 10 },
    { id: 2, tipo: "Qualidade Ar", local_id: 12 },
    { id: 3, tipo: "Ruido", local_id: 15 },
    { id: 4, tipo: "Temperatura", local_id: 20 },
    { id: 5, tipo: "Umidade", local_id: 22 }
];

const dadosParaInserir = [];
const diasAtras = 7; 
const agora = new Date();


print("⏳ Gerando lote extra de leituras...");

for (let d = 0; d < diasAtras; d++) {
    for (let h = 0; h < 24; h++) {
        
        let dataLeitura = new Date();
        dataLeitura.setDate(agora.getDate() - d);
        dataLeitura.setHours(h, 0, 0, 0);
        
        let minutoRandom = Math.floor(Math.random() * 60);
        dataLeitura.setMinutes(minutoRandom);

        sensores.forEach(sensor => {
            let temp = (20 + Math.random() * 15).toFixed(2);
            let umid = (40 + Math.random() * 40).toFixed(1);
            let bateria = Math.floor(80 + Math.random() * 20);

            dadosParaInserir.push({
                "timestamp": dataLeitura,
                "sensor_id": sensor.id,
                "metadados": {
                    "tipo": sensor.tipo,
                    "localizacao_pg_id": sensor.local_id
                },
                "valor_bruto": {
                    "temperatura": parseFloat(temp),
                    "umidade": parseFloat(umid),
                    "bateria": bateria
                }
            });
        });
    }
}

if (dadosParaInserir.length > 0) {
    db.leituras.insertMany(dadosParaInserir);
    print("LOTE ADICIONADO! " + dadosParaInserir.length + " novos registros somados ao banco.");
}
EOF

echo "Fim da execução."
