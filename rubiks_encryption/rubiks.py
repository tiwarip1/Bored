#!/usr/bin/env python
import copy
import random 
import sys
import pyperclip
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QCheckBox,  QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox, QInputDialog, QLabel
from PyQt5.QtGui import *  
from PyQt5.QtCore import QSize 

def threeD_cube(n,name):
    
    face_l=[]
    
    #name='MonaLisa2@#$'
    decoded_l=s_to_bitlist(name)
    
    for i in range(0,6):
        row_l=[]
        for j in range(0,n):
            column_l=[]
            for k in range(0,n):
                try:
                    column_l.append(decoded_l[i*n**2+j*n+k])
                except UnboundLocalError:
                    print('password must be 12 digits long')
                    sys.exit()
            row_l.append(column_l)
        face_l.append(row_l)
    return face_l

def format_threeD(face_l):
    for i in range(0,6):
        for j in range(0,len(face_l[0])):
            print(face_l[i][j])
        print('\n')

def change_face(face_l,direction,inverted=False):
    face_l=face_change(face_l,direction,inverted)
    side_change(face_l,direction,inverted)
    return face_l
    
def side_change(face_l,side,inverted=False):
    
    count_1=0
    count_2=0
    count_3=0
    count_4=0
    
    if side == 'right':
        column_num=-1
        list_of_faces=[face_l[2],face_l[4],face_l[0],face_l[5]]
    elif side == 'left':
        column_num=0
        list_of_faces=[face_l[0],face_l[5],face_l[2],face_l[4]]
    elif side == 'top':
        row_up=0
        row_down=-1
        #list_row=[face_l[1],face_l[2],face_l[3],face_l[5]]
    elif side == 'bottom':
        row_up=-1
        row_down=0
        #list_row=[face_l[1],face_l[5],face_l[3],face_l[2]]        
    
    if side == 'left' or side == 'right':
        
        columns_left=list(zip(*list_of_faces[2]))
        columns_bottom=list(zip(*list_of_faces[1]))
        columns_top=list(zip(*list_of_faces[0]))
        columns_right=list(zip(*list_of_faces[3]))

        if (side =='left' and inverted==False) or (side == 'right' and inverted == False):
            rotate_order=[0,1,2,3]
        else:
            rotate_order=[3,2,1,0]
        
        for i in list_of_faces[rotate_order[0]]:
            i[column_num]=list(zip(*columns_bottom))[count_1][column_num]
            count_1+=1
        for i in list_of_faces[rotate_order[1]]:
            i[column_num]=list(zip(*columns_right))[count_2][column_num]
            count_2+=1
        for i in list_of_faces[rotate_order[2]]:
            i[column_num]=list(zip(*columns_top))[count_3][column_num]
            count_3+=1
        for i in list_of_faces[rotate_order[3]]:
            i[column_num]=list(zip(*columns_left))[count_4][column_num]
            count_4+=1
                                    
    elif (side=='top' and inverted==True) or (side=='bottom' and inverted==False):
        
        rotate_clockwise=[face_l[5][row_down],face_l[1][row_up],face_l[2][row_up],face_l[3][row_up]]
        face_l[5][row_down]=list(reversed(rotate_clockwise[3]))
        face_l[1][row_up]=list(reversed(rotate_clockwise[0]))
        face_l[2][row_up]=rotate_clockwise[1]
        face_l[3][row_up]=rotate_clockwise[2]
        
    elif (side == 'top' and inverted==False) or (side=='bottom' and inverted==True):
        
        rotate_counter=[face_l[2][row_up],face_l[3][row_up],face_l[5][row_down],face_l[1][row_up]]
        face_l[5][row_down]=list(reversed(rotate_counter[3]))
        face_l[1][row_up]=rotate_counter[0]
        face_l[2][row_up]=rotate_counter[1]
        face_l[3][row_up]=list(reversed(rotate_counter[2]))
        
    elif side=='front' or side=='back':
        
        rotate_left_fake=list(zip(*face_l[1]))
        rotate_bottom=face_l[4]
        rotate_right_fake=list(zip(*face_l[3]))
        rotate_top=face_l[0]
        
        rotate_right=[]
        rotate_left=[]
        
        for i in range(0,len(rotate_left_fake)):
            rotate_rig=[]
            rotate_lef=[]
            for j in range(0,len(rotate_left_fake[0])):
                rotate_lef.append(rotate_left_fake[i][j])
                rotate_rig.append(rotate_right_fake[i][j])
            rotate_left.append(rotate_lef)
            rotate_right.append(rotate_rig)

        if side=='front':
            row_down = 0
            row_up=-1
        else:
            row_down=-1
            row_up=0

        if (side=='front' and inverted==False) or (side=='back' and inverted==True):            
            rotate_order=[rotate_left,rotate_top,rotate_right,rotate_bottom]
            rotate_order[0]=list(zip(*reversed(rotate_order[0])))
            rotate_order[1]=list(zip(*reversed(rotate_order[1])))
            rotate_order[2]=list(zip(*reversed(rotate_order[2])))
            rotate_order[3]=list(zip(*reversed(rotate_order[3])))
        else:          
            rotate_order=[rotate_right,rotate_bottom,rotate_left,rotate_top]
            rotate_order[0]=list(reversed(list(zip(*rotate_order[0]))))
            rotate_order[1]=list(reversed(list(zip(*rotate_order[1]))))
            rotate_order[2]=list(reversed(list(zip(*rotate_order[2]))))
            rotate_order[3]=list(reversed(list(zip(*rotate_order[3]))))
            
        for i in face_l[3]:
            i[row_down]=rotate_order[1][count_1][row_down]
            count_1+=1
        for i in face_l[1]:
            i[row_up]=rotate_order[3][count_2][row_up]
            count_2+=1 
        face_l[4][row_down]=list(list(zip(*reversed(rotate_order[2])))[row_up])
        face_l[0][row_up]=list(list(zip(*reversed(rotate_order[0])))[row_down]) 
            
    #format_threeD(face_l)
    #print('#####################')
    
    
