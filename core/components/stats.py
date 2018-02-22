def count_messages(obj, start=None, end=None, message_type=None):
    """
    Return number of messages contained in obj.

    Keyword arguments:
    start -- optional datetime to start counting from
    end -- optional datetime to stop counting at
    message_type -- optional type of message of to count
    """
    start = obj.first_message_timestamp if start is None else start
    end = obj.last_message_timestamp if end is None else end
    count = 0
    for message in obj.messages:
        if start <= message.timestamp <= end:
            if message_type is None or message.type == message_type:
                count += 1
    return count


def count_words(obj, start=None, end=None):
    """
    Return number of words contained in obj.

    Keyword arguments:
    start -- optional datetime to start counting from
    end -- optional datetime to stop counting at
    """
    start = obj.first_message_timestamp if start is None else start
    end = obj.last_message_timestamp if end is None else start
    count = 0
    for message in obj.messages:
        count += len(message.words)
    return count


def message_count_list(chat, start=None, end=None):
    """
    Return list of tuples containing each member's name and their
    message count sorted by their message count, not including members
    who have not sent any messages.

    Keyword arguments:
    start -- optional datetime to start counting from
    end -- optional datetime to stop counting at
    """
    start = chat.first_message_timestamp if start is None else start
    end = chat.last_message_timestamp if end is None else end
    message_count_list = []
    for member in chat.members:
        message_count = count_messages(member, start, end)
        if message_count > 0:
            message_count_list.append((member, message_count))
    return sorted(message_count_list, key=lambda x: x[1], reverse=True)
