import wx


class MainFrame(wx.Frame):
    """Main GUI Window."""
    def __init__(self):
        super().__init__(None, title="WhatsApp Statistics")
        self.Bind(wx.EVT_CLOSE, self.on_close_window)
        self.init_menu_bar()
        box_sizer = wx.BoxSizer()
        box_sizer.Add(MainPanel(self))
        self.SetSizerAndFit(box_sizer)

    def init_menu_bar(self):
        """Initialise menu bar."""
        menu_bar = wx.MenuBar()
        file_menu = wx.Menu()
        file_menu.Append(wx.ID_OPEN, '&Open...\tCtrl+O')
        self.Bind(wx.EVT_MENU, self.on_open, id=wx.ID_OPEN)
        file_menu.Append(wx.ID_EXIT, 'Exit')
        self.Bind(wx.EVT_MENU, self.on_exit, id=wx.ID_EXIT)
        menu_bar.Append(file_menu, '&File')
        self.SetMenuBar(menu_bar)

    def on_close_window(self, event):
        """
        Ask user if they are sure and close window if the answer is yes.
        """
        question = wx.MessageDialog(None, 'Are you sure you want to quit?',
                                    'Are you sure?', wx.YES_NO | wx.NO_DEFAULT)
        answer = question.ShowModal()
        self.Destroy() if answer == wx.ID_YES else event.Veto()

    def on_open(self, event):
        print('open...')

    def on_exit(self, event):
        """Close window."""
        self.Close()


class MainPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        vertical_box = wx.BoxSizer(wx.VERTICAL)

        input_grid = wx.FlexGridSizer(4, 2, 15, 10)
        chat_name_text = wx.StaticText(self, label='Chat Name:')
        chat_name_input = wx.TextCtrl(self)
        start_date_text = wx.StaticText(self, label='Start Date:')
        start_date_input = wx.TextCtrl(self)
        end_date_text = wx.StaticText(self, label='End Date:')
        end_date_input = wx.TextCtrl(self)
        members_text = wx.StaticText(self, label='Members:')
        members_dropdown = wx.TextCtrl(self)
        input_grid.AddMany([
                        (chat_name_text, 0, wx.ALIGN_CENTER_VERTICAL),
                        (chat_name_input),
                        (start_date_text, 0, wx.ALIGN_CENTER_VERTICAL),
                        (start_date_input),
                        (end_date_text, 0, wx.ALIGN_CENTER_VERTICAL),
                        (end_date_input),
                        (members_text, 0, wx.ALIGN_CENTER_VERTICAL),
                        (members_dropdown),
                        ])
        vertical_box.Add(input_grid, flag=wx.TOP | wx.LEFT | wx.RIGHT,
                         border=5)

        generate_button = wx.Button(self, label="Generate Statistics")
        vertical_box.Add(generate_button, flag=wx.ALIGN_CENTRE | wx.TOP
                         | wx.BOTTOM, border=5)

        self.SetSizer(vertical_box)


app = wx.App()
frame = MainFrame()
frame.Show()
app.MainLoop()
