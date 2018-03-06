import wx
import wx.adv


class MainWindow(wx.Frame):
    """Main GUI Window."""
    def __init__(self):
        style = wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX)
        super().__init__(None, title="WhatsApp Statistics", style=style)
        self.Bind(wx.EVT_CLOSE, self.on_close_window)
        box_sizer = wx.BoxSizer()
        box_sizer.Add(MainPanel(self))
        self.SetSizerAndFit(box_sizer)

    def on_close_window(self, event):
        """
        Ask user if they are sure and close window if the answer is yes.
        """
        message = 'Are you sure you want to quit?'
        caption = 'WhatsApp Statistics'
        flags = wx.OK | wx.CANCEL | wx.CANCEL_DEFAULT | wx.ICON_EXCLAMATION
        question = wx.MessageDialog(None, message, caption, flags)
        answer = question.ShowModal()
        self.Destroy() if answer == wx.ID_OK else event.Veto()

    def on_exit(self, event):
        """Close window."""
        self.Close()


class MainPanel(wx.Panel):
    """Main panel which contains window title and inputs."""
    def __init__(self, parent):
        super().__init__(parent)
        self.vertical_box = wx.BoxSizer(wx.VERTICAL)
        self.init_title()
        self.init_open_button()
        self.init_inputs()
        self.init_generate_button()
        self.SetSizer(self.vertical_box)

    def init_title(self):
        """Create title and add to vertical box."""
        font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        font.SetPointSize(2 * font.GetPointSize())
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        title = wx.StaticText(self, label='WhatsApp Statistics Generator')
        title.SetFont(font)
        flags = wx.TOP | wx.LEFT | wx.RIGHT | wx.ALIGN_CENTRE
        self.vertical_box.Add(title, flag=flags, border=10)

    def init_open_button(self):
        """Create open button and add to vertical box."""
        self.open_button = wx.Button(self, label='Open Archive')
        self.Bind(wx.EVT_BUTTON, self.on_open, self.open_button)
        flags = wx.TOP | wx.LEFT | wx.RIGHT | wx.ALIGN_CENTRE
        self.vertical_box.Add(self.open_button, flag=flags, border=15)

    def init_inputs(self):
        """Create inputs and add to vertical box."""
        grid = wx.FlexGridSizer(4, 2, 15, 5)
        chat_name_text = wx.StaticText(self, label='Chat Name:')
        self.chat_name = wx.TextCtrl(self)
        self.chat_name.Disable()
        start_date_text = wx.StaticText(self, label='Start Date:')
        self.start_date = wx.adv.DatePickerCtrl(self, style=wx.adv.DP_DEFAULT)
        self.start_date.Disable()
        end_date_text = wx.StaticText(self, label='End Date:')
        self.end_date = wx.adv.DatePickerCtrl(self, style=wx.adv.DP_DEFAULT)
        self.end_date.Disable()
        members_text = wx.StaticText(self, label='Members:')
        self.members_dropdown = wx.ComboBox(self, style=wx.CB_READONLY)
        self.members_dropdown.Disable()
        grid.AddMany([
                     (chat_name_text, 0, wx.ALIGN_CENTER_VERTICAL),
                     (self.chat_name),
                     (start_date_text, 0, wx.ALIGN_CENTER_VERTICAL),
                     (self.start_date),
                     (end_date_text, 0, wx.ALIGN_CENTER_VERTICAL),
                     (self.end_date),
                     (members_text, 0, wx.ALIGN_CENTER_VERTICAL),
                     (self.members_dropdown),
                     ])
        self.vertical_box.Add(grid, flag=wx.TOP | wx.ALIGN_CENTRE, border=15)

    def init_generate_button(self):
        """Create generate button and add to vertical box."""
        self.generate_button = wx.Button(self, label="Generate Statistics")
        self.generate_button.Disable()
        flags = wx.ALIGN_CENTRE | wx.TOP | wx.BOTTOM
        self.vertical_box.Add(self.generate_button, flag=flags, border=15)

    def on_open(self, event):
        print('open')


app = wx.App()
frame = MainWindow()
frame.Show()
app.MainLoop()
