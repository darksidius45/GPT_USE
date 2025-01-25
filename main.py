import json
import subprocess
import pypff
from bs4 import BeautifulSoup as bs
from config import promt

file_pars = r"C:\Users\prive\Downloads\Saalbach.pst"
file_pars2 =r"C:\Users\prive\Downloads\backup.pst"

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

            messages.append({
                "folder": folder.name,
                "subject": message.subject,
                "sender_name": message.sender_name,
                "datetime": message.client_submit_time,  
                "body_plain": body_plain  # Use the retrieved or default value
            })
    return messages



def make_request(prompt, context_message):  # Get the prompt from the config file
    full_prompt = f"{prompt}\n{context_message}"  # Combine context with the prompt

    curl_command = [
        "curl",
        "https://api.proxyapi.ru/openai/v1/chat/completions",
        "-H", "Content-Type: application/json",
        "-H", "Authorization: Bearer sk-UmoxJZ8wJm1DEmcSrwP3Iu9Bk4TGZJ0h", 
        "-d", json.dumps({
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": full_prompt}],
            "stream": False 
        })
    ]

    result = subprocess.run(curl_command, capture_output=True, text=True, encoding='utf-8')
    response = json.loads(result.stdout)
    return response['choices'][0]['message']['content']


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
    message_str += f"  Date and Time: {message['datetime']}\n"
    
    # Проверка на None
    if message['body_plain'] is not None:
        body_text = " ".join(bs(message['body_plain'], 'html.parser').get_text().split())
    else:
        body_text = "No body content available."

    message_str += f"  Body: {body_text}\n"
    message_str = "\n".join(line.strip() for line in message_str.splitlines() if line.strip())
    messages_str.append(message_str)
    i += 1


with open('context.txt', 'w', encoding='utf-8') as f:
    f.write("\n".join(messages_str))

