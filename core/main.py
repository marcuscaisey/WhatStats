from components import Chat
from components.stats import message_count_list
from helpers import extract_chat_log, get_chat_log_path


# extract_chat_log()
chat_log = get_chat_log_path()
chat = Chat(chat_log)
start = chat.first_message_timestamp
end = chat.last_message_timestamp
print(message_count_list(chat, start, end, 'text'))
