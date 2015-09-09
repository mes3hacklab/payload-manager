'''
Created on 15 ago 2015
Rev 3.0
@author: Righetz,M
'''
import Engine
import tkinter as tk
from tkinter.messagebox import YESNOCANCEL
import os

class Gui():
    '''
    Render user interface using tkinter
    '''
    def __init__(self):
        '''
        Inizializing a Gui object also invokes inizialization of an Engine.py obj
        '''
        self.engine = Engine.Engine()

    def render_gui(self):
        '''
        Define User Interface components and render them to screen.
        '''
        self.payloads = self.engine.get_payloads()
        frame = tk.Tk()
        frame.title('XSS Manager')

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)
        frame.resizable(False, False)

        # TOP PANEL
        top_panel = tk.Frame(frame)
        top_panel.grid(row=0)
        label_search = tk.Label(top_panel, text="Search", width=8)
        label_search.grid(row=0, column=0)

        # SEARCH BAR STUFF INIZIALIZATIONS
        search_var = tk.StringVar()
        search_bar = tk.Entry(top_panel, textvariable=search_var, width=97, bg='white')
        search_bar.grid(row=0, column=1)
        # BOTTOM PANEL
        bottom_panel = tk.Frame(frame)
        bottom_panel.grid(row=1)
        # BOTTOM LEFT
        bottom_left = tk.Frame(bottom_panel)
        bottom_left.grid(row=0, column=0)
        list_label = tk.Label(bottom_left, text='Payload List')
        list_label.grid(row=0, column=0)
        #payload list listbox
        self.payload_list = tk.Listbox(bottom_left, width=30, height=28, bg='white')
        self.payload_list.grid(row=1, column=0)
        # payload list's scrollbar
        scrollbar_list = tk.Scrollbar(bottom_left, command=self.payload_list.yview)
        scrollbar_list.grid(row=1, column=1, sticky='nsew')
        self.payload_list['yscrollcommand'] = scrollbar_list.set

        # BOTTOM RIGHT
        bottom_right = tk.Frame(bottom_panel)
        bottom_right.grid(row=0, column=1)

        # BUTTON CONTAINER
        button_container = tk.Frame(bottom_right)
        button_container.grid(row=0)
        button_save = tk.Button(button_container, text='Save',
                                width=21, command=self.__save())
        button_save.grid(row=0, column=1)

        button_delete = tk.Button(button_container, text='Delete',
                                  width=21, command=self.__delete)
        button_delete.grid(row=0, column=2)

        # PAYLOAD CONTAINER
        payload_container = tk.Frame(bottom_right)
        payload_container.grid(row=1)

        # HEADING CONTAINER
        heading_container = tk.Frame(payload_container)
        heading_container.grid(row=0)

        title_label = tk.Label(heading_container, text='Title', width=12)
        title_label.grid(row=0, column=0)
        self.title = tk.Entry(heading_container, width=60, bg='white')
        self.title.grid(row=0, column=1)

        tags_label = tk.Label(heading_container, text='Tags', width=12)
        tags_label.grid(row=1, column=0)
        self.tags = tk.Entry(heading_container, width=60, bg='white')
        self.tags.grid(row=1, column=1)

        description_label = tk.Label(heading_container, text='Description', width=12)
        description_label.grid(row=2, column=0)
        self.description = tk.Entry(heading_container, width=60, bg='white')
        self.description.grid(row=2, column=1)
        # CODE CONTAINER
        code_container = tk.Frame(payload_container)
        code_container.grid(row=1)
        self.code = tk.Text(code_container, width=80, height=25, bg='white')
        self.code.grid(row=0, column=0)
        scrollbar = tk.Scrollbar(code_container, command=self.code.yview)
        scrollbar.grid(row=0, column=1, sticky='nsew')
        self.code['yscrollcommand'] = scrollbar.set
        button_new = tk.Button(button_container, text='New',
                               command=self.__get_new_payload_callback(heading_container), width=21)
        button_new.grid(row=0, column=0)
        self.__search_filter(self.payloads, search_var)
        self.__populate_list()
        self.current_selection = {}
        frame.mainloop()

    def __populate_list(self):
        '''
        Inserts payload titles into payload list.
        '''
        self.payload_list.delete(0, tk.END)
        for payload in self.payloads:
            self.payload_list.insert(tk.END, payload['title'])
        self.payload_list.bind('<<ListboxSelect>>', self.__display_attributes(self.payloads))

    def __display_attributes(self, payloads):
        '''
        After populating list, bind a selected item with the corresponding value fields to display.
        '''
        def callback(e):
            self.title.delete(0, tk.END)
            self.tags.delete(0, tk.END)
            self.description.delete(0, tk.END)
            self.code.delete(1.0, tk.END)
            current_title = self.payload_list.curselection()[0]
            self.current_selection = payloads[current_title]
            self.title.insert(tk.END, payloads[current_title]['title'])
            self.tags.insert(tk.END, ", ".join(payloads[current_title]['tags']))
            self.description.insert(tk.END, payloads[current_title]['description'])
            self.code.insert(tk.END, payloads[current_title]['code'])
        return callback


    def __get_new_payload_callback(self, heading_container):
        '''
        Action for "new" button. Deletes what's inside payload values fields.
        '''
        def callback():
            if not self.current_selection == {}:
                if (not (self.current_selection['title'] == self.title.get()) or
                    not (self.current_selection['tags'] == self.tags.get().split(', ')) or
                    not (self.current_selection['description'] == self.description.get()) or
                    not (self.current_selection['code'].strip() == self.code.get(1.0, tk.END).strip())):
                    choice = tk.messagebox.askquestion('Changes detected',
                                                      'Continue without saving current edited payload?')
                    if choice == 'yes':
                        self.title.delete(0, tk.END)
                        self.tags.delete(0, tk.END)
                        self.description.delete(0, tk.END)
                        self.code.delete(1.0, tk.END)
                        self.current_selection = {}
                    if choice == 'no':
                        self.__save()()
                else:
                    self.__clear_fields()
                    self.current_selection = {}
            else:
                self.__clear_fields()
        return callback

    def __search_filter(self, payloads, search_var):
        '''
        Filters payload list depending on search bar inputs.
        '''
        search_var.trace('w', lambda name, index, mode: self.__update_list(search_var, payloads))
        self.__update_list(search_var, self.payloads)

    def __update_list(self, search_var, payloads):
        '''
        After payload list's filtering, insert eligible elements into it.
        '''
        self.updated_list = []
        self.search_query = search_var.get()
        self.payload_list.delete(0, tk.END)
        self.payloads = self.engine.get_payloads()
        for self.payload in self.payloads:
            found = True
            for search_term in self.search_query.split(' '):
                if (search_term.lower() not in self.payload['title'].lower() and
                        search_term.lower() not in ",".join(self.payload['tags']) and
                        search_term.lower() not in self.payload['description'] and
                        search_term.lower() not in self.payload['code']):
                    found = False
                    break
            if found:
                self.payload_list.insert(tk.END, self.payload['title'])
                self.updated_list.append(self.payload['title'])
        self.payloads = self.engine.update_values(self.updated_list)
        self.payload_list.bind('<<ListboxSelect>>', self.__display_attributes(self.payloads))
        
    def __save(self):
        '''
        Action for save button. Checks if file exists or not,
        then replace or create file saving data in it.
        '''
        def callback_save():
            if 'title' in self.current_selection:
                old_title = self.current_selection['title']
                new_payload = False
            else:
                new_payload = True
            self.current_selection['title'] = self.title.get()
            self.current_selection['description'] = self.description.get()
            self.current_selection['tags'] = self.tags.get().split(', ')
            self.current_selection['code'] = self.code.get(1.0, tk.END)
            if self.code.get(1.0, tk.END).strip() and self.title.get().strip() and new_payload == False:
                path = self.engine.path
                if not os.path.isfile(path +
                                      self.current_selection['title'].replace(' ', '_') + '.json'):
                    self.result = tk.messagebox.askquestion('Save new',
                                                            'Save as new file?', type=YESNOCANCEL)
                    if self.result == 'yes':
                        self.engine.save_file(self.current_selection, False)
                    elif self.result == 'no':
                        self.engine.save_file(self.current_selection, False)
                        os.remove(path + old_title.replace(' ', '_') + '.json')
                else:
                    self.engine.save_file(self.current_selection, True)
            else:
                self.engine.save_file(self.current_selection, False)
            self.payloads = self.engine.get_payloads()
            self.__populate_list()
        return callback_save

    def __delete(self):
        '''
        show message box and call delete_file if answer is yes. Refresh payload list afterwards
        '''
        if not self.current_selection == {}:
            choice = tk.messagebox.askquestion('Delete payload', 'Are you sure you want to delete?')
            if choice == 'yes':
                self.engine.delete_file(self.current_selection['title'])
                self.payloads = self.engine.get_payloads()
                self.__populate_list()
                self.__clear_fields()
                self.current_selection = {}
                
    def __clear_fields(self):
        '''
        Delete title,description,tags,code fields,making them empty
        '''
        self.title.delete(0, tk.END)
        self.tags.delete(0, tk.END)
        self.description.delete(0, tk.END)
        self.code.delete(1.0, tk.END)
