from components import Chat
from components.stats import message_count_data, word_count_data
from components.plots import show_bar_chart
from helpers import get_chat_log_path


chat = Chat(get_chat_log_path())
start = chat.first_message_timestamp
end = chat.last_message_timestamp
data = message_count_data(chat, start, end)
show_bar_chart(data, y_label='Messages Sent', title='Messages Sent')
