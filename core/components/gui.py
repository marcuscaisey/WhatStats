import wx
import wx.adv
import wx.lib.mixins.listctrl as listmixin
from ObjectListView import ObjectListView, ColumnDefn


class MainFrame(wx.Frame):
    """Main window of GUI."""

    def __init__(self):
        style = wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX)
        super().__init__(None, title="WhatStats", style=style)
        self.panel = MainPanel(self)
        self.menu_bar = MainMenuBar()
        self.init_layout()

    def init_layout(self):
        """Add panel to main sizer and set menu bar."""
        main_sizer = wx.BoxSizer()
        main_sizer.Add(self.panel)
        self.SetMenuBar(self.menu_bar)
        self.SetSizerAndFit(main_sizer)
        self.Centre()


class MainMenuBar(wx.MenuBar):
    """Main menu bar for frame."""

    def __init__(self):
        super().__init__()
        file_menu = wx.Menu()
        file_menu.Append(wx.ID_OPEN, 'Import Chat Log\tCtrl+O')
        file_menu.Append(wx.ID_EXIT, 'Quit\tCtrl+Q')
        self.Append(file_menu, '&File')


class MainPanel(wx.Panel):
    """Main panel which contains inputs and options."""

    def __init__(self, parent):
        super().__init__(parent)
        self.subject_input = wx.TextCtrl(self, size=(150, -1))
        self.start_date_input = wx.adv.DatePickerCtrl(self)
        self.end_date_input = wx.adv.DatePickerCtrl(self)
        self.members_list = MembersList(self, 150)
        self.generate_button = wx.Button(self, label="Generate Statistics")
        self.init_layout()
        self.toggle_inputs()

    def init_layout(self):
        """Add inputs and options to frame."""
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        details_sizer = wx.StaticBoxSizer(wx.VERTICAL, self, 'Chat Details')
        details_grid = wx.FlexGridSizer(2, 2, 0, 5)
        options_sizer = wx.StaticBoxSizer(wx.VERTICAL, self, 'Options')
        options_grid = wx.FlexGridSizer(2, 2, 0, 5)

        subject_text = wx.StaticText(self, label='Subject:')
        members_text = wx.StaticText(self, label='Members:')
        start_date_text = wx.StaticText(self, label='Start Date:')
        start_date_text.SetMinSize((155, -1))
        end_date_text = wx.StaticText(self, label='End Date:')

        details_grid.Add(subject_text, flag=wx.LEFT, border=5)
        details_grid.Add(members_text, flag=wx.RIGHT, border=5)
        details_grid.Add(self.subject_input, flag=wx.LEFT, border=5)
        details_grid.Add(self.members_list, flag=wx.RIGHT, border=5)

        options_grid.Add(start_date_text, flag=wx.LEFT, border=5)
        options_grid.Add(end_date_text, flag=wx.RIGHT, border=5)
        options_grid.Add(self.start_date_input, flag=wx.LEFT, border=5)
        options_grid.Add(self.end_date_input, flag=wx.RIGHT, border=5)

        main_sizer.Add((-1, 10))
        details_sizer.Add(details_grid)
        details_sizer.Add((-1, 5))
        main_sizer.Add(details_sizer, flag=wx.LEFT | wx.RIGHT, border=10)
        main_sizer.Add((-1, 10))
        options_sizer.Add(options_grid)
        options_sizer.Add((-1, 5))
        main_sizer.Add(options_sizer, 0, wx.LEFT | wx.RIGHT | wx.EXPAND, 10)
        main_sizer.Add(self.generate_button, 0, wx.ALIGN_CENTRE | wx.ALL, 15)
        self.SetSizer(main_sizer)

    def toggle_inputs(self):
        """Enable/disable inputs."""
        enable = False if self.subject_input.IsEnabled() else True
        self.subject_input.Enable(enable)
        self.start_date_input.Enable(enable)
        self.end_date_input.Enable(enable)
        self.generate_button.Enable(enable)

    def init_inputs(self, chat):
        """Initialise inputs with data from chat."""
        self.subject_input.SetValue(chat.subject)
        self.start_date_input.SetValue(chat.start_date)
        self.end_date_input.SetValue(chat.end_date)
        self.members_list.set_members(chat.members)
        self.toggle_inputs()


class MembersList(ObjectListView, listmixin.ListCtrlAutoWidthMixin):
    """
    List control that contains member objects and updates them when
    their name is edited.
    """
    def __init__(self, parent, width):
        stl = wx.LC_REPORT | wx.LC_NO_HEADER | wx.BORDER_SUNKEN
        super().__init__(parent, style=stl, size=(width, 100), sortable=False)
        self.cellEditMode = ObjectListView.CELLEDIT_DOUBLECLICK
        self.useAlternateBackColors = False
        self.SetEmptyListMsg('')
        self.setResizeColumn(0)
        self.SetColumns([
            ColumnDefn('', valueGetter='name', valueSetter='name')
        ])

    def set_members(self, members):
        """Set list to list of members."""
        self.SetObjects(members)
