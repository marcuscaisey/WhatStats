from datetime import datetime
import re


TIMESTAMP_PATTERN = r'\[\d{2}/\d{2}/\d{4}, \d{2}:\d{2}:\d{2}]'
MESSAGE_PATTERN = (
    r'(?s)'
    r'\[(?P<timestamp>\d{2}/\d{2}/\d{4}, \d{2}:\d{2}:\d{2})] '
    r'(?P<sender>[^\u200e].*?): '
    r'(?P<content>[^\u200e].*)'
)


class Chat:
    """
    Chat object which holds the members of the chat and their messages.
    """

    def __init__(self, chat_log):
        self.members = MemberList()
        self.messages = []
        self.get_members_messages(chat_log)
        self.first_message_date = self.messages[0].timestamp.date()
        self.last_message_date = self.messages[-1].timestamp.date()

    def read_messages(self, chat_log):
        """
        Return iterator object which iterates over messages in chat log.
        """
        with open(chat_log, encoding='utf-8') as file_obj:
            message = file_obj.readline()
            for line in file_obj:
                # If the next line starts with a timestamp then the
                # current line must be the end of the current message
                if re.match(TIMESTAMP_PATTERN, line):
                    yield message.rstrip('\n')
                    message = line
                else:
                    message += line
            yield message.rstrip('\n')

    def add_message(self, timestamp, sender, content):
        """Add message to list of messages."""
        self.messages.append(Message(timestamp, sender, content))

    def get_members_messages(self, chat_log):
        """Extract members and messages from chat log zip."""
        for message in self.read_messages(chat_log):
            match = re.match(MESSAGE_PATTERN, message)
            if match:
                timestamp = match.group('timestamp')
                sender = match.group('sender')
                content = match.group('content')
                self.add_message(timestamp, sender, content)
                if self.members.contains(sender):
                    member = self.members.find(sender)
                    member.add_message(timestamp, sender, content)
                else:
                    self.members.add(timestamp, sender, content)


class MemberList(list):
    """List object which contains chat members."""

    def add(self, timestamp, sender, content):
        """Add member to list along with their first message."""
        self.append(Member(sender))
        self[-1].add_message(timestamp, sender, content)

    def contains(self, name):
        """Return true if there is a member with name."""
        return name in [member.name for member in self]

    def find(self, name):
        """Return member with name."""
        return [member for member in self if member.name == name][0]


class Member:
    """Member object which holds each member's name and messages."""

    def __init__(self, name):
        self.name = name
        self.messages = []

    def add_message(self, timestamp, sender, content):
        """Add message to list of member's messages."""
        self.messages.append(Message(timestamp, sender, content))

    def __repr__(self):
        return self.name


class Message:
    """
    Message object which holds the message's timestamp and content.

    Types: text, image, video, gif, document, location, contact
    """

    def __init__(self, timestamp, sender, content):
        self.timestamp = datetime.strptime(timestamp, '%d/%m/%Y, %H:%M:%S')
        self.sender = sender
        self.content = content
        self.type = self.get_type(content)

    def get_type(self, content):
        """Return the type of the message based on the content."""
        # Non text messages contain the character \u200e which is
        # followed by the type of the message
        match = re.search(r'\u200e(\w+)', content)
        return match.group(1).lower() if match else 'text'

    @property
    def words(self):
        """Return list of words in message if message is a text."""
        return self.content.split() if self.type == 'text' else None

    def __repr__(self):
        return '{timestamp}: {sender}: {content}'.format(
            timestamp=self.timestamp,
            sender=self.sender,
            content=self.content)
