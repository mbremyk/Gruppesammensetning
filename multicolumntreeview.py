from tkinter import *
from tkinter import font
from tkinter.ttk import *


class MultiColumnTreeView(Frame):
    def __init__(self, master, columns, data, text, **kw):
        super().__init__(master, **kw)
        self.master = master
        self.columns = columns
        self.data = data
        self.text = text
        self.label = None
        self.tree = None
        self.__setupwidgets()
        self.__buildtree()

    def __setupwidgets(self):
        frame = Frame(self.master)
        frame.pack(fill=BOTH, expand=1)

        self.label = Label(frame, text=self.text)
        self.label.grid(column=0, row=0, sticky='nw')

        self.tree = Treeview(frame, columns=self.columns, show='headings', selectmode='browse')
        self.tree.grid(column=0, row=1, sticky='nsew')

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)

    def __buildtree(self):
        for col in self.columns:
            self.tree.heading(col, text=col.title(), command=lambda c=col: self.__sortby(self.tree, c, 0))
            self.tree.column(col, width=font.Font().measure(col.title()))
        for item in self.data:
            self.tree.insert('', 'end', values=item)
            # adjust column's width if necessary to fit each value
            for ix, val in enumerate(item):
                col_w = font.Font().measure(val)
                if self.tree.column(self.columns[ix], width=None) < col_w:
                    self.tree.column(self.columns[ix], width=col_w)
        pass

    def __sortby(self, tree, col, descending):
        """sort tree contents when a column header is clicked on"""
        # grab values to sort
        data = [(tree.set(child, col), child)
                for child in tree.get_children('')]
        # if the data to be sorted is numeric change to float
        # data =  change_numeric(data)
        # now sort the data in place
        data.sort(reverse=descending)
        for ix, item in enumerate(data):
            tree.move(item[1], '', ix)
        # switch the heading so it will sort in the opposite direction
        tree.heading(col, command=lambda c=col: self.__sortby(tree, c, int(not descending)))
