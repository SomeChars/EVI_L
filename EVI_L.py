from os import listdir
from time import localtime
from matplotlib.pyplot import Figure,rc
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import Tk,Label,Entry,Button,Scale,HORIZONTAL
from tkinter.ttk import Treeview
import tkcalendar as tc



class InputVariables:
    def __init__(self): 
        #window
        self.window = Tk()
        self.window.geometry("300x115")
        #self.window.title('Input Variables')
        
        #default result
        self.result = ['nothing','data',10]
        self.valid = '0123456789'
        
        #texts
        eoz_text = Label(self.window,anchor="nw",text="Пациент",font=("Inter", 14 * -1),fg='#1E1E1E')
        eoz_text.place(x=10.0,y=10.0)
        
        date_text = Label(self.window,anchor="nw",text="Окно рассчёта ИВЭ",font=("Inter", 14 * -1),fg='#1E1E1E')
        date_text.place(x=10.0,y=45.0)

        #register validation method for inputs
        self.validation_method = (self.window.register(self.validate_input),'%P')
        
        #Patient input
        self.entry1 = Entry(self.window,bd=3,bg="#FFFFFF",fg="#1E1E1E",highlightthickness=0)
        self.entry1.place(x=90.0,y=10.0,width=200.0,height=25.0)
        
        #evi_window input
        self.entry2 = Entry(self.window,bd=3,bg="#FFFFFF",fg="#1E1E1E",highlightthickness=0,
                             validate='key',validatecommand=self.validation_method)
        self.entry2.place(x=175.0,y=45.0,width=50.0,height=25.0)
        
        #submit button
        self.button1 = Button(self.window,borderwidth=0,highlightthickness=0,
                                    command = lambda: self.post(),bg='#AEAEAE',fg='#1E1E1E',anchor='s',
                                    relief="raised",text='Подтвердить',font=("Inter", 14 * -1))
        self.button1.place(x=75.0,y=80,width=150.0,height=25.0)
        
        #draw window
        self.window.mainloop()

    def update_input(self):
        v1,v2 = self.get_input()
        good_input = self.validate_values(v1,v2)
        return good_input,v1,v2   
    
    def get_input(self):    
        v1 = self.entry1.get().strip()
        v2 = self.entry2.get().strip()
        return v1,v2
    
    def validate_values(self,v1,v2):
        #check empty fields
        if v1 == '' or v2 == '':
            return False
        #check if not intable or too big
        try:
            if int(v2) > 1e6:
                return False
        except:
            return False
        
        #if all good
        return True
    
    def validate_input(self,var):
        for l in var:
            if l not in self.valid:
                return False
        return True
    
    def post(self):
        good_input,v1,v2 = self.update_input()
        if good_input:
            self.window.quit()
            self.result = ['ok',v1,int(v2)]



