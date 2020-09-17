#!/usr/bin/python3.8
# -*- coding: utf-8 -*-
import sqlite3
import tkinter as tk
from tkinter import ttk


def open_update_dialog():
    Update()


def open_dialog():
    Child()


class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.search_img = tk.PhotoImage(file='icons/search.png')
        self.add_img = tk.PhotoImage(file='icons/plus.png')
        self.update_img = tk.PhotoImage(file='icons/edit.png')
        self.eye_img = tk.PhotoImage(file='icons/eye.png')
        self.delete_img = tk.PhotoImage(file='icons/clear.png')
        self.sort_img = tk.PhotoImage(file='icons/sort.png')
        self.init_main()
        self.db = db
        self.view_records()

    def init_main(self):  # main window
        toolbar = tk.Frame(bg='#d7d8e0', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        btn_open_dialog = tk.Button(
            toolbar, text='', command=open_dialog,
            bg='#d7d8e0', bd=5, compound=tk.TOP, image=self.add_img)
        btn_open_dialog.pack(side=tk.LEFT)

        btn_edit_dialog = tk.Button(
            toolbar, text='', bg='#d7d8e0', bd=5,
            image=self.update_img, compound=tk.TOP,
            command=open_update_dialog)
        btn_edit_dialog.pack(side=tk.LEFT)

        btn_eye = tk.Button(
            toolbar, text='', bg='#d7d8e0', bd=5, image=self.eye_img,
            compound=tk.TOP, command=self.view_records)
        btn_eye.pack(side=tk.RIGHT)

        btn_delete_records = tk.Button(
            toolbar, text='', bg='#aa5f5f', bd=5, image=self.delete_img,
            compound=tk.TOP, command=self.delete_records)
        btn_delete_records.pack(side=tk.LEFT)

        search_toolbar = tk.Frame(bd=10)
        search_toolbar.pack(side=tk.TOP, fill=tk.X)

        self.label1 = ttk.Label(
            search_toolbar, text="Type:", font=("Helvetica", 18))
        self.label1.pack(side=tk.LEFT)

        self.check_combobox1 = ttk.Combobox(search_toolbar, width=32, values=[
            u'<--->',
            u'Lighting',
            u'Power supply',
            u'Equipment',
            u'Other'
        ])
        self.check_combobox1.current(0)
        self.check_combobox1.pack(side=tk.LEFT)

        self.label2 = ttk.Label(search_toolbar, text="Corpus:",
                                font=("Helvetica", 18))
        self.label2.pack(side=tk.LEFT)

        self.check_combobox2 = ttk.Combobox(search_toolbar, values=[
            u'<--->',
            u'1 corpus',
            u'2 corpus',
            u'3 corpus'
        ])
        self.check_combobox2.current(0)
        self.check_combobox2.pack(side=tk.LEFT)

        self.label3 = ttk.Label(search_toolbar, text="Stage:",
                                font=("Helvetica", 18))
        self.label3.pack(side=tk.LEFT)

        self.check_combobox3 = ttk.Combobox(search_toolbar, values=[
            u'<--->',
            u'1 stage',
            u'2 stage',
            u'3 stage'
        ])
        self.check_combobox3.current(0)
        self.check_combobox3.pack(side=tk.LEFT)

        btn_sort = tk.Button(
            search_toolbar, text='', bg='#d7d8e0', bd=5, image=self.sort_img,
            compound=tk.TOP, command=self.sort_records)
        btn_sort.pack(side=tk.LEFT)

        search_line = tk.Frame(bd=10)
        search_line.pack(side=tk.TOP, fill=tk.X)

        self.entry_search = tk.Entry(
            search_line, width=110, bd=6, text='Search')
        self.entry_search.insert(0, '')
        self.entry_search.place(x=40, y=10)
        self.entry_search.pack(side=tk.LEFT)
        btn_search = tk.Button(
            search_line, text='', bg='#d7d8e0', bd=5, image=self.search_img,
            compound=tk.TOP, command=self.search_records)
        btn_search.pack(side=tk.LEFT)

        self.tree = ttk.Treeview(
            self, columns=('ID', 'description', 'corpus', 'stage', 'obj'),
            height=17, show='headings')
        self.tree.column('ID', width=35, anchor=tk.CENTER)
        self.tree.column('description', width=190, anchor=tk.CENTER)
        self.tree.column('corpus', width=110, anchor=tk.CENTER)
        self.tree.column('stage', width=100, anchor=tk.CENTER)
        self.tree.column('obj', width=400, anchor=tk.CENTER)
        self.tree.heading('ID', text='ID')
        self.tree.heading('description', text='Type')
        self.tree.heading('corpus', text='Corpus')
        self.tree.heading('stage', text='Stage')
        self.tree.heading('obj', text='Description')
        self.vsb = ttk.Scrollbar(orient="vertical", command=self.tree.yview)
        self.vsb.place(x=680 + 150, y=200, height=400)
        self.tree.configure(yscrollcommand=self.vsb.set)
        self.tree.pack(side=tk.BOTTOM)

        style = ttk.Style()
        style.configure("Treeview.Heading", font=(None, 18))
        style.configure("Treeview", rowheight=25, font=('Consolas', 14))

    def add_records(self, description, corpus, stage, obj):
        self.db.insert_data(description, corpus, stage, obj)
        self.view_records()

    def update_record(self, description, corpus, stage, obj):
        self.db.c.execute(
            '''UPDATE table1 SET description=?, 
            corpus=?, stage=?, obj=? WHERE ID=?''',
            (description, corpus, stage, obj,
             self.tree.set(self.tree.selection()[0], '#1')))
        self.db.conn.commit()
        self.view_records()

    def view_records(self):
        self.db.c.execute('''SELECT * FROM table1''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert(
            '', 'end', values=row) for row in self.db.c.fetchall()]

    def sort_records(self):
        """Sort records by parameters."""
        if self.check_combobox1.get() != '<--->' \
                and self.check_combobox2.get() == '<--->' \
                and self.check_combobox3.get() == '<--->':
            self.db.c.execute(
                '''SELECT * FROM table1 WHERE description=? ''',
                [self.check_combobox1.get()])
            self.search_func()
        elif self.check_combobox2.get() != '<--->' \
                and self.check_combobox1.get() == '<--->' \
                and self.check_combobox3.get() == '<--->':
            self.db.c.execute(
                '''SELECT * FROM table1 WHERE corpus=? ''',
                [self.check_combobox2.get()])
            self.search_func()
        elif self.check_combobox3.get() != '<--->' \
                and self.check_combobox1.get() == '<--->' \
                and self.check_combobox2.get() == '<--->':
            self.db.c.execute('''SELECT * FROM table1 WHERE stage=? ''',
                              [self.check_combobox3.get()])
            self.search_func()

        elif self.check_combobox1.get() != '<--->' \
                and self.check_combobox2.get() != '<--->':
            self.db.c.execute(
                '''SELECT * FROM table1 WHERE description=? AND corpus=? ''',
                [self.check_combobox1.get(), self.check_combobox2.get()])
            self.search_func()
            if self.check_combobox3.get() != '<--->':
                self.db.c.execute(
                    '''SELECT * FROM table1 WHERE 
                    description=? AND corpus=? AND stage=?''',
                    [self.check_combobox1.get(), self.check_combobox2.get(),
                     self.check_combobox3.get()])
                self.search_func()
        elif self.check_combobox1.get() != '<--->' \
                and self.check_combobox3.get() != '<--->':
            self.db.c.execute(
                '''SELECT * FROM table1 WHERE description=? AND stage=? ''',
                [self.check_combobox1.get(), self.check_combobox3.get()])
            self.search_func()
            if self.check_combobox2.get() != '<--->':
                self.db.c.execute(
                    '''SELECT * FROM table1 WHERE 
                    description=? AND corpus=? AND stage=?''',
                    [self.check_combobox1.get(), self.check_combobox2.get(),
                     self.check_combobox3.get()])
        elif self.check_combobox2.get() != '<--->' \
                and self.check_combobox3.get() != '<--->':
            self.db.c.execute(
                '''SELECT * FROM table1 WHERE corpus=? AND stage=? ''',
                [self.check_combobox2.get(), self.check_combobox3.get()])
            self.search_func()
            if self.check_combobox1.get() != '<--->':
                self.db.c.execute('''SELECT * FROM table1 
                WHERE description=? AND corpus=? AND stage=?''',
                                  [self.check_combobox1.get(),
                                   self.check_combobox2.get(),
                                   self.check_combobox3.get()])

    def search_records(self):
        """Search records by name(description)."""
        self.db.c.execute(
            '''SELECT * FROM table1 WHERE obj= ?''', [self.entry_search.get()])
        self.search_func()

    def search_func(self):
        search_list = self.db.c.fetchall()
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in search_list]

    def delete_records(self):
        for selection_item in self.tree.selection():
            self.db.c.execute(
                '''DELETE FROM table1 WHERE id=?''',
                [(self.tree.set(selection_item, '#1'))])
        self.db.conn.commit()
        self.view_records()


class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.btn_ok = ttk.Button(self, text='Add')
        self.entry_obj = ttk.Entry(self)
        self.third_combobox = ttk.Combobox(self, values=[
            u'1 stage',
            u'2 stage',
            u'3 stage'
        ])
        self.second_combobox = ttk.Combobox(self, values=[
            u'1 corpus',
            u'2 corpus',
            u'3 corpus'
        ])
        self.first_combobox = ttk.Combobox(self, values=[
            u'Lighting',
            u'Power supply',
            u'Equipment',
            u'Other'
        ])
        self.init_child()
        self.view = app

    def init_child(self):
        self.title('add equipment')
        self.geometry('500x300+400+300')
        self.resizable(False, False)

        label_description = tk.Label(self, text='Type:')
        label_description.place(x=50, y=50)
        label_select = tk.Label(self, text='Corpus:')
        label_select.place(x=50, y=80)
        label_stage = tk.Label(self, text='Stage:')
        label_stage.place(x=50, y=110)
        label_obj = tk.Label(self, text='Description:')
        label_obj.place(x=50, y=140)

        self.first_combobox.current(0)
        self.first_combobox.place(x=200, y=50)

        self.second_combobox.current(0)
        self.second_combobox.place(x=200, y=80)

        self.third_combobox.current(0)
        self.third_combobox.place(x=200, y=110)

        self.entry_obj.place(x=200, y=140)

        btn_cancel = ttk.Button(self, text='Close', command=self.destroy)
        btn_cancel.place(x=300, y=170)

        self.btn_ok.place(x=220, y=170)
        self.btn_ok.bind(
            '<Button-1>', lambda event: self.view.add_records(
                self.first_combobox.get(),
                self.second_combobox.get(),
                self.third_combobox.get(),
                self.entry_obj.get())
        )
        self.grab_set()
        self.focus_set()


class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app

    def init_edit(self):
        self.title('edit')
        btn_edit = ttk.Button(self, text='Edit')
        btn_edit.place(x=195, y=170)
        btn_edit.bind('<Button-1>', lambda event: self.view.update_record(
            self.first_combobox.get(),
            self.second_combobox.get(),
            self.third_combobox.get(),
            self.entry_obj.get()))
        self.btn_ok.destroy()


class DB:
    def __init__(self):
        self.conn = sqlite3.connect('sqlite3.db')
        self.c = self.conn.cursor()
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS table1 (id integer primary key,
             description text, corpus text, stage text, obj text)''')
        self.conn.commit()

    def insert_data(self, description, corpus, stage, obj):
        self.c.execute(
            '''INSERT INTO table1(description, corpus, stage, obj)
             VALUES (?, ?, ?, ?)''', (description, corpus, stage, obj)
        )
        self.conn.commit()


if __name__ == "__main__":
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title("db-table interface")
    root.geometry("850x600+300+200")
    root.resizable(False, False)
    root.mainloop()
