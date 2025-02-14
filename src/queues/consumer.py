import pika

# Настройки подключения
rabbitmq_host = "localhost"  # RabbitMQ работает на localhost в контейнере
username = "rmuser"         # Установленный пользователь
password = "rmpassword"     # Установленный пароль

# Устанавливаем соединение
credentials = pika.PlainCredentials(username, password)
connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host, credentials=credentials))
channel = connection.channel()

# Объявляем очередь (на случай, если её ещё нет)
queue_name = "test_queue"
channel.queue_declare(queue=queue_name)

# Функция обработки сообщений
def callback(ch, method, properties, body):
    print(f"[x] Получено сообщение: {body.decode()}")

# Подписываемся на очередь
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

print("[*] Ожидание сообщений. Для выхода нажмите CTRL+C")
channel.start_consuming()