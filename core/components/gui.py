import wx
import wx.adv


class MainFrame(wx.Frame):
    def __init__(self):
        style = wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX)
        super().__init__(None, title="WhatsApp Statistics", style=style)
        self.panel = MainPanel(self)
        self.init_layout()

    def init_layout(self):
        """Add main panel to frame and fit frame around it."""
        sizer = wx.BoxSizer()
        sizer.Add(self.panel)
        self.SetSizerAndFit(sizer)


class MainPanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.import_button = wx.Button(self, label='Open Archive')
        self.chat_name_input = wx.TextCtrl(self)
        self.chat_name_input.Disable()
        self.start_date_picker = wx.adv.DatePickerCtrl(self)
        self.start_date_picker.Disable()
        self.end_date_picker = wx.adv.DatePickerCtrl(self)
        self.end_date_picker.Disable()
        self.members_dropdown = wx.ComboBox(self, style=wx.CB_READONLY)
        self.members_dropdown.Disable()
        self.generate_button = wx.Button(self, label="Generate Statistics")
        self.generate_button.Disable()
        self.init_layout()

    def init_layout(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        grid = wx.FlexGridSizer(4, 2, 15, 5)

        title_font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        title_font.SetPointSize(2 * title_font.GetPointSize())
        title_font.SetWeight(wx.FONTWEIGHT_BOLD)
        title = wx.StaticText(self, label='WhatsApp Statistics Generator')
        title.SetFont(title_font)

        chat_name_text = wx.StaticText(self, label='Chat Name:')
        start_date_text = wx.StaticText(self, label='Start Date:')
        end_date_text = wx.StaticText(self, label='End Date:')
        members_text = wx.StaticText(self, label='Members:')

        grid.Add(chat_name_text, flag=wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self.chat_name_input)
        grid.Add(start_date_text, flag=wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self.start_date_picker)
        grid.Add(end_date_text, flag=wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self.end_date_picker)
        grid.Add(members_text, flag=wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self.members_dropdown)

        flags = wx.TOP | wx.ALIGN_CENTRE
        sizer.Add(title, flag=flags | wx.LEFT | wx.RIGHT, border=10)
        sizer.Add(self.import_button, flag=flags, border=15)
        sizer.Add(grid, flag=flags, border=15)
        sizer.Add(self.generate_button, flag=flags | wx.BOTTOM, border=15)
        self.SetSizer(sizer)
