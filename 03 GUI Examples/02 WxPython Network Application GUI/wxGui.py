import wx
from Server import TalkToYourServer
import threading

EVT_RESULT_ID = wx.NewIdRef(count=1)
EVT_TAB_CREATE_ID = wx.NewIdRef(count=1)


class TabCreateEvent(wx.PyEvent):
    """Simple event to carry arbitrary result data."""

    def __init__(self, data):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_TAB_CREATE_ID)
        self.data = data


class ResultEvent(wx.PyEvent):
    """Simple event to carry arbitrary result data."""
    def __init__(self, data):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_RESULT_ID)
        self.data = data


class UIInterface:
    def __init__(self, my_frame):
        self.wxframe = my_frame
        # a list of (TextPanel, Connection) instances
        self.tab_list = []

    def add_entry(self, connection):
        wx.PostEvent(self.wxframe, TabCreateEvent(connection))

    def gui_add_entry(self, connection):
        tab, tab_id = self.wxframe.add_tab(self)
        self.tab_list.append((tab_id, tab, connection))
        connection.notify(tab_id)

    def delete_entry(self, list_id):
        for tab in self.tab_list:
            tab_id, tab, connection = tab
            if tab_id == list_id:
                self.tab_list.remove(tab)
                return True
        return False

    def add_text(self, list_id, text):
        for tab in self.tab_list:
            tab_id, tab, connection = tab
            if tab_id == list_id:
                wx.PostEvent(self.wxframe, ResultEvent((tab_id, text)))
                return True
        return False

    def gui_add_text(self, list_id, text):
            for tab in self.tab_list:
                tab_id, tab, connection = tab
                if tab_id == list_id:
                    tab.add_text(text)
                    return True
            return False

    def push_network_message(self, list_id, text):
        for tab in self.tab_list:
            tab_id, tab, connection = tab
            if tab_id == list_id:
                connection.push_message(text)
                return True
        return False


class TextPanel(wx.Panel):
    def __init__(self, parent, ui_interface, tab_id):
        wx.Panel.__init__(self, parent)

        self.ui_interface = ui_interface
        self.tab_id = tab_id

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
            self.ui_interface.push_network_message(self.tab_id, value)
            print(f'You typed: "{value}"')

    def add_text(self, text):
        self.label.SetLabel(text)


class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Hello World', size=(640, 480))

        self.ui_interface = UIInterface(self)
        self.panel_count = 0

        self.EVT_RESULT(self, self.OnResult)
        self.EVT_TAB_CREATE(self, self.OnTabCreate)

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

        # # create the page windows as children of the notebook
        #         # page1 = TextPanel(self.nb, self.ui_interface)
        #         # page2 = TextPanel(self.nb, self.ui_interface)
        #         # page3 = TextPanel(self.nb, self.ui_interface)
        #         #
        #         # # add the pages to the notebook with the label to show on the tab
        #         # self.nb.AddPage(page1, "Page 1")
        #         # self.nb.AddPage(page2, "Page 2")
        #         # self.nb.AddPage(page3, "Page 3")

        # finally, put the notebook in a sizer for the panel to manage
        # the layout
        self.panel.SetSizer(my_sizer_v)

        self.server = TalkToYourServer("127.0.0.1", 50001, self.ui_interface)
        self.server.start()

        self.Show()

    def EVT_RESULT(self, win, func):
        """Define Result Event."""

        win.Connect(-1, -1, EVT_RESULT_ID, func)

    def EVT_TAB_CREATE(self, win, func):
        """Define Result Event."""

        win.Connect(-1, -1, EVT_TAB_CREATE_ID, func)

    def add_tab(self, ui_interface):
        self.panel_count = self.panel_count + 1
        tab = TextPanel(self.nb, ui_interface, self.panel_count)
        self.nb.AddPage(tab, str(self.panel_count))
        return tab, self.panel_count

    def OnResult(self, event):
        if event.data is None:
            pass
        else:
            # Process results here
            tab_id, text = event.data
            self.ui_interface.gui_add_text(tab_id, text)

    def OnTabCreate(self, event):
        if event.data is None:
            pass
        else:
            self.ui_interface.gui_add_entry(event.data)


if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    app.MainLoop()