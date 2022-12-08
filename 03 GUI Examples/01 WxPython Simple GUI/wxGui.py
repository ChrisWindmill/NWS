import wx


class TextPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.label = wx.StaticText(self, label="Text window", size=(400, 330))
        self.text_ctrl = wx.TextCtrl(self)
        self.my_btn = wx.Button(self, label='Press Me')
        self.my_btn.Bind(wx.EVT_BUTTON, self.on_press)

        my_sizer_v = wx.BoxSizer(wx.VERTICAL)
        my_sizer_h = wx.BoxSizer(wx.HORIZONTAL)

        # parent, expand, flags, border, userdata
        my_sizer_h.Add(self.text_ctrl, 1, wx.ALL | wx.EXPAND, 5)
        my_sizer_h.Add(self.my_btn, 0, wx.ALL | wx.Right, 5)

        my_sizer_v.Add(self.label, 0, wx.ALL | wx.EXPAND, 0)
        my_sizer_v.Add(my_sizer_h, 0, wx.ALL | wx.EXPAND,0)

        self.SetSizer(my_sizer_v)

    def on_press(self, event):
        value = self.text_ctrl.GetValue()
        if not value:
            print("You didn't enter anything!")
        else:
            print(f'You typed: "{value}"')


class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Hello World', size=(640, 480))

        self.panel = wx.Panel(self)
        # Tab panel for clients
        self.panelWest = wx.Panel(self.panel, size=(140, 400))
        self.panelWest.SetBackgroundColour(wx.Colour(0,0,255))
        self.panelEast = wx.Panel(self.panel, size=(500, 400))
        self.panelEast.SetBackgroundColour(wx.Colour(0, 255, 255))
        self.panelSouth = wx.Panel(self.panel, size=(640, 40))
        self.panelSouth.SetBackgroundColour(wx.Colour(255, 0, 255))

        my_sizer_v = wx.BoxSizer(wx.VERTICAL)
        my_sizer_h = wx.BoxSizer(wx.HORIZONTAL)

        # parent, expand, flags, border, userdata
        my_sizer_h.Add(self.panelWest, 0, wx.ALL | wx.EXPAND, 0)
        my_sizer_h.Add(self.panelEast, 0, wx.ALL | wx.Right, 0)

        my_sizer_v.Add(my_sizer_h, 0, wx.ALL | wx.EXPAND, 0)
        my_sizer_v.Add(self.panelSouth, 0, wx.ALL | wx.EXPAND, 0)

        self.nb = wx.Notebook(self.panelEast)

        sizer = wx.BoxSizer()
        sizer.Add(self.nb, 1, wx.EXPAND)
        self.panelEast.SetSizer(sizer)

        # create the page windows as children of the notebook
        page1 = TextPanel(self.nb)
        page2 = TextPanel(self.nb)
        page3 = TextPanel(self.nb)

        # add the pages to the notebook with the label to show on the tab
        self.nb.AddPage(page1, "Page 1")
        self.nb.AddPage(page2, "Page 2")
        self.nb.AddPage(page3, "Page 3")

        # finally, put the notebook in a sizer for the panel to manage
        # the layout
        self.panel.SetSizer(my_sizer_v)

        self.Show()

if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    app.MainLoop()