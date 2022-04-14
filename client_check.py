import socket
import PySimpleGUI as sg
#השמת שם ברגע התחברות ושליחת הודעות למשתמשים אחרים

MAX_MSG_LENGTH = 1024
PORT = 5555
IP = "127.0.0.1"

Setup_User = "1"
Close_Connection = "0"










class Server_Funcation:
    def __init__(self, IP, PORT):
        self.my_socket = socket.socket()
        self.my_socket.connect((IP, PORT))



    #מקבל הודעת תגובה מהשרת
    def Recv_From_Server(self):
        server_request = self.my_socket.recv(MAX_MSG_LENGTH).decode()
        print("|server sent to client: ", server_request, " |")


    #ומחזיר בקשה לשרת
    def Send_Command_To_Server(self, command):
        self.my_socket.send(command.encode())
        print("|client sent to server: ", command, " |")

    def Send_Sing_Up(self, command, name, password):
        massage = command + name + "©" + password
        self.my_socket.send(massage.encode())



class Client_Input:
    def __init__(self, sg):
        self.c = Server_Funcation(IP, PORT)
        self.win = Gui_Windows(sg)
        self.Choose_Command(self.win)
        #self.c.Recv_From_Server()


    #מחליט על הבקשה לשליחה לשרת
    #משתנה נוסף יתווסף ברגע השמת הגוי והוא יהיה הכפתור עליו המשתמש ילחץ
    def Choose_Command(self, win):
        window1, window2 = self.win.wellcome_win(), None  # start off with 1 window open

        while True:  # Event Loop
            window, event, values = sg.read_all_windows()
            if event == sg.WIN_CLOSED or event == 'Exit':
                window.close()
                if window == window2:  # if closing win 2, mark as closed
                    window2 = None
                elif window == window1:  # if closing win 1, exit program
                    self.c.Send_Command_To_Server(Close_Connection)
                    break
            elif event == 'Log in':
                sg.popup('NOT WORKING', 'all windows remain inactive while popup active')
            elif event == 'Sign in' and not window2:
                window2 = self.win.register_win()
            elif event == '-NAME-':
                if values["-NAME-"] == '':
                    window['-CHECK_NAME-'].update('User name not acceptable')
                else:
                    window['-CHECK_NAME-'].update('User name acceptable')
            elif event == '-PASSWORD-':
                if values["-PASSWORD-"] == '':
                    window['-CHECK_PASSWORD-'].update('Password not acceptable')
                else:
                    window['-CHECK_PASSWORD-'].update('Password acceptable')

            elif event == 'Enter':
                #הוספה בדיקה שכל הערכים ניתנים להרשמה
                canEnter = True
                userName = values["-NAME-"]
                passWord = values["-PASSWORD-"]
                if userName == '' or userName == '':
                    canEnter = False
                print(userName)
                print(passWord)
                if canEnter:
                    self.c.Send_Sing_Up(Setup_User, userName, passWord)
                    break

        window.close()



class Gui_Windows:
    def __init__(self, sg):
        self.sg = sg

    def wellcome_win(self):
        layout = [[sg.Text('This is the FIRST WINDOW'), sg.Text('      ', k='-OUTPUT-')],
                  [sg.Text('If you already have an account press [Log in]')],
                  [sg.Button('Sign in'), sg.Button('Log in'), sg.Button('Exit')]]
        return sg.Window('register', layout, location=(800, 600), finalize=True)

    def register_win(self):
        layout = [[sg.Text('Sign in')],
                  [sg.Text(size=(25, 1), text='user name')], [sg.Input(key='-NAME-', enable_events=True)],
                  [sg.Text(size=(25, 1), text='password')], [sg.Input(key='-PASSWORD-', enable_events=True)],
                  [sg.Text(size=(25, 1), k='-CHECK_NAME-')],
                  [sg.Text(size=(25, 1), k='-CHECK_PASSWORD-')],
                  [sg.Button('Enter'), sg.Button('Exit')]]
        return sg.Window('Second Window', layout, finalize=True)




a = Client_Input(sg)
