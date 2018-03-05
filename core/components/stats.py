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


def message_count_plot_data(chat, start, end, message_type=None):
    """
    Return (x, y) where x is list of members and y is their respective
    message counts between start and end (datetime), sorted by message
    count.
    """
    x = []
    y = []
    for member in chat.members:
        message_count = count_messages(member, start, end, message_type)
        if message_count > 0:
            x.append(member.name)
            y.append(message_count)
    x = [i for _, i in sorted(zip(y, x), reverse=True)]
    y.sort(reverse=True)
    return (x, y)


def word_count_plot_data(chat, start, end):
    """
    Return (x, y) where x is list of members and y is their respective
    message counts between start and end (datetime), sorted by message
    count.
    """
    x = []
    y = []
    for member in chat.members:
        word_count = count_words(member, start, end)
        if word_count > 0:
            x.append(member.name)
            y.append(word_count)
    x = [i for _, i in sorted(zip(y, x), reverse=True)]
    y.sort(reverse=True)
    return (x, y)
