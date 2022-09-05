from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import urllib
from bs4 import BeautifulSoup
from docx import *
from googlesearch import search
from threading import Thread
import numpy as np


LargeFont = ('AdobeHeitiStd-Regular', 14)
SmallFont = ('AdobeHeitiStd-Regular', 10)


class App:# class created to create an object which is the tkinter window
    def __init__(self,master): #initialisation of all attributes of class.
        self.master = master #the root tkinter functionality E.G. Tk()
        self.Google_Results = [] #List that will contain retrieved URL(s) from Google search 
        master.geometry('600x500') # length and width of GUI window
        title = master.title('Plagiarism Detection Software') # Name of GUI window 
        master.iconbitmap('plagiarism.ico') # Icon picture for GUI window
        self.docx = [] # List containig extracted text from word document
        self.query = ''
        self.text_file = '' # string that will contain contents of text file 
        self.Num_Of_Results = StringVar() #The data that is entered into second entry field of GUI window 
        self.Filename = StringVar() # Data thta is entered into first field in GUI window ``

        frame = Frame(master) #tkinter frame that allows widgets to be placed within its area
        frame.place(relx=0.5, rely=0.3, relwidth=0.75, relheight=0.1, anchor='n')#dimensions of frame

        bottom_frame = Frame(master)# bottom frame for second entry field
        bottom_frame.place(relx=0.5,rely=0.5,relwidth=0.75,relheight=0.1, anchor='n') 

        self.label_1 = ttk.Label(master, text='Enter Filename:', font=LargeFont)# Text displayed in the window 
        self.label_1.place(relx=0.25, rely=0.2, relwidth=0.25, relheight=0.1)

        self.label_2 = ttk.Label(master, text='Enter number of Google results:',font=LargeFont)
        self.label_2.place(relx=0.15,rely=0.4,relwidth=0.5, relheight=0.1)

        self.entry_1 = ttk.Entry(frame, textvariable=self.Filename, font=LargeFont)
        self.entry_1.place(relwidth=0.65, relheight=1) # first entry 

        self.entry_2 = ttk.Entry(bottom_frame,textvariable=self.Num_Of_Results,font=LargeFont)
        self.entry_2.place(relwidth=0.65, relheight=1) # second entry

        self.program_button = ttk.Button(frame, text='Submit', 
            command=lambda: Thread(target=self.search_google).start()) #Submit button that runs the main program through a thread                                                                                          thread to prevent freezing'''
        self.program_button.place(relx=0.7, relwidth=0.3, relheight=1)
        
        self.progress_bar = ttk.Progressbar(master, orient='horizontal', length=285, mode='indeterminate')#progress/loading bar 


    def user_entry(self): # function that calls methods for specified file format
        entry_info = self.Filename.get() # data entered into entry field is retrieved and stored as a string
        y = entry_info.endswith('.txt')#boolean variables checking if filename entered ends with correct format  
        x = entry_info.endswith('.docx')
        if y:
            self.text_file = self.extract_text() # calls extract text function
            return self.text_file
        elif x:
            self.docx = self.extract_word_docx()# calls extract word document function
            return self.docx
        else:
            messagebox.showinfo('Error', 'File format is invalid')
            return False


    def extract_text(self): # text extraction for text file format
        try:# error handling 
            entry = self.Filename.get()
            with open(entry, 'r', encoding='utf8') as f:
                text = f.read()
            User_file_txt = (text)
            return User_file_txt
        except FileNotFoundError: # run if file does not exist or not a valid filename
            messagebox.showinfo('Error', 'File does not exist')
            return False
            
            
    def extract_word_docx(self):# extract text form word document 
        entry = self.Filename.get()
        text_list = [] 
        word_obj = Document(entry)# docx module object being created
        for i in word_obj.paragraphs:
            text_list.append(i.text) # append each line to list 
            wrd_text = '\n'.join(text_list)
        return_docx = (wrd_text)
        print(return_docx)
        return return_docx


    def search_google(self):
        self.start_progress_bar()
        User_Results = self.int_validation() # run integer validation 
        self.query = self.user_entry() # runs metho d 
        if self.query is False:# selection statements to break function
            return False
        elif User_Results is False:
            return False
        else:
            self.program_button.configure(state=DISABLED) 
            Google_search = search(self.query, tld='com', lang='en', num = User_Results, 
                start=0, stop=1, pause=3) # function that searches google query is passed as parameter so it is searched 
            for i in Google_search:
                Url_source = Label(self.master, text='Url retrieved: '+i, font=SmallFont).place(relx=0.15,rely=0.1)
                self.Google_Results.append(i) # Each URL is appended to a list 
        self.extract_url_text()


    def int_validation(self):
        try: 
            String_conv = int(self.Num_Of_Results.get()) # gets data from entry and converts it to an integer
            if String_conv >= 1: # number entered has to be greater than one
                return String_conv
            else:
                messagebox.showinfo('Error', 'An integer greater than 1 must be entered')
                return False
        except ValueError: #error handling for validation that it is an integer
            messagebox.showinfo('Error', 'You did not enter an integer')
            return False


    def extract_url_text(self):
        for i in self.Google_Results: # loop for every item in list
            Str_1 = str(i)
            Url_req = urllib.request.Request(Str_1) # request of each url
            Url_text = urllib.request.urlopen(Url_req) # url is opened 
            Data = Url_text.read() # data from url is read
            Extract = BeautifulSoup(Data, 'html.parser') # Beautiful soup object is created so text can be parsed
            for i in Extract(['script', 'style']): # removal of any script (Javascript)
                i.extract()
            body = Extract.find_all('p') # every paragraph tag is searched and all text is taken fronm it 
            data_store = open('Returned Data.txt', 'w+',encoding='utf8')
            for tag in body:
                #tag = tag.text # text is extracted from <p> tags
                tag = re.sub('\[\d+\]', '', str(tag)) # regular expression thst substitutes any square brackets
                tag = re.sub('\[.*?\]','',str(tag)) # removes any empty square brackets
                Clear_text = str(tag) + '\n'
                data_store.write(Clear_text)
            data_store.seek(0) # reads file from the beginning (first character)
            text1 = data_store.read()
            data_store.close()
            str1 = text1.replace(' ','')
            self.query = self.query.replace(' ', '')
            Sliced_string = str1[0:len(self.query)]
            self.lev_distance(self.query,Sliced_string)
            self.stop_progress_bar()
            self.program_button.configure(state=NORMAL)

        
    def start_progress_bar(self):
        self.progress_bar.place(relx=0.15,rely=0.7)
        self.progress_bar.start(20)


    def stop_progress_bar(self):
        self.progress_bar.stop()
        self.progress_bar.place_forget()

    
    def lev_distance(self,str1, str2): 
        length_1 = len(self.query) + 1
        length_2 = len(str2) + 1
        Matrix = np.zeros((length_1, length_1)) # creation of numpy matrix
        for a in range(length_1):
            Matrix [a, 0] = a
        for b in range(length_1):
            Matrix [0, b] = b
        for a in range(1, length_1):
            for b in range (1, length_1):# Columns and rows of matrix are iterated through 
                if str1[a-1] == str2[b-1]:
                    Matrix [a,b] = min(   # insertions, deletions or substitutions 
                    Matrix[a-1, b] + 1,
                    Matrix[a-1, b-1],
                    Matrix[a, b-1] + 1
                    )
                else:
                    Matrix [a,b] = min(
                    Matrix[a-1,b] + 1,
                    Matrix[a-1,b-1] + 1,
                    Matrix[a,b-1] + 1
                    )
        Levdistance_count = Matrix[length_1 - 1, length_1 - 1] # last column and row position
        print(Levdistance_count)
        percentage = (1 - Levdistance_count/length_1) * 100
        if int(percentage) > 60: # percentage less then 10 is not considered as plagiarised
            Plagiarism_detected = Label(self.master,text='Percentage of plagiarsim in student\'s document is '
                                    + str(round(percentage, 2)) +
                                    '%',fg='red',font=LargeFont).pack()
        else:
            No_plagiarism = Label(self.master,text='No sufficient plagiarism or plagiarism has not been detected', 
            fg='black',font=SmallFont).pack()
        #open('Returned Data.txt', 'w').close()# removes content from text file
  

def main():
    base = Tk()
    Window_Object = App(base) # tkinter window object instantiated 
    base.mainloop()

if __name__ == "__main__":
    main()