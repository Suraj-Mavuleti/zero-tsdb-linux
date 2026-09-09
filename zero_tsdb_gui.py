import sys
import gi
import os
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib

class ZeroTSDB(Gtk.Window):
    def __init__(self):
        super().__init__(title="Zero TSDB - Ultimate Studio")
        self.set_default_size(1200, 800)
        
        self.header = Gtk.HeaderBar()
        self.header.set_show_close_button(True)
        self.header.props.title = ""
        self.header.get_style_context().add_class("hidden-header")
        self.set_titlebar(self.header)
        
        self.setup_css()
        
        main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.add(main_box)
        
        # ================= SIDEBAR =================
        self.sidebar = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.sidebar.set_size_request(260, -1)
        self.sidebar.get_style_context().add_class("sidebar")
        main_box.pack_start(self.sidebar, False, False, 0)
        
        logo = Gtk.Label(label="Z E R O T S D B")
        logo.get_style_context().add_class("sidebar-logo")
        logo.set_margin_top(20)
        logo.set_margin_bottom(20)
        self.sidebar.pack_start(logo, False, False, 0)
        
        lbl_cluster = Gtk.Label(label="CLUSTERS")
        lbl_cluster.get_style_context().add_class("section-label")
        lbl_cluster.set_halign(Gtk.Align.START)
        lbl_cluster.set_margin_start(20)
        self.sidebar.pack_start(lbl_cluster, False, False, 10)
        
        for c in ["Production DB", "Staging DB", "Analytics Cache"]:
            btn = Gtk.Button(label="📊 " + c)
            btn.get_style_context().add_class("cluster-btn")
            btn.set_alignment(0.0, 0.5)
            self.sidebar.pack_start(btn, False, False, 2)
            
        # ================= MAIN WORKSPACE =================
        self.workspace = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.workspace.get_style_context().add_class("workspace")
        main_box.pack_start(self.workspace, True, True, 0)
        
        top_bar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        top_bar.set_margin_start(30)
        top_bar.set_margin_end(30)
        top_bar.set_margin_top(20)
        
        title = Gtk.Label(label="Production DB Metrics")
        title.get_style_context().add_class("dash-title")
        top_bar.pack_start(title, False, False, 0)
        
        btn_refresh = Gtk.Button(label="🔄 Refresh")
        btn_refresh.get_style_context().add_class("action-btn")
        top_bar.pack_end(btn_refresh, False, False, 0)
        
        self.workspace.pack_start(top_bar, False, False, 20)
        
        grid = Gtk.Grid(column_spacing=20, row_spacing=20)
        grid.set_margin_start(30)
        grid.set_margin_end(30)
        self.workspace.pack_start(grid, True, True, 0)
        
        grid.attach(self.make_chart_card("Query Latency (p99)", "14 ms", True), 0, 0, 2, 1)
        grid.attach(self.make_chart_card("Ingestion Rate", "45,000 pts/s", False), 0, 1, 1, 1)
        grid.attach(self.make_chart_card("Disk Usage", "84% (4.2 TB)", False), 1, 1, 1, 1)
        
    def make_chart_card(self, title, val, big):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.get_style_context().add_class("chart-card")
        if big:
            box.set_size_request(800, 300)
        else:
            box.set_size_request(390, 250)
            
        t = Gtk.Label(label=title)
        t.get_style_context().add_class("chart-title")
        t.set_halign(Gtk.Align.START)
        t.set_margin_start(20)
        t.set_margin_top(20)
        
        v = Gtk.Label(label=val)
        v.get_style_context().add_class("chart-val")
        v.set_halign(Gtk.Align.START)
        v.set_margin_start(20)
        v.set_margin_top(10)
        
        # Fake chart area
        c_area = Gtk.Box()
        c_area.get_style_context().add_class("chart-area")
        c_area.set_margin_start(20)
        c_area.set_margin_end(20)
        c_area.set_margin_bottom(20)
        c_area.set_margin_top(10)
        
        box.pack_start(t, False, False, 0)
        box.pack_start(v, False, False, 0)
        box.pack_start(c_area, True, True, 0)
        return box
        
    def setup_css(self):
        css = b'''
            window { background-color: #030305; }
            .hidden-header { background: #030305; min-height: 0px; padding: 0px; border: none; box-shadow: none; }
            .sidebar { background-color: rgba(6, 8, 12, 0.98); border-right: 1px solid rgba(255, 255, 255, 0.05); }
            .sidebar-logo { color: #FFFFFF; font-size: 20px; font-weight: 900; letter-spacing: 5px; text-shadow: 0 0 15px rgba(255, 204, 0, 0.6); }
            .section-label { color: #4A5568; font-size: 11px; font-weight: 900; letter-spacing: 2px; }
            .cluster-btn { background: transparent; color: #8B94A5; border: none; box-shadow: none; padding: 12px 20px; font-size: 14px; font-weight: bold; }
            .cluster-btn:hover { background: rgba(255, 255, 255, 0.05); color: #FFFFFF; }
            .workspace { background: radial-gradient(circle at top right, #10141E, #030305); }
            .dash-title { color: #FFFFFF; font-size: 28px; font-weight: bold; }
            .action-btn { background: linear-gradient(45deg, #FFCC00, #FF9900); color: #000000; border-radius: 8px; font-weight: bold; padding: 10px 20px; border: none; box-shadow: 0 5px 15px rgba(255, 204, 0, 0.3); transition: all 0.3s; }
            .action-btn:hover { box-shadow: 0 8px 25px rgba(255, 204, 0, 0.5); }
            .chart-card { background: rgba(255,255,255,0.02); border: 1px solid rgba(255, 204, 0, 0.2); border-radius: 16px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); transition: all 0.3s ease; }
            .chart-card:hover { border: 1px solid #FFCC00; box-shadow: 0 15px 40px rgba(255, 204, 0, 0.2); }
            .chart-title { color: #8B94A5; font-size: 14px; text-transform: uppercase; letter-spacing: 1px; }
            .chart-val { color: #FFCC00; font-size: 36px; font-weight: 200; text-shadow: 0 0 15px rgba(255, 204, 0, 0.3); }
            .chart-area { background: rgba(0,0,0,0.3); border-radius: 8px; border: 1px solid rgba(255,255,255,0.05); }
        '''
        provider = Gtk.CssProvider()
        provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

if __name__ == "__main__":
    win = ZeroTSDB()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
