import wx
import wx.adv
import wx.lib.mixins.listctrl as listmixin
from ObjectListView import ObjectListView, ColumnDefn

COLUMN_WIDTH = 150


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
        self.subject_input = wx.TextCtrl(self, size=(COLUMN_WIDTH, -1))
        self.statistic_choices = StatisticChoices(self, COLUMN_WIDTH)
        self.chart_style_choices = ChartStyleChoices(self, COLUMN_WIDTH)
        self.start_date_input = wx.adv.DatePickerCtrl(self)
        self.end_date_input = wx.adv.DatePickerCtrl(self)
        self.members_list = MembersList(self, COLUMN_WIDTH)
        self.generate_button = wx.Button(self, label='Generate Chart')
        self.init_layout()

    def init_layout(self):
        """Add inputs and options to frame."""
        details_sizer = wx.StaticBoxSizer(wx.VERTICAL, self, 'Chat Details')
        details_grid = wx.FlexGridSizer(2, 2, 0, 5)
        subject_text = wx.StaticText(self, label='Subject')
        members_text = wx.StaticText(self, label='Members')
        details_grid.Add(subject_text)
        details_grid.Add(members_text)
        details_grid.Add(self.subject_input)
        details_grid.Add(self.members_list)
        details_sizer.Add(details_grid, flag=wx.ALL & ~wx.TOP, border=5)

        options_sizer = wx.StaticBoxSizer(wx.VERTICAL, self, 'Options')
        options_grid = wx.FlexGridSizer(3, 2, 0, 5)
        start_text = wx.StaticText(self, label='Start Date',
                                   size=(COLUMN_WIDTH, -1))
        end_text = wx.StaticText(self, label='End Date')
        options_grid.Add(self.statistic_choices, flag=wx.BOTTOM, border=10)
        options_grid.Add(self.chart_style_choices)
        options_grid.Add(start_text)
        options_grid.Add(end_text)
        options_grid.Add(self.start_date_input)
        options_grid.Add(self.end_date_input)
        options_sizer.Add(options_grid, flag=wx.ALL & ~wx.TOP, border=5)

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(details_sizer, flag=wx.ALL, border=10)
        main_sizer.Add(options_sizer, 0, wx.ALL & ~wx.TOP | wx.EXPAND, 10)
        main_sizer.Add(self.generate_button, 0, wx.ALIGN_CENTRE | wx.ALL, 5)

        self.SetSizer(main_sizer)


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


class StatisticChoices(wx.RadioBox):
    """Static box containing options for statistic."""

    CHOICES = [
        'Messages sent',
        'Words sent',
    ]

    def __init__(self, parent, width):
        super().__init__(parent, label='Statistic', majorDimension=1,
                         choices=self.CHOICES, size=(width, -1))


class ChartStyleChoices(wx.RadioBox):
    """Static box containing options for chart style."""

    CHOICES = [
        'Doughnut chart',
        'Bar chart',
    ]

    def __init__(self, parent, width):
        super().__init__(parent, label='Chart Style', majorDimension=1,
                         choices=self.CHOICES, size=(width, -1))


class CloseDialog(wx.MessageDialog):
    """Dialog shown when user quits which asks if they are sure."""

    def __init__(self, parent):
        message = 'Are you sure you want to quit?'
        caption = 'WhatStats'
        flags = wx.OK | wx.CANCEL | wx.CANCEL_DEFAULT | wx.ICON_EXCLAMATION
        super().__init__(parent, message, caption, flags)
        self.CentreOnParent()


class ImportDialog(wx.FileDialog):
    """Dialog shown where user chooses chat log zip to import."""

    def __init__(self, parent):
        message = 'Import'
        style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
        wildcard = '*.zip'
        super().__init__(parent=parent, message=message, style=style,
                         wildcard=wildcard)
        self.CentreOnParent()


class LoadingDialog(wx.ProgressDialog):
    """
    Dialog shown when chat is being imported which contains loading bar
    and status message.
    """

    def __init__(self, parent):
        title = 'WhatStats'
        style = (wx.PD_SMOOTH | wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME
                 | wx.PD_CAN_ABORT)
        super().__init__(parent=parent, message='Importing chat log...',
                         title=title, style=style)
        self.CentreOnParent()