def face_change(face_l,side,inverted=False):
    
    item_l=[]
    thing_l=[]
    other=[]
    
    if side == 'right':
        face_num=3
    elif side == 'left':
        face_num=1
    elif side == 'top':
        face_num=0
    elif side == 'bottom':
        face_num=4
    elif side == 'front':
        face_num=2
    elif side == 'back':
        face_num=5
    else:
        print('face side name is incorrect')
    
    for i in face_l[face_num]:
        item_l.append(i)
    column_l=list(zip(*item_l))
    if inverted == False:
        for i in range(0,len(column_l)):
            row_l=[]
            for j in range(0,len(column_l[0])):
                row_l.append(column_l[i][j])
            thing_l.append(list(reversed(row_l)))
        face_l[face_num]=thing_l
    else:
        for i in range(0,len(column_l)):
            row_l=[]
            for j in range(0,len(column_l[0])):
                row_l.append(column_l[i][j])
            thing_l.append(list(row_l))
        thing_l=list(reversed(thing_l))
        for i in thing_l:
            thingy_l=[]
            for j in i:
                thingy_l.append(j)
            other.append(thingy_l)
        face_l[face_num]=other
    return face_l

def give_randomness():
    num=random.randint(0,11)
    if num%2==0:
        inverted=True
    else:
        inverted=False
    if num == 0 or num == 11:
        direction='right'
    elif num == 1 or num == 10:
        direction='left'
    elif num == 2 or num == 9:
        direction='top'
    elif num == 3 or num == 8:
        direction='bottom'
    elif num == 4 or num == 7:
        direction='front'
    elif num == 5 or num == 6:
        direction='back'
    return [direction,inverted]

def take_back_randomness():
    
    num=random.randint(0,11)
    if num%2==1:
        inverted=True
    else:
        inverted=False
    if num == 0 or num == 11:
        direction='right'
    elif num == 1 or num == 10:
        direction='left'
    elif num == 2 or num == 9:
        direction='top'
    elif num == 3 or num == 8:
        direction='bottom'
    elif num == 4 or num == 7:
        direction='front'
    elif num == 5 or num == 6:
        direction='back'
    return [direction,inverted]

def shuffle_cube(face_l,name):
    
    for i in range(1,30*len(name)):
        random.seed(i%12)
        randomness=give_randomness()
        face_l=change_face(face_l,randomness[0],randomness[1])  
    
        
def unshuffle_cube(face_l,name):

    for i in range(30*len(name)-1,0,-1):
        random.seed(i%12)
        randomness=take_back_randomness()
        face_l=change_face(face_l,randomness[0],randomness[1])

def s_to_bitlist(s):
    
     ords = (ord(c) for c in s)
     shifts = (7, 6, 5, 4, 3, 2, 1, 0)
     return [(o >> shift) & 1 for o in ords for shift in shifts]
 
def bitlist_to_chars(bl):
     bi = iter(bl)
     bytes = zip(*(bi,) * 8)
     shifts = (7, 6, 5, 4, 3, 2, 1, 0)
     for byte in bytes:
         yield chr(sum(bit << s for bit, s in zip(byte, shifts)))
    
def bitlist_to_s(bl):
     return ''.join(bitlist_to_chars(bl))
 
