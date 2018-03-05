def count_messages(message_container, start, end, message_type=None):
    """
    Return number of messages sent between start and end (datetime)
    contained by message_container (chat/member).
    """
    count = 0
    for message in message_container.messages:
        if start <= message.timestamp <= end:
            if message_type is None or message.type == message_type:
                count += 1
    return count


def count_words(message_container, start, end):
    """
    Return number of words sent between start and end (datetime)
    contained by message_container (chat/member).
    """
    count = 0
    for message in message_container.messages:
        if start <= message.timestamp <= end:
            count += len(message.words)
    return count


def message_count_list(chat, start, end, message_type=None):
    """
    Return list of tuples containing each member's name and their
    message count between start and end (datetime), sorted by message
    count, not including members who have not sent any messages.
    """
    message_count_list = []
    for member in chat.members:
        message_count = count_messages(member, start, end, message_type)
        if message_count > 0:
            message_count_list.append((member, message_count))
    return sorted(message_count_list, key=lambda x: x[1], reverse=True)


def word_count_list(chat, start, end):
    """
    Return list of tuples containing each member's name and their
    word count between start and end (datetime), sorted by message
    count, not including members who have not sent any messages.
    """
    word_count_list = []
    for member in chat.members:
        word_count = count_words(member, start, end)
        if word_count > 0:
            word_count_list.append((member, word_count))
    return sorted(word_count_list, key=lambda x: x[1], reverse=True)
