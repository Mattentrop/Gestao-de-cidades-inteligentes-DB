Repositório do projeto de um banco de dados para uma Plataforma Gestão de Cidade Inteligente proposto na disciplina de Banco de Dados II, responsável por registrar, armazenar, organizar e correlacionar informações da malha urbana urbana: bairros, ruas, sensores, câmeras, serviços públicos, protocolos, veículos e ocorrências, além de indicadores de recursos básicos (água, energia e resíduos). O objetivo é prover uma base coesa, auditável e performática dos dados para operação diária, relatórios gerenciais e possivel integração com aplicações web/BI/IoT. Fazendo o uso de ferramentas de BDs relacionais e não relacionais como MySQL e o MongoDB. O projeto é composto por um grupo de cinco alunos da disciplina: Luiz Thiago Gonçalves Cassab, Matheus Henrique Gonçalves Rodrigues, Gabriel Vaz de Sá Melo Marcondes de Andrade, João Paulo Guinancio Ferreira, Juan Peres.



# Triggers


**2. Atualização Automática de Datas (updated_at)**

O que faz: Garante que o campo data_ultima_modificacao seja atualizado automaticamente para o instante atual (NOW()) sempre que um registro sofrer qualquer alteração.

Por que usar: Elimina a necessidade de enviar a data manualmente em cada comando UPDATE na aplicação, garantindo que o carimbo de tempo seja sempre fidedigno.

    -- Função que define o timestamp atual 
    CREATE OR REPLACE FUNCTION public.atualizar_timestamp_modificacao()

    RETURNS trigger AS $BODY$

    BEGIN

        NEW.data_ultima_modificacao = NOW();
        RETURN NEW;
    END;
    $BODY$ LANGUAGE plpgsql;

    -- Aplicação do gatilho na tabela 'ocorrencia'
    CREATE TRIGGER tg_atualiza_data_ocorrencia
    BEFORE UPDATE ON ocorrencia
    FOR EACH ROW
    EXECUTE FUNCTION atualizar_timestamp_modificacao();



**2. Auditoria de Mudança de Status (Audit Trail)**

O que faz: Monitora a tabela de ocorrências **e, apenas quando detecta uma mudança no status** (ex: de 'Aberta' para 'Em Análise'), cria automaticamente um registro na tabela de histórico log_status_ocorrencia.


Por que usar: Permite rastrear todo o ciclo de vida de um chamado sem poluir a tabela principal. É essencial para calcular métricas de tempo de atendimento (SLA) e para auditoria de ações.

    -- Função que registra o histórico
    CREATE OR REPLACE FUNCTION public.registrar_mudanca_status_ocorrencia()
    RETURNS trigger AS $BODY$
    BEGIN
        -- Verifica se houve mudança real no status para evitar logs duplicados
        IF NEW.status <> OLD.status THEN
            INSERT INTO log_status_ocorrencia (
                id_ocorrencia, 
                status_antigo, 
                status_novo, 
                data_alteracao,
                usuario_alteracao,      -- Cargo do usuário (ENUM)
                id_usuario_responsavel  -- ID do usuário responsável
            )
            VALUES (
                NEW.id_ocorrencia, 
                OLD.status, 
                NEW.status, 
                NOW(),
                'operador'::tipo_usuario_enum, -- Valor padrão caso o sistema não informe
                COALESCE(NEW.id_usuario_reportou, 0)
            );
        END IF;
        RETURN NEW;
    END;
    $BODY$ LANGUAGE plpgsql;

    -- Aplicação do gatilho (roda APÓS a atualização)
    CREATE TRIGGER tg_auditoria_status
    AFTER UPDATE ON ocorrencia
    FOR EACH ROW
    EXECUTE FUNCTION registrar_mudanca_status_ocorrencia();
