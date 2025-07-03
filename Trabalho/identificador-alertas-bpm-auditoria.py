import pandas as pd
import pika
import json
import time

RABBITMQ_HOST = 'localhost'
NORMAL_ALERT_QUEUE = 'normal_alert_queue'
ATTENTION_ALERT_QUEUE = 'attention_alert_queue'
CRITICAL_ALERT_QUEUE = 'critical_alert_queue'

NORMAL_ALERT_ID = 1
ATTENTION_ALERT_ID = 2
CRITICAL_ALERT_ID = 3

def create_rabbitmq_channel():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        channel = connection.channel()
        print("Conexão com RabbitMQ estabelecida com sucesso.")

        channel.queue_declare(queue=NORMAL_ALERT_QUEUE, durable=True)
        channel.queue_declare(queue=ATTENTION_ALERT_QUEUE, durable=True)
        channel.queue_declare(queue=CRITICAL_ALERT_QUEUE, durable=True)
        print(f"As filas Rabbit '{NORMAL_ALERT_QUEUE}', '{ATTENTION_ALERT_QUEUE}' e '{CRITICAL_ALERT_QUEUE}' estão prontas.")

        return connection, channel

    except pika.exceptions.AMQPConnectionError as e:
        print(f"ERRO: Não foi possível conectar ao RabbitMQ em '{RABBITMQ_HOST}'.")
        print("Verifique se o RabbitMQ está rodando (ex: via Docker) e acessível.")
        exit()

def read_patients_file():
    try:
        patients_file = pd.read_csv("monitoramento_pacientes.csv")
        print(f"Arquivo 'monitoramento_pacientes.csv' lido. Total de {len(patients_file)} registros.")

        return patients_file.groupby('paciente_id')

    except FileNotFoundError:
        print("ERRO: Arquivo 'monitoramento_pacientes.csv' não encontrado.")
        exit()
    except Exception as ex:
        print(f"Erro: Erro no acesso ao arquivo: 'monitoramento_pacientes.csv': {ex}.")
        exit()

def read_heartbeat_intervals_by_state_file():
    try:
        heartbeat_intervals_by_state_file = pd.read_csv("batimentos_por_estado.csv")
        print(f"Arquivo 'batimentos_por_estado.csv' lido. Total de {len(heartbeat_intervals_by_state_file)} registros.")

        heartbeat_intervals_by_state_file.set_index('state_id', inplace=True)

        return heartbeat_intervals_by_state_file

    except FileNotFoundError:
        print("ERRO: Arquivo 'batimentos_por_estado.csv' não encontrado.")
        exit()
    except Exception as ex:
        print(f"Erro: Erro no acesso ao arquivo: 'batimentos_por_estado.csv': {ex}.")
        exit()

def classify_alerts(heartbeat_intervals, bpm, state, age):
    try:
        heartbeat_intervals_info = heartbeat_intervals.loc[state]

        normal_heartbeat_min = heartbeat_intervals_info['normal_bpm_min']
        normal_heartbeat_max = heartbeat_intervals_info['normal_bpm_max']
        attention_heartbeat_max = heartbeat_intervals_info['attention_bpm_max']

        if age > 65:
            normal_heartbeat_min -= 10
            normal_heartbeat_max -= 10
            attention_heartbeat_max -= 10

        if attention_heartbeat_max < bpm or normal_heartbeat_min > bpm:
            return CRITICAL_ALERT_ID
        elif normal_heartbeat_max < bpm:
            return ATTENTION_ALERT_ID
        else:
            return NORMAL_ALERT_ID
    except Exception as ex:
        print(f"Erro: Erro ao classificar alerta: bmp: '{bpm}', state: '{state}' e age: '{age}': {ex}.")
        exit()


