from pathlib import Path
from zipfile import ZipFile

import wx

from .components.chat import Chat
from .components.gui import MainFrame
from .components.plots import show_bar_chart
from .components.stats import message_count_data

TEMP_PATH = Path('temp')
CHAT_LOG_NAME = '_chat.txt'
CHAT_LOG_PATH = TEMP_PATH / CHAT_LOG_NAME


def extract_chat_log(zip_path, destination_path):
    """Extract chat log from chat log zip to destination_path."""
    with ZipFile(zip_path) as zip_obj:
        zip_obj.extract(CHAT_LOG_NAME, path=destination_path)


class WhatStats(wx.App):
    """Program which generates statistics from WhatsApp chat logs."""

    def __init__(self):
        super().__init__()
        self.frame = MainFrame()
        self.panel = self.frame.panel
        self.bind_events()

    def start(self):
        """Start program."""
        self.frame.Show()
        self.MainLoop()

    def bind_events(self):
        """Bind events to their event handlers."""
        # self.frame.Bind(wx.EVT_CLOSE, self.on_close)
        self.panel.import_button.Bind(wx.EVT_BUTTON, self.on_import)
        self.panel.generate_button.Bind(wx.EVT_BUTTON, self.on_generate)

    def on_close(self, event):
        """Ask user if they are sure they want to quit."""
        message = 'Are you sure you want to quit?'
        caption = 'WhatsApp Statistics'
        flags = wx.OK | wx.CANCEL | wx.CANCEL_DEFAULT | wx.ICON_EXCLAMATION
        with wx.MessageDialog(None, message, caption, flags) as quit_dialog:
            if quit_dialog.ShowModal() == wx.ID_OK:
                self.frame.Destroy()
            else:
                event.Veto()

    def init_inputs(self, chat):
        """Initialise inputs with data from imported chat."""
        self.panel.chat_name_input.SetValue(chat.name)
        self.panel.start_date_input.SetValue(chat.start_date)
        self.panel.end_date_input.SetValue(chat.end_date)
        self.panel.members_list.set_members(chat.members)

    def on_import(self, event):
        """
        Ask user to select archive zip, then extract it and initialise
        Chat object.
        """
        with wx.FileDialog(None, wildcard='*.zip') as file_dialog:
            if file_dialog.ShowModal() != wx.ID_CANCEL:
                zip_path = file_dialog.GetPath()
                try:
                    extract_chat_log(zip_path, str(TEMP_PATH))
                    self.chat = Chat(CHAT_LOG_PATH)
                    CHAT_LOG_PATH.unlink()
                    self.init_inputs(self.chat)
                except OSError:
                    wx.LogError('Coulnd\'t open zip file.')
                except KeyError:
                    wx.LogError('Couldn\'t extract chat log.')
                except ValueError:
                    wx.LogError('Chat log not valid.')

    def on_generate(self, event):
        """Show bar chart."""
        chat_name = self.panel.chat_name_input.GetValue()
        start = self.panel.start_date_input.GetValue()
        end = self.panel.end_date_input.GetValue()
        data = message_count_data(self.chat, start, end)
        title = 'Messages sent in chat: {}'.format(chat_name)
        show_bar_chart(data, title=title)