def read_back_cube(face_l):
    
    encoded_password=''
    
    for i in face_l:
        first_let=bitlist_to_s(i[0]+i[1])
        second_let=bitlist_to_s(i[2]+i[3])
        encoded_password+=first_let+second_let
    return encoded_password

def finding_encoding_l(possible_charecters):
    
    counter=0
    additional_counter=0
    encrypting=possible_charecters
    
    num_per_charecters=int(round(256/len(encrypting),0))
    additional_chars=256%len(encrypting)
    
    encoding_l=[]
    for i in encrypting:
        if additional_counter<additional_chars :
            encoding_l.append([i,counter,counter+num_per_charecters])
            counter+=num_per_charecters+1
            additional_counter+=1
        else:
            encoding_l.append([i,counter,counter+num_per_charecters-1])
            counter+=num_per_charecters
    
    return encoding_l

def get_encoding_pass(face_l,encoding_l):
    
    encoded_pass=''
    
    for i in face_l:
        l=i[0]+i[1]
        letter_1=l[0]*2**7+l[1]*2**6+l[2]*2**5+l[3]*2**4+l[4]*2**3+l[5]*2**2+\
l[6]*2+l[7]
        q=i[2]+i[3]
        letter_2=q[0]*2**7+q[1]*2**6+q[2]*2**5+q[3]*2**4+q[4]*2**3+q[5]*2**2+\
q[6]*2+q[7]
        for j in encoding_l:
            if ((letter_1<=j[-1])and(letter_1>=j[-2])):
                encoded_pass+=j[0]
            if ((letter_2<=j[-1])and(letter_2>=j[-2])):
                encoded_pass+=j[0]
    return encoded_pass

def letters_and_numbers(face_l):
    
    encrypting='0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ' 
    encoding_l=finding_encoding_l(encrypting)
    encoded_pass=get_encoding_pass(face_l,encoding_l)    
    return encoded_pass

def only_letters(face_l):
    
    '''This is a function that will encode the faces into only letters'''
    
    encrypting='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    encoding_l=finding_encoding_l(encrypting)
    encoded_pass=get_encoding_pass(face_l,encoding_l)  
    return encoded_pass

def numbers_and_specials(face_l):
    
    encrypting='!@#$%^&*()1234567890-_+=\\|]}[{\'"};:/?.>,<`~'
    encoding_l=finding_encoding_l(encrypting)
    encoded_pass=get_encoding_pass(face_l,encoding_l)  
    return encoded_pass

def numbers(face_l):
    
    encrypting='1234567890'
    encoding_l=finding_encoding_l(encrypting)
    encoded_pass=get_encoding_pass(face_l,encoding_l)  
    return encoded_pass

def specials(face_l):
    
    encrypting='!@#$%^&*()-_+=\\|]}[{\'"};:/?.>,<`~'
    encoding_l=finding_encoding_l(encrypting)
    encoded_pass=get_encoding_pass(face_l,encoding_l)  
    return encoded_pass

def letters_and_specials(face_l):
    
    encrypting='!@#$%^&*()-_+=\\|]}[{\'"};:/?.>,<`~abcdefghijklmnopqrstuvwxyzA\
BCDEFGHIJKLMNOPQRSTUVWXYZ'
    encoding_l=finding_encoding_l(encrypting)
    encoded_pass=get_encoding_pass(face_l,encoding_l)  
    return encoded_pass

def letters_numbers_and_specials(face_l):
    
    encrypting='abcdefghijklmnopqrstuvwxyz!@#$%^&*()1234567890-_+=\\|]}[{\'"};\
:/?.>,<`~ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    encoding_l=finding_encoding_l(encrypting)
    encoded_pass=get_encoding_pass(face_l,encoding_l)  
    return encoded_pass

def Start():
    m = App()
    m.show()
    return m

