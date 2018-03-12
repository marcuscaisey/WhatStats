from .stats import messages_sent, words_sent


def messages_sent_data(chat, start_date, end_date, message_type=None):
    """
    Return (x, y) where x is list of members and y is a list of their
    respective message counts between start and end date, sorted by message
    count.
    """
    x = []
    y = []
    for member in chat.members:
        count = messages_sent(member, start_date, end_date, message_type)
        if count > 0:
            x.append(member.name)
            y.append(count)
    x = [i for _, i in sorted(zip(y, x), reverse=True)]
    y.sort(reverse=True)
    return (x, y)


def words_sent_data(chat, start_date, end_date):
    """
    Return (x, y) where x is list of members and y is a list of their
    respective word counts between start and end date, sorted by word count.
    """
    x = []
    y = []
    for member in chat.members:
        count = words_sent(member, start_date, end_date)
        if count > 0:
            x.append(member.name)
            y.append(count)
    x = [i for _, i in sorted(zip(y, x), reverse=True)]
    y.sort(reverse=True)
    return (x, y)