class EditRow:
    def __init__(self,date,eoz):
        #window
        self.window = Tk()
        self.window.geometry("335x150")
        self.window.title('Edit Row')
        
        #default result
        self.result = ['nothing',date,eoz]
        self.valid = '0123456789.'
        
        #texts
        eoz_text = Label(self.window,anchor="nw",text="EOZ",font=("Inter", 14 * -1),fg='#1E1E1E')
        eoz_text.place(x=10.0,y=45.0)
        
        date_text = Label(self.window,anchor="nw",text="Date",font=("Inter", 14 * -1),fg='#1E1E1E')
        date_text.place(x=10.0,y=80.0)

        #register validation method for inputs
        self.validation_method = (self.window.register(self.validate_input),'%P')
        
        #eoz input
        self.entry = Entry(self.window,bd=3,bg="#FFFFFF",fg="#1E1E1E",highlightthickness=0,
                             validate='key',validatecommand=self.validation_method)
        self.entry.place(x=55.0,y=45.0,width=75.0,height=25.0)
        self.entry.insert(0,str(eoz))
        
        #date input
        self.date = tc.DateEntry(self.window,bd=3,bg="#FFFFFF",fg="#000716",
                                 highlightthickness=0,date_pattern='dd/mm/yyyy')
        self.date.place(x=55.0,y=80.0,width=110,height=25)
        self.date.set_date(str(date))
        
        #submit button
        self.button1 = Button(self.window,borderwidth=0,highlightthickness=0,
                                    command = lambda: self.post('change'),bg='#AEAEAE',fg='#1E1E1E',anchor='s',
                                    relief="raised",text='Изменить',font=("Inter", 14 * -1))
        self.button1.place(x=175.0,y=10,width=150.0,height=25.0)
        
        #delete button
        self.button2 = Button(self.window,borderwidth=0,highlightthickness=0,
                                 command = lambda: self.post('delete'),bg='#AEAEAE',fg='#1E1E1E',anchor='s',
                                 relief="raised",text='Удалить',font=("Inter", 14 * -1))
        self.button2.place(x=175,y=45,width=150.0,height=25.0)
        
        #insert above button
        self.button3 = Button(self.window,borderwidth=0,highlightthickness=0,
                                 command = lambda: self.post('insert_above'),bg='#AEAEAE',fg='#1E1E1E',anchor='s',
                                relief="raised",text='Вставить выше',font=("Inter", 14 * -1))
        self.button3.place(x=175.0,y=80,width=150.0,height=25.0)
        
        #insert below button
        self.button4 = Button(self.window,borderwidth=0,highlightthickness=0,
                                    command = lambda: self.post('insert_below'),bg='#AEAEAE',fg='#1E1E1E',anchor='s',
                                    relief="raised",text='Вставить ниже',font=("Inter", 14 * -1))
        self.button4.place(x=175.0,y=115,width=150.0,height=25.0)
        
        #draw window
        self.window.mainloop()
        
        
    def update_input(self):
        v1,v2 = self.get_input()
        good_input = self.validate_values(v1,v2)
        return good_input,v1,v2   
    
    def get_input(self):    
        v1 = self.entry.get().strip().replace(',','.')
        v2 = str(self.date.get_date())
        return v1,v2
    
    def validate_values(self,v1,v2):
        #check empty fields
        if v1 == '':
            return False
        #check correct date
        for l in v2:
            if l not in self.valid.replace('.','')+'-':
                return False
        #check if not floatable or too big
        try:
            if float(v1) > 1e9:
                return False
        except:
            return False
        
        #if all good
        return True
    
    def validate_input(self,var):
        for l in var:
            if l not in self.valid:
                return False
        return True
    
    def post(self,var):
        good_input,v1,v2 = self.update_input()
        if good_input:
            self.window.quit()
            self.result = [var,'/'.join(v2.split('-')[::-1]),float(v1)]



