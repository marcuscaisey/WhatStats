from pathlib import Path
from zipfile import ZipFile

import wx

from .components.charts import chart_title, bar_chart, pie_chart
from .components.chat import Chat
from .components.data import messages_sent_data, words_sent_data
from .components.gui import MainFrame

TEMP_PATH = Path('temp')
CHAT_LOG_NAME = '_chat.txt'
CHAT_LOG_PATH = TEMP_PATH / CHAT_LOG_NAME


def extract_chat_log(zip_path, destination_path):
    """Extract chat log from chat log zip to destination path."""
    with ZipFile(zip_path) as zip_obj:
        zip_obj.extract(CHAT_LOG_NAME, path=str(destination_path))


class WhatStats(wx.App):
    """Program which generates statistics from WhatsApp chat logs."""

    def __init__(self):
        super().__init__()
        self.frame = MainFrame()
        self.panel = self.frame.panel
        self.bind_event_handlers()

    def start(self):
        """Start program."""
        self.frame.Show()
        self.MainLoop()

    def bind_event_handlers(self):
        """Bind events to their event handlers."""
        self.frame.Bind(wx.EVT_CLOSE, self.on_close)

        self.frame.menu_bar.Bind(wx.EVT_MENU, self.on_import, id=wx.ID_OPEN)
        self.frame.menu_bar.Bind(wx.EVT_MENU, self.on_quit, id=wx.ID_EXIT)

        kill_event = wx.EVT_KILL_FOCUS
        self.panel.subject_input.Bind(kill_event, self.on_subject_change)
        self.panel.generate_button.Bind(wx.EVT_BUTTON, self.on_generate)

    def on_close(self, event):
        """Ask user if they are sure they want to quit."""
        message = 'Are you sure you want to quit?'
        caption = 'WhatStats'
        flags = wx.OK | wx.CANCEL | wx.CANCEL_DEFAULT | wx.ICON_EXCLAMATION
        with wx.MessageDialog(None, message, caption, flags) as quit_dialog:
            if quit_dialog.ShowModal() == wx.ID_OK:
                self.frame.Destroy()
            else:
                event.Veto()

    def on_import(self, event):
        """
        Ask user to select chat log zip, then extract it and initialise
        Chat object.
        """
        with wx.FileDialog(None, wildcard='*.zip') as file_dialog:
            if file_dialog.ShowModal() != wx.ID_CANCEL:
                zip_path = file_dialog.GetPath()
                try:
                    extract_chat_log(zip_path, TEMP_PATH)
                    self.chat = Chat(CHAT_LOG_PATH)
                    CHAT_LOG_PATH.unlink()
                    self.panel.init_inputs(self.chat)
                except OSError:
                    wx.LogError('Coulnd\'t open zip file.')
                except KeyError:
                    wx.LogError('Couldn\'t extract chat log.')
                except ValueError:
                    wx.LogError('Chat log not valid.')

    def on_quit(self, event):
        self.frame.Close()

    def on_subject_change(self, event):
        """Set chat subject to contents of chat subject` input."""
        self.chat.subject = self.panel.subject_input.GetValue()

    def on_generate(self, event):
        """Show bar chart."""
        start = self.panel.start_date_input.GetValue()
        end = self.panel.end_date_input.GetValue()
        data = messages_sent_data(self.chat, start, end)
        title = chart_title('Messages sent', self.chat, start, end)
        pie_chart(data, title)