class App(QWidget):
 
    def __init__(self):
        super().__init__()
        self.title = 'PassMeWord'
        self.left = 0
        self.top = 50
        self.width = 840
        self.height = 280
        self.initUI()
 
    def initUI(self):
        
        '''Sets up the GUI'''
        
        previous_values = self.take_values_from_log()
        
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
 
        #Password length
        label=QLabel('Password Length:',self)
        label.move(20,25)
        
        label=QLabel('Original Password:',self)
        label.move(20,85)
        
        label=QLabel('Encrypting Text:',self)
        label.move(20,145)
        
        self.pass_len = QLineEdit(self,text=str(previous_values[0]))
        self.pass_len.move(200,20)
        self.pass_len.resize(280,40)
        
        # Create textbox
        self.password = QLineEdit(self,text=str(previous_values[0]))
        self.password.move(200, 80)
        self.password.resize(280,40)
        self.password.setToolTip('Unencrypted Password')
        
        
        self.encroding_string = QLineEdit(self)
        self.encroding_string.move(200, 140)
        self.encroding_string.resize(280,40)
        self.encroding_string.setToolTip('Encrypting Keyword')
 
        # Create a button in the window
        self.button = QPushButton('Encode', self)
        self.button.move(200,200)
        self.button.clicked.connect(self.on_click)
        
        #CheckBox
        self.b1 = QCheckBox("Letters",self)
        self.b1.move(540,20)
        self.b1.resize(320,40)
        
        self.b2 = QCheckBox("Numbers",self)
        self.b2.move(540,60)
        self.b2.resize(320,40)
        
        self.b3 = QCheckBox("Special Charecters",self)
        self.b3.move(540,100)
        self.b3.resize(320,40)

        # Create a quit buttom
        self.button = QPushButton('Quit',self)
        self.button.move(380,200)
        self.button.clicked.connect(self.exiting)
 
        # connect button to function on_click     
                
    def take_values_from_log(self):
        
        '''This function will take the values from the logfile and have it set
        as the value in the textbox when the program opens'''
        
        file=open('log.txt','r')
        
        for line in file:
            things=line
            stuff_l=things.split(' | ')
            pass_len=stuff_l[0]
            password=stuff_l[1]
        
        file.close()
        
        return [pass_len,password]

    def save_previous_settings(self):
        
        '''This function will take the values input after pressing encode (not 
        encoding passphrase) and save these values to a file for another
        function to take on startup so the user doesn't have to type everything
        over and over again'''
        
        file=open('log.txt','w')
        
        pass_length=str(self.pass_len.text())
        password=str(self.password.text())
        stuff=pass_length+' | '+password
        
        file.write(stuff)
        
        file.close()
 
    def password_length(self,encoding_password):
        
        '''This function will take the given password that needs to be encoded
and makes sure it's the correct length to have everything work'''
        
        if len(encoding_password)<=3:
            print('Encrypting Passwors Length must be more than 3 characters')
            sys.exit()

        if len(encoding_password)<=6 and len(encoding_password)>3:
            encoding_password=encoding_password[:]+encoding_password[:]+\
encoding_password[:]
        elif len(encoding_password)>6 and len(encoding_password)<12:
            encoding_password=encoding_password[:]+encoding_password[:]
        
        if len(encoding_password)>12:
            encoding_password=encoding_password[:12]
            
        return encoding_password
    
    def exiting(self):
        sys.exit()
        
    def on_click(self):
        
        '''This function activates when the user clicks the encode button and
        does the encoding and saves some values for the next startup'''
        
        self.save_previous_settings()

        state1=self.b1.isChecked()
        state2=self.b2.isChecked()
        state3=self.b3.isChecked()
        name = self.encroding_string.text()
        name=name.lower()
        if len(name)<3:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Charecter Length Warning")
            msg.setInformativeText("Unencrypted Password is not long enough")
            msg.setWindowTitle("Password Error")
            msg.setDetailedText("Unencrypted password must be atleast 3 \
charecters long")
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msg.show()
        n=4
        pass_text=self.password.text()
        pass_text=self.password_length(pass_text)
        face_l=threeD_cube(n,pass_text)
        shuffle_cube(face_l,name)
        encoded_password=''
        if state1 == True and state2==True and state3==True:
            while len(encoded_password)<int(self.pass_len.text()):
                encoded_password+=letters_numbers_and_specials(face_l)
            if len(encoded_password)>int(self.pass_len.text()):
                encoded_password=encoded_password[:int(self.pass_len.text())]
            pyperclip.copy(encoded_password)
        elif state1==True and state2==True and state3==False:
            encoded_password=letters_and_numbers(face_l)
            pyperclip.copy(encoded_password)
        elif state1==True and state2==False and state3==False:
            encoded_password=only_letters(face_l)
            pyperclip.copy(encoded_password)
        elif state1==False and state2==True and state3==True:
            encoded_password=numbers_and_specials(face_l)
            pyperclip.copy(encoded_password)
        elif state1==False and state2==False and state3==True:
            encoded_password=specials(face_l)
            pyperclip.copy(encoded_password)
        elif state1==True and state2==False and state3==True:
            encoded_password=letters_and_specials(face_l)
            pyperclip.copy(encoded_password)
        elif state1==False and state2==True and state3==False:
            encoded_password=numbers(face_l)
            pyperclip.copy(encoded_password)
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Functionality Warning")
            msg.setInformativeText("We do not offer that functionality yet")
            msg.setWindowTitle("Funcationality Error")
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msg.show()
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Start()
    app.exec_()