class EVI_L:
    def __init__(self):
        
        # create InputVariables window to ask for variables
        input_variables = InputVariables()
        if input_variables.result[0] == 'ok':
            self.fn = input_variables.result[1] + '.txt'
            self.EVI_WINDOW = input_variables.result[2]
            input_variables.window.destroy()
        else:
            self.fn = 'data' + '.txt'
            self.EVI_WINDOW = 10

        # magic parameter - idk how it works
        self.graph_empty_space = 1/2

        self.valid='0123456789.'
        self.slider_exists = False
        rc('xtick', labelsize=min(round(8*10/self.EVI_WINDOW),8))
        
        # create window
        self.window = Tk()
        self.window.geometry("800x600")
        self.window.title(input_variables.result[1])
        
        # texts
        leyc = Label(self.window,anchor="nw",text="Лейкоцитов на 1 мкл крови",font=("Inter", 14 * -1),fg='#1E1E1E')
        leyc.place(x=10.0,y=450.0)
        eoz_percent = Label(self.window,anchor="nw",text="Процент эозинофилов",font=("Inter", 14 * -1),fg='#1E1E1E')
        eoz_percent.place(x=10.0,y=485.0)
        self.eoz_text = Label(self.window,anchor="nw",text="Эозинофилов в 1 мкл крови",font=("Inter", 14 * -1),fg='#1E1E1E')
        self.eoz_text.place(x=10.0,y=520.0)
        date_text = Label(self.window,anchor="nw",text="Дата",font=("Inter", 14 * -1),fg='#1E1E1E')
        date_text.place(x=10.0,y=555.0)
        
        # register validation method for inputs
        self.validation_method = (self.window.register(self.validate_input),'%P','%W')
        
        # leyc input
        self.entry1 = Entry(self.window,bd=3,bg="#FFFFFF",fg="#1E1E1E",highlightthickness=0,
                              validate='key',validatecommand=self.validation_method)
        self.entry1.place(x=250.0,y=450.0,width=75.0,height=25.0)

        # %eoz input
        self.entry2 = Entry(self.window,bd=3,bg="#FFFFFF",fg="#1E1E1E",highlightthickness=0,
                              validate='key',validatecommand=self.validation_method)
        self.entry2.place(x=250.0,y=485.0,width=75.0,height=25.0)

        # date input
        self.date = tc.DateEntry(self.window,bd=3,bg="#FFFFFF",fg="#1E1E1E",
                                 highlightthickness=0,date_pattern='dd/mm/yyyy')
        self.date.place(x=60.0,y=555.0,width=110,height=25)

        # submit button
        self.button1 = Button(self.window,borderwidth=0,highlightthickness=0,
                                    command = lambda: self.post(),bg='#AEAEAE',fg='#1E1E1E',anchor='center',
                                    relief="raised",text='Подтвердить',font=("Inter", 14 * -1,'bold'))
        self.button1.place(x=230.0,y=552,width=120.0,height=30.0)

        # eoz output
        self.entry3 = Entry(self.window,bd=0,highlightthickness=0,fg="#1E1E1E",
                               font=("Inter", 18 * -1),state='readonly')
        self.entry3.place(x=250.0,y=520.0,width=75,height=25)
        
        # evi_output
        self.entry4 = Entry(self.window,bd=0,highlightthickness=0,fg="#1E1E1E",
                               font=("Inter", 28 * -1),state='readonly')
        self.entry4.place(x=460.0,y=450.0,width=220,height=50)

        # warning
        self.warning = Label(self.window,anchor="nw",text='',font=("Inter", 14 * -1),fg='#1E1E1E')
        self.warning.place(x=400.0,y=500.0)

        # create plot & table
        self.create_table()
        self.create_plot()

        # draw plot & plot_slider & eoz (order matters)
        eoztl = len(self.table.data['EOZ']) - self.EVI_WINDOW
        if eoztl > 0:
            self.create_slider(eoztl)
        self.update_plot()
        if self.table.data['EOZ']:
            self.update_evi()
        self.entry1.focus_set()

        self.window.mainloop()
    
    def create_plot(self):
        self.fig = Figure(figsize=(5,4.26))
        self.ax = self.fig.add_subplot()
        self.fig.tight_layout(pad=3)
        self.canvas = FigureCanvasTkAgg(figure=self.fig,master=self.window)
        self.canvas.get_tk_widget().place(x=292.0,y=6.0)

    def create_table(self):
        input_data = self.data_input('file')
        columns = ['№']+list(input_data.keys())
        self.table = Treeview(master=self.window,columns=columns,show='headings',
                                     height=20,selectmode='browse')
        self.table.heading(column=columns[0],text=columns[0])
        self.table.column(column=columns[0],width=30,anchor='center')
        for column in columns[1:]:
            self.table.heading(column=column,text=column)
            self.table.column(column=column,width=120,anchor='center')
        for i in range(len(input_data[list(input_data.keys())[0]])):
            self.table.insert(parent='',index='end',values=[i+1]+[input_data[k][i] for k in input_data])
        self.table.place(x=7.0,y=6.0)
        self.table.data = input_data
        self.table.bind("<Double-Button-1>", self.on_double_mouse_click)

    def data_input(self,source='file'):
        if source == 'file':
            return self.file_input()

    def file_input(self):
        data = {'Date':[],'EOZ':[]}
        if self.fn not in listdir('.'):
            with open(self.fn,'w') as f:
                f.write('Date,EOZ')
        else:
            with open(self.fn,'r') as f:
                for l in f.readlines()[1:]:
                    data['Date'] += [l.split(',')[0].strip()]
                    data['EOZ'] += [float(l.split(',')[1].strip())]
        return data
    
    def update_data(self,source='file'):
        if source == 'file':
            self.update_file()

    def update_file(self):
        keys = list(self.table.data.keys())
        with open(self.fn,'w') as f:
            f.write(','.join(keys))
            for i in range(len(self.table.data['EOZ'])):
                f.write(f"\n{self.table.data['Date'][i]},{self.table.data['EOZ'][i]}")
    
    def append_to_file(self,new_date,new_eoz):
        with open(self.fn,'a') as f:
            f.write(f'\n{new_date},{new_eoz}')
    
    def update_input(self):
        v1,v2,v3 = self.get_input()
        good_input = self.validate_values(v1,v2,v3)
        if good_input:
            self.reset_input(v1,v2,v3)
        return good_input,v1,v2,v3    
    
    def get_input(self):    
        v1 = self.entry1.get().strip()
        v2 = self.entry2.get().strip()
        v3 = str(self.date.get_date())
        return v1,v2,v3
    
    def validate_values(self,v1,v2,v3):
        # check empty fields
        if v1 == '' or v2 == '':
            return False
        # check correct date
        for l in v3:
            if l not in self.valid.replace('.','')+'-':
                return False
        # check if not floatable or too big
        try:
            if float(v1) > 1e9 or float(v2) > 1e2:
                return False
        except:
            return False
        
        # if all good
        return True

    def reset_input(self,v1,v2,v3):
        tl=localtime()
        self.entry1.delete(0,len(v1))
        self.entry2.delete(0,len(v2))
        self.date.set_date(f'{tl[2]}/{tl[1]}/{tl[0]}')
        self.entry1.focus_set()
    
    def change_entry_text(self,entry,new_text):
        # change entry state to normal to insert text, then lock it in readonly,
        # so the text inside is copyable
        if entry == 3:
            text = self.entry3.get()
            self.entry3.configure(state='normal')
            self.entry3.delete(0,len(text))
            self.entry3.insert(0,new_text)
            self.entry3.configure(state='readonly')
        elif entry == 4:
            text = self.entry4.get()
            self.entry4.configure(state='normal')
            self.entry4.delete(0,len(text))
            self.entry4.insert(0,new_text)
            self.entry4.configure(state='readonly')

    def validate_input(self,var,widget):
        for l in var:
            if l not in self.valid:
                return False
        v1,v2,v3 = self.get_input()
        # there're two entry inupt wigets with vals v1,v2,
        # which change to var dependig on in which one user is typing      
        if widget == '.!entry':
            if self.validate_values(var,v2,v3):
                self.change_entry_text(3,str(round(float(var)*float(v2)/100,2)))
            else:
                self.change_entry_text(3,'')
        else: 
            if self.validate_values(v1,var,v3):
                self.change_entry_text(3,str(round(float(v1)*float(var)/100,2)))
            else:
                self.change_entry_text(3,'')
        return True
    
    def create_slider(self,slider_len):
        #creates a slider with $slider_len points
        self.plot_slider = Scale(self.window,orient=HORIZONTAL,length=390,from_=0,to=slider_len,
                                    command=self.move_slider,showvalue=0)
        self.plot_slider.set(slider_len)
        self.plot_slider.place(x=350,y=435)
        # see update_slider
        self.slider_exists = True

    def move_slider(self,var):
        self.update_plot()
        
    def update_slider(self,insert = 1):
        # slider can switch states as:
        # 1. not exists -> not exists (no need to handle)
        # 2. not exists -> exists
        # 3. exists -> not exists
        # 4. exists -> exists
        # thus needed a variable to check its state
        new_slider_len = len(self.table.data['EOZ'])-self.EVI_WINDOW
        #3
        if self.slider_exists and new_slider_len == 0:
            self.plot_slider.destroy()
            self.slider_exists = False
        elif new_slider_len == 1:
            #4 (if its len becomes 1)
            if self.slider_exists:
                self.plot_slider.configure(to=1)
                if self.plot_slider.get() == 2:
                    self.plot_slider.set(1)
            #2
            else:
                self.create_slider(1)
        elif new_slider_len > 1:
            #4 
            self.plot_slider.configure(to=new_slider_len)
            if self.plot_slider.get() == new_slider_len-1:
                self.plot_slider.set(self.plot_slider.get()+insert)
    
    def update_table(self,v1,v2,v3):
        new_eoz = round(float(v1)*float(v2)/100,2)
        new_date = '/'.join(v3.split('-')[::-1])
        self.append_to_file(new_date,new_eoz)
        self.table.data['Date'] += [new_date]
        self.table.data['EOZ'] += [new_eoz]
        self.table.insert(parent='',index='end',values=[len(self.table.data['EOZ']),new_date,new_eoz])
        self.update_slider()
            
    def update_plot(self):
        pos = 0
        if self.slider_exists:
            pos = self.plot_slider.get()
        maxt = 1
        mint = 0
        if self.table.data['EOZ']:
            maxt = max(self.table.data['EOZ'])
            mint = min(self.table.data['EOZ'])
        points = self.table.data['EOZ'][pos:pos+self.EVI_WINDOW]
        self.ax.clear()
        self.ax.set_title('EOZ')
        self.ax.set_xticks([i for i in range(len(points))],labels=self.table.data['Date'][pos:pos+self.EVI_WINDOW],rotation=30)
        # sometimes they're equal
        if max(mint-(maxt-mint)*self.graph_empty_space/2,0) < maxt+(maxt-mint)*self.graph_empty_space/2:
            self.ax.set_ylim([max(mint-(maxt-mint)*self.graph_empty_space/2,0),
                              maxt+(maxt-mint)*self.graph_empty_space/2])
        self.ax.fill_between([i for i in range(len(points))],points,[0]*len(points),color='grey')
        self.canvas.draw()
        
        # plot redrawn -> sider moves/changes -> need to recalc evi
        self.update_evi()
           
    def update_evi(self):
        pos = 0
        if self.slider_exists:
            pos = self.plot_slider.get()
        if self.table.data['EOZ']:
            evi = round((1-min(self.table.data['EOZ'][pos:pos+self.EVI_WINDOW])/max(self.table.data['EOZ'][pos:pos+self.EVI_WINDOW]))*100,2)
            self.change_entry_text(4,f"ИВЭ={evi}%")
            if evi >= 50:
                self.warning.configure(text='Высокий риск обострения/приступа\n бронхиальной астмы')
            else:
                self.warning.configure(text='')
    
    def on_double_mouse_click(self,event):
        y = event.y
        vals = self.table.item(self.table.identify_row(y))['values']
        if vals != '':
            edit_row = EditRow(vals[1],vals[2])
            try:
                edit_row.window.destroy()
            except:
                pass
            date,eoz = edit_row.result[1],edit_row.result[2]
            if edit_row.result[0] != 'nothing':
                if edit_row.result[0] == 'change':
                    self.table.set(self.table.identify_row(y),column='Date',value=date)
                    self.table.set(self.table.identify_row(y),column='EOZ',value=eoz)
                    self.table.data['Date'][self.table.index(self.table.identify_row(y))] = date
                    self.table.data['EOZ'][self.table.index(self.table.identify_row(y))] = eoz
                elif edit_row.result[0] == 'delete':
                    self.table.delete(self.table.identify_row(y))
                    self.table.data['Date'].pop(self.table.index(self.table.identify_row(y)))
                    self.table.data['EOZ'].pop(self.table.index(self.table.identify_row(y)))  
                    self.reassign_table_index()              
                    self.update_slider(-1)
                elif edit_row.result[0] == 'insert_above':
                    index = self.table.index(self.table.identify_row(y))
                    self.table.insert(parent='',index=index,values=[0,date,eoz])
                    self.table.data['Date'].insert(index,date)
                    self.table.data['EOZ'].insert(index,eoz)
                    self.reassign_table_index() 
                    self.update_slider()
                elif edit_row.result[0] == 'insert_below':
                    index = self.table.index(self.table.identify_row(y))
                    self.table.insert(parent='',index=index+1,values=[0,date,eoz])
                    self.table.data['Date'].insert(index+1,date)
                    self.table.data['EOZ'].insert(index+1,eoz)
                    self.reassign_table_index()
                    self.update_slider()
                self.update_file()
                self.update_plot()
                self.entry1.focus_set()

    def reassign_table_index(self):
        i = 1
        for child in self.table.get_children():
            self.table.set(child,'№',i)
            i += 1
    
    def post(self):
        # on submit button read inputs
        good_input,v1,v2,v3 = self.update_input()
        if good_input:
            # if input is valid - clear eoz output & update stuff
            self.change_entry_text(3,'')
            self.update_table(v1,v2,v3)
            self.update_plot()
            self.update_evi()



EVI_L()