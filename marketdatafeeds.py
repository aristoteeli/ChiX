import tkinter as tk
from tkinter.font import *
from tkinter.ttk import *

from sqlalchemy.sql.expression import insert

import marketdata as md

class  mainWnd:

    def __init__(self) -> None:

        self.root = tk.Tk()
        self.root.title('Market Data Demo V1.0')
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.screen_w = self.root.winfo_screenwidth()
        self.screen_h = self.root.winfo_screenheight()
 
        self.pane = MainFrame(self.root)
        self.pane.pack(expand=tk.TRUE,fill=tk.BOTH)

        self.d_log = tk.Text(self.root)
        # self.log_scroll  = Scrollbar(self.d_log,orient=tk.VERTICAL,command=self.d_log.yview)
        # self.d_log['yscrollcommand']=self.log_scroll.set

        self.d_log.pack(side=tk.TOP,fill=tk.BOTH,padx=3,pady=3)
        # self.log_scroll.pack(side=tk.LEFT,fill=tk.Y)

        self.root.mainloop()

    def get_root(self) :
        return self.root


class MainFrame(PanedWindow):

    def __init__(self,master) -> None:
        super().__init__(master,orient=tk.HORIZONTAL)

        self.mk_data = md.MarketData() 

        self.l_pane = self.set_l_pane()
        self.add(self.l_pane)
        self.r_pane = self.set_r_pane()
        self.add(self.r_pane)
    
        self.set_l_meta_name()
        self.set_r_meta_def()

    def set_l_pane(self):
        l_pane = Frame(self)

        self.l_meta_name = Treeview(l_pane,columns=('#1'), show='headings')
        self.l_meta_name.pack(side=tk.LEFT,expand=tk.TRUE,fill=tk.BOTH,padx=(3,1),pady=(23,3))
        self.l_meta_name.bind('<ButtonRelease-1>', self.onLeftSelectRow)
        self.l_meta_name.bind('<ButtonRelease-3>', self.onLeftMenu)

        self.m_scroll  = Scrollbar(l_pane,orient=tk.VERTICAL,command=self.onScroll)
        self.l_meta_name['yscrollcommand']=self.m_scroll.set
        self.m_scroll.pack(side=tk.LEFT,fill=tk.Y)

        return l_pane

    def set_r_pane(self):

        r_pane = Notebook(self)
        r_pane.pack(pady=5, expand=True)

        self.r_meta_def = Treeview(self)
        self.r_meta_def['yscrollcommand']=self.m_scroll.set
        self.r_meta_def.pack(side=tk.LEFT,fill=tk.Y)
        self.r_meta_def.bind('<ButtonRelease-1>', self.onRightSelectRow)
        self.r_meta_def.bind('<ButtonRelease-3>', self.onRightMenu)

        r_pane.add(self.r_meta_def, text='series definitions')
        r_pane.pack(side=tk.LEFT,expand=tk.TRUE,fill=tk.BOTH)

        return r_pane

    def onScroll(self,*args):
        self.l_meta_name.yview(*args)
        self.r_meta_def.yview(*args)
    
    def onLeftSelectRow(self, event):
        self.r_meta_def.selection_set(self.l_meta_name.selection())

    def onRightSelectRow(self, event):
        self.l_meta_name.selection_set( self.r_meta_def.selection())

    def onLeftMenu(self,event):
        it = self.l_meta_name.identify_row(event.y)
        if it in self.l_meta_name.selection():
            m = LaunchFeedMenu(self)
            m.tk_popup(event.x_root,event.y_root)

    def onRightMenu(self,event):
        it = self.r_meta_def.identify_row(event.y)
        if it in self.r_meta_def.selection():
            m = SetMetadatasMenus(self)
            m.tk_popup(event.x_root,event.y_root)
            
    def get_selected_item(self):
        items = self.r_meta_def.selection()
        return items

    def set_l_meta_name(self):
        self.l_meta_name.heading('#1',text='Indicateur')
        meta_names = []
        for k,v in self.mk_data.series_metadata.items() :
           self.l_meta_name.insert('', tk.END, values=v.name)


        # tree_view.bind('<<TreeviewOpen>>', open_node)
        # tree_view.bind('<<TreeviewClose>>', close_node)
        # self.l_content.bind('<<TreeviewSelect>>', item_selected)

    def set_r_meta_def(self):

        headings = self.mk_data.get_series_col()

        col_idx =[]
        cols =[]

        for i,v in enumerate(headings):
           col_idx.append(f'#{i+1}')
           cols.append(v)

        self.r_meta_def['columns']=cols
        self.r_meta_def['show']='headings'

        for i,v in enumerate(headings):
            self.r_meta_def.heading(f'#{i+1}',text=f'{v}')

        for k,v in self.mk_data.series_metadata.items() :
            r=[] 
            for c in cols:    
                r.append(f'{getattr(v,c)}')

            self.r_meta_def.insert('', tk.END, values=r)        

    def lv_get_item(self):
        pass


class LaunchFeedMenu(tk.Menu):
    def __init__(self, master) -> None:
        super().__init__(master=master)
        self.add_command(label="Run Feeds",command=self.dummy)

    def dummy(self):
        print("LaunchFeedMenu")


class SetMetadatasMenus(tk.Menu):
    def __init__(self, master) -> None:
        super().__init__(master=master)
        self.add_command(label="Reset",command=self.dummy)
        self.add_command(label="Save",command=self.dummy)

    def dummy(self):
        print("SetMetadatasMenus")

# class SeriesMetadata(Treeview):

#     def __init__(self, master, ) -> None:
#         super().__init__(master=master, columns=columns, 
#                          cursor=cursor, displaycolumns=displaycolumns, 
#                          height=height, name=name, padding=padding, 
#                          selectmode=selectmode, show=show, style=style, 
#                          takefocus=takefocus, xscrollcommand=xscrollcommand, 
#                          yscrollcommand=yscrollcommand)

class EntryPopup(Entry):

    def __init__(self, parent, iid, text, **kw):
        ''' If relwidth is set, then width is ignored '''
        super().__init__(parent, **kw)
        self.tv = parent
        self.iid = iid

        self.insert(0, text) 
        # self['state'] = 'readonly'
        # self['readonlybackground'] = 'white'
        # self['selectbackground'] = '#1BA1E2'
        self['exportselection'] = False

        self.focus_force()
        self.bind("<Return>", self.on_return)
        self.bind("<Control-a>", self.select_all)
        self.bind("<Escape>", lambda *ignore: self.destroy())

    def on_return(self, event):
        self.tv.item(self.iid, text=self.get())
        self.destroy()

    def select_all(self, *ignore):
        ''' Set selection on the whole text '''
        self.selection_range(0, 'end')

        # returns 'break' to interrupt default key-bindings
        return 'break'
