import pika

# Настройки подключения
rabbitmq_host = "localhost"  # RabbitMQ работает на localhost в контейнере
username = "rmuser"         # Установленный пользователь
password = "rmpassword"     # Установленный пароль

# Устанавливаем соединение
credentials = pika.PlainCredentials(username, password)
connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host, credentials=credentials))
channel = connection.channel()

# Объявляем очередь
queue_name = "test_queue"
channel.queue_declare(queue=queue_name)

# Отправляем сообщение
message = "Hello, RabbitMQ!"
channel.basic_publish(exchange="", routing_key=queue_name, body=message)
print(f"[x] Отправлено сообщение: {message}")

# Закрываем соединение
connection.close()