def analyze_patient_info(patient_info, patient_data_file, heartbeat_intervals):
    try:
        age = patient_info['idade']
        state_id = patient_info['estado_id']

        alert_classifications = patient_data_file['batimento_cardiaco'].apply(
            lambda bpm: classify_alerts(heartbeat_intervals, bpm, state_id, age)
        )

        state = patient_info['estado']

        if CRITICAL_ALERT_ID in alert_classifications.values:
            final_alert_id = CRITICAL_ALERT_ID
            critical_point = patient_data_file[alert_classifications == CRITICAL_ALERT_ID].iloc[0]
            analysis_summary = f"Registrou pico de {critical_point['batimento_cardiaco']} BPM em {state} no minuto {critical_point['minuto']}, precisa de atendimento URGENTE!"
        elif ATTENTION_ALERT_ID in alert_classifications.values:
            final_alert_id = ATTENTION_ALERT_ID
            attention_point = patient_data_file[alert_classifications == ATTENTION_ALERT_ID].iloc[0]
            analysis_summary = f"Registrou {attention_point['batimento_cardiaco']} BPM em {state}, indicando necessidade de acompanhamento."
        else:
            final_alert_id = NORMAL_ALERT_ID
            media_bpm = patient_data_file['batimento_cardiaco'].mean()
            analysis_summary = f"Paciente estável com média de {media_bpm:.1f} BPM em {state}."

        return final_alert_id, analysis_summary
    except Exception as ex:
        print(f"Erro: Erro ao analizar dados do paciente: '{patient_info.to_dict()}': {ex}.")
        exit()

def publish_message_to_rabbitmq(channel, queue, message):
    message_body = json.dumps(message, indent=4)
    try:
        channel.basic_publish(
            exchange='',
            routing_key=queue,
            body=message_body,
            properties=pika.BasicProperties(delivery_mode=2))

        print(f"\nMensagem '{message}' enviada para a fila '{queue}'.")
    except Exception as ex:
        print(f"Erro: Erro ao publicar mensagem: '{message_body}', na fila '{queue}': {ex}.")
        exit()

def create_audit_file(audit_records):
    nome_arquivo_auditoria = "log_auditoria_classificacao.csv"
    try:
        print("\nGerando CSV de auditoria:")
        df_auditoria = pd.DataFrame(audit_records)
        df_auditoria.to_csv(nome_arquivo_auditoria, index=False, encoding='utf-8-sig')

        print(f"Arquivo de auditoria gerado com sucesso;'")
    except Exception as ex:
        print(f"Erro: Erro ao gerar o arquivo: '{nome_arquivo_auditoria}': {ex}.")
        exit()

def main():
    try:
        print("Iniciando programa:")

        connection, channel = create_rabbitmq_channel()

        patients = read_patients_file()
        heartbeat_intervals = read_heartbeat_intervals_by_state_file()

        audit_records = []

        print("\nIniciando análise de cada paciente:")
        for patient_id, patient_data_file in patients:
            patient_info = patient_data_file.iloc[0]

            final_alert_id, analysis_summary = analyze_patient_info(patient_info, patient_data_file, heartbeat_intervals)

            if final_alert_id == CRITICAL_ALERT_ID:
                final_alert = "Alerta Crítico"
                destiny_queue = CRITICAL_ALERT_QUEUE
            elif final_alert_id == ATTENTION_ALERT_ID:
                final_alert = "Atenção"
                destiny_queue = ATTENTION_ALERT_QUEUE
            else:
                final_alert = "Normal"
                destiny_queue = NORMAL_ALERT_QUEUE

            message = {
                'paciente_id': int(patient_id),
                'nivel_alerta_id': final_alert_id,
                'nivel_alerta': final_alert,
                'timestamp_analise': time.strftime('%Y-%m-%dT%H:%M:%S'),
                'resumo_analise': analysis_summary,
                'dados_paciente': patient_info.to_dict()
            }

            audit_record = {
                'paciente_id': int(patient_id),
                'idade': patient_info['idade'],
                'sexo': patient_info['sexo'],
                'estado_permanente': patient_info['estado'],
                'classificacao_final_id': final_alert_id,
                'classificacao_final': final_alert,
                'justificativa': analysis_summary
            }
            audit_records.append(audit_record)

            publish_message_to_rabbitmq(channel, destiny_queue, message)

        create_audit_file(audit_records)

        connection.close()
        print("\nAnálise concluída. Todas as mensagens foram publicadas e o log de auditoria foi gerado.")
    except Exception as ex:
        print(f"Erro: Erro na execução do programa: {ex}.")
        exit()


if __name__ == '__main__':
    main()