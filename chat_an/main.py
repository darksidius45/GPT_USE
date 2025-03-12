import json
import subprocess
import pypff
from bs4 import BeautifulSoup as bs
from sito_info.config import promt
import re

file_pars = r"C:\Users\prive\Downloads\Saalbach.pst"
file_pars2 = r"C:\Users\prive\Downloads\backup.pst"


def process_plain_text_body(message):
    return re.sub(r"([\r\n]+ ?)+", r"\r\n", message.plain_text_body.decode("utf-8"))


# Обработка html тела
def process_html_body(message):
    soup = bs(message.html_body(), "lxml")
    plain_text = soup.get_text()
    # Удаление html комментариев
    plain_text = re.sub(r"(<!--.*-->)+", r"", plain_text, flags=re.S)
    plain_text = re.sub(r"([\r\n]+ ?)+", r"\r\n", plain_text)
    return plain_text


def get_body(message):
    if message.get_plain_text_body():
        return process_plain_text_body(message)
    if message.get_html_body():
        return process_html_body(message)


def parse_folder(base):
    messages = []
    for folder in base.sub_folders:
        if folder.number_of_sub_folders:
            # Извлечение писем из дочерней папки
            messages += parse_folder(folder)
        # Обработка писем в текущей папке
        for message in folder.sub_messages:
            body_plain = None
            try:
                body_plain = message.get_html_body()  # Attempt to get the HTML body
            except OSError:
                body_plain = "No HTML body available."  # Handle the error gracefully

            messages.append(
                {
                    "folder": folder.name,
                    "subject": message.subject,
                    "sender_name": message.sender_name,
                    "sender_email": message.sender_email_address,
                    "datetime": message.client_submit_time,
                    "body_plain": get_body(
                        message
                    ),  # Get the whole body of the message
                }
            )
    return messages


# def make_request(prompt, context_message):  # Get the prompt from the config file
#     full_prompt = f"{prompt}\n{context_message}"  # Combine context with the prompt

#     curl_command = [
#         "curl",
#         "https://api.proxyapi.ru/openai/v1/chat/completions",
#         "-H", "Content-Type: application/json",
#         "-H", "Authorization: Bearer sk-UmoxJZ8wJm1DEmcSrwP3Iu9Bk4TGZJ0h",
#         "-d", json.dumps({
#             "model": "gpt-4o-mini",
#             "messages": [{"role": "user", "content": full_prompt}],
#             "stream": False
#         })
#     ]

#     result = subprocess.run(curl_command, capture_output=True, text=True, encoding='utf-8')
#     response = json.loads(result.stdout)
#     return response['choices'][0]['message']['content']


pst = pypff.file()
pst.open(file_pars2)
root = pst.get_root_folder()
# Извлечение всех писем из файла
messages = parse_folder(root)
i = 1
messages_str = []
for message in messages:
    print(f"Processing message {i}: {message['subject']}")  # Выводим каждое сообщение
    message_str = f"Message {i}:\n"
    message_str += f"  Folder: {message['folder']}\n"
    message_str += f"  Subject: {message['subject']}\n"
    message_str += f"  Sender: {message['sender_name']}\n"
    message_str += f"  Email: {message['sender_email']}"
    message_str += f"  Date and Time: {message['datetime']}\n"
    message_str += f"  Body: {get_body(message['body_plain'])}\n"
    message_str = "\n".join(
        line.strip() for line in message_str.splitlines() if line.strip()
    )
    messages_str.append(message_str)
    i += 1


r = open("context.txt", "w")
for message in messages_str:
    r.write(message)
r.close
