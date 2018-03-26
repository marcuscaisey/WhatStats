import re
from datetime import datetime

TIMESTAMP_PATTERN = r'\[\d{2}/\d{2}/\d{4}, \d{2}:\d{2}:\d{2}]'
ENCRYPTION_PATTERN = TIMESTAMP_PATTERN + r' (.+): \u200e'
SUBJECT_PATTERN = (
    TIMESTAMP_PATTERN
    + r' \u200e.+ changed the subject to “(.+)”'
)
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

    def __init__(self, chat_log_path):
        self.chat_log_path = chat_log_path
        if self.valid_chat_log(chat_log_path):
            self.subject = self.get_subject(chat_log_path)
            self.members = MemberList()
            self.messages = []
            self.start_date = None
            self.end_date = None
        else:
            raise ValueError

    def valid_chat_log(self, chat_log_path):
        """Return True if chat log is valid."""
        # Chat log is valid if it's first line starts with a timestamp
        # and contains a line which looks like a message
        with chat_log_path.open(encoding='utf-8') as chat_log_obj:
            for line in chat_log_obj:
                if re.match(TIMESTAMP_PATTERN, line) is None:
                    return False
                elif re.match(MESSAGE_PATTERN, line):
                    return True

    def get_subject(self, chat_log_path):
        """Return subject of chat."""
        with chat_log_path.open(encoding='utf-8') as chat_log_obj:
            match = re.match(ENCRYPTION_PATTERN, chat_log_obj.readline())
            if match:
                return match.group(1)
            else:
                matches = re.findall(SUBJECT_PATTERN, chat_log_obj.read())
                return matches[-1] if matches else 'none found'

    def read_lines(self, chat_log_path):
        """Return iterator which iterates over lines in chat log."""
        with chat_log_path.open(encoding='utf-8') as chat_log_obj:
            message = chat_log_obj.readline()
            for line in chat_log_obj:
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

    def load_messages(self, loading_dialog=None, exit_flag=None):
        """
        Extract members and messages from chat log, possibly updating
        optional loading dialog as each line is parsed.

        Optional Arguments:
        loading_dialog - dialog so status of chat log parsing can be
                         shown to user (gui.LoadingDialog)
        exit_flag - exit flag so that loading can be aborted from
                    another thread (threading.Event)
        """
        if loading_dialog is not None:
            lines = sum(1 for _ in self.read_lines(self.chat_log_path))

        for i, message in enumerate(self.read_lines(self.chat_log_path), 1):
            if loading_dialog.WasCancelled():
                if exit_flag is not None:
                    exit_flag.set()
                return

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

            if loading_dialog is not None and i % 1000 == 0:
                loading_dialog.Update(100 * i / lines)

        self.start_date = self.messages[0].timestamp.date()
        self.end_date = self.messages[-1].timestamp.date()


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

    def words(self):
        """Return list of words in message if message is a text."""
        return self.content.split() if self.type == 'text' else None

    def __repr__(self):
        return '{timestamp}: {sender}: {content}'.format(
            timestamp=self.timestamp,
            sender=self.sender,
            content=self.content)
