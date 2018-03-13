import wx
import wx.adv
import wx.lib.mixins.listctrl as listmixin
from ObjectListView import ObjectListView, ColumnDefn


class MainFrame(wx.Frame):
    """Main window of GUI."""

    def __init__(self):
        style = wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX)
        super().__init__(None, title="WhatStats", style=style)
        self.opening_panel = OpeningPanel(self)
        self.main_panel = MainPanel(self)
        self.menu_bar = MainMenuBar()
        self.init_layout()

    def init_layout(self):
        """Add panels to main sizer and show opening panel."""
        self.main_sizer = wx.BoxSizer()
        self.main_sizer.Add(self.opening_panel)
        self.main_sizer.Add(self.main_panel)
        self.main_panel.Hide()
        self.SetSizerAndFit(self.main_sizer)

    def set_main_layout(self):
        """Hide opening panel and show main panel."""
        self.opening_panel.Hide()
        self.SetMenuBar(self.menu_bar)
        self.main_panel.Show()
        self.main_sizer.Fit(self)


class OpeningPanel(wx.Panel):
    """Panel shown on opening which contains title and import button."""

    def __init__(self, parent):
        super().__init__(parent)
        self.import_button = wx.Button(self, label='Import Chat Log')
        self.init_layout()

    def init_layout(self):
        sizer = wx.BoxSizer(wx.VERTICAL)

        title_font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        title_font.SetPointSize(4 * title_font.GetPointSize())
        title_font.SetWeight(wx.FONTWEIGHT_BOLD)
        title = wx.StaticText(self, label='WhatStats')
        title.SetFont(title_font)

        sizer.Add(title, flag=wx.ALIGN_CENTRE | wx.LEFT | wx.RIGHT, border=30)
        sizer.Add(self.import_button, flag=wx.ALIGN_CENTRE | wx.ALL, border=30)
        self.SetSizer(sizer)


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


class MembersList(ObjectListView, listmixin.ListCtrlAutoWidthMixin):
    """
    List control that contains member objects and updates them when
    their name is edited.
    """
    def __init__(self, parent, width):
        style = wx.LC_REPORT | wx.LC_NO_HEADER
        super().__init__(parent, style=style, size=(width, -1), sortable=False)
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
