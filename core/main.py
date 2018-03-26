import threading
from pathlib import Path
from zipfile import ZipFile

import wx

from .components.charts import bar_chart, chart_title, doughnut_chart
from .components.chat import Chat
from .components.data import messages_sent_data, words_sent_data
from .components.gui import MainFrame, CloseDialog, ImportDialog, LoadingDialog

TEMP_PATH = Path('temp')
CHAT_LOG_NAME = '_chat.txt'
CHAT_LOG_PATH = TEMP_PATH / CHAT_LOG_NAME

CHAT_LOAD_EVENT_TYPE = wx.NewEventType()
CHAT_LOAD_EVENT_BINDER = wx.PyEventBinder(CHAT_LOAD_EVENT_TYPE)


class ChatLoadThread(threading.Thread):
    """
    Thread which: extracts chat log from zip file, initialises chat
    object from chat log (whilst updating GUI loading dialog), then
    posts ChatLoadEvent back to main thread.
    """

    def __init__(self, parent, zip_path, loading_dialog):
        super().__init__()
        self.parent = parent
        self.zip_path = zip_path
        self.loading_dialog = loading_dialog
        self.exit_flag = threading.Event()

    def extract_chat_log(self, zip_path, destination_path):
        """Extract chat log from chat log zip to destination path."""
        with ZipFile(zip_path) as zip_obj:
            zip_obj.extract(CHAT_LOG_NAME, path=str(destination_path))

    def run(self):
        try:
            self.extract_chat_log(self.zip_path, TEMP_PATH)
            chat = Chat(CHAT_LOG_PATH)
            chat.load_messages(self.loading_dialog, self.exit_flag)
            wx.CallAfter(self.loading_dialog.Destroy)
            CHAT_LOG_PATH.unlink()
            if not self.exit_flag.is_set():
                wx.PostEvent(self.parent, ChatLoadEvent(chat))
        except OSError:
            wx.LogError('Couldn\'t open zip file.')
        except KeyError:
            wx.LogError('Couldn\'t extract chat log.')
        except ValueError:
            wx.LogError('Chat log not valid.')


class ChatLoadEvent(wx.PyCommandEvent):
    """
    Event that signals chat object has been initialised and is ready to
    be loaded.
    """

    def __init__(self, chat):
        super().__init__(eventType=CHAT_LOAD_EVENT_TYPE)
        self.chat = chat


class WhatStats(wx.App):
    """Program which generates statistics from WhatsApp chat logs."""

    def __init__(self):
        super().__init__()
        self.frame = MainFrame()
        self.panel = self.frame.panel
        self.chat = None
        self.chat_load_thread = None
        self.bind_event_handlers()

    def start(self):
        """Start program."""
        self.toggle_inputs(False)
        self.frame.Show()
        self.MainLoop()

    def bind_event_handlers(self):
        """Bind events to their event handlers."""
        self.frame.Bind(wx.EVT_CLOSE, self.on_close)

        self.frame.Bind(CHAT_LOAD_EVENT_BINDER, self.on_chat_load)
        self.frame.menu_bar.Bind(wx.EVT_MENU, self.on_import, id=wx.ID_OPEN)
        self.frame.menu_bar.Bind(wx.EVT_MENU, self.on_quit, id=wx.ID_EXIT)

        self.panel.subject_input.Bind(wx.EVT_KILL_FOCUS, self.on_subject_input)
        self.panel.generate_button.Bind(wx.EVT_BUTTON, self.on_generate)

    def on_close(self, event):
        """Ask user if they are sure they want to quit."""
        with CloseDialog(self.frame) as close_dialog:
            if close_dialog.ShowModal() == wx.ID_OK:
                self.frame.Destroy()
            else:
                event.Veto()

    def on_import(self, event):
        """
        Ask user to select chat log zip, then extract it and initialise
        Chat object in a seperate thread.
        """
        with ImportDialog(self.frame) as import_dialog:
            if import_dialog.ShowModal() != wx.ID_CANCEL:
                zip_path = import_dialog.GetPath()
                loading_dialog = LoadingDialog(self.frame)
                thread = ChatLoadThread(self.frame, zip_path, loading_dialog)
                thread.start()

    def on_chat_load(self, event):
        """Set chat variable and initialise inputs with chat data."""
        self.chat = event.chat
        self.init_inputs(self.chat)

    def on_quit(self, event):
        self.frame.Close()

    def on_subject_input(self, event):
        """Set chat subject to contents of chat subject input."""
        self.chat.subject = self.panel.subject_input.GetValue()

    def on_generate(self, event):
        """Show chart of user's choice for chosen statistic."""
        start = self.panel.start_date_input.GetValue()
        end = self.panel.end_date_input.GetValue()
        statistic = self.panel.statistic_choices.GetStringSelection()
        chart_style = self.panel.chart_style_choices.GetStringSelection()

        if statistic == 'Messages sent':
            data = messages_sent_data(self.chat, start, end)
        elif statistic == 'Words sent':
            data = words_sent_data(self.chat, start, end)

        title = chart_title(statistic, self.chat, start, end)
        if chart_style == 'Doughnut chart':
            doughnut_chart(data, title)
        elif chart_style == 'Bar chart':
            bar_chart(data, title)

    def toggle_inputs(self, status):
        """Enable/disable inputs."""
        self.panel.subject_input.Enable(status)
        self.panel.start_date_input.Enable(status)
        self.panel.end_date_input.Enable(status)
        self.panel.statistic_choices.Enable(status)
        self.panel.chart_style_choices.Enable(status)
        self.panel.generate_button.Enable(status)

    def init_inputs(self, chat):
        """Initialise inputs with data from chat."""
        self.panel.subject_input.SetValue(chat.subject)
        self.panel.start_date_input.SetValue(chat.start_date)
        self.panel.end_date_input.SetValue(chat.end_date)
        self.panel.members_list.set_members(chat.members)
        self.toggle_inputs(True)
