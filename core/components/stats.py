def messages_sent(message_container, start_date, end_date, message_type=None):
    """
    Return number of messages sent between start and end date contained
    by message container (chat/member).
    """
    messages_sent = 0
    for message in message_container.messages:
        if (start_date <= message.timestamp.date() <= end_date
           and (message_type is None or message.type == message_type)):
                messages_sent += 1
    return messages_sent


def words_sent(message_container, start_date, end_date):
    """
    Return number of words sent between start and end date contained by
    message container (chat/member).
    """
    words_sent = 0
    for message in message_container.messages:
        if (start_date <= message.timestamp.date() <= end_date
           and message.type == 'text'):
                words_sent += len(message.words())
    return words_sent
