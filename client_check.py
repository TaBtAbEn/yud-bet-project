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
        self.win = Gui_Layout(sg)
        self.Gui_Functions(self.win)
        #self.c.Recv_From_Server()


    #מחליט על הבקשה לשליחה לשרת
    #משתנה נוסף יתווסף ברגע השמת הגוי והוא יהיה הכפתור עליו המשתמש ילחץ
    def Gui_Functions(self, win):
        window1, window2, window3 = self.win.wellcome_win(), None, None

        while True:
            window, event, value = sg.read_all_windows()
            if window == window1 and event in (sg.WIN_CLOSED, 'Exit'):
                # סגירת חיבור לשרת
                self.c.Send_Command_To_Server(Close_Connection)
                break

            if window == window1:

                if event == '-NAME-':
                    if value["-NAME-"] == '':
                        window['-CHECK_NAME-'].update('User name not acceptable')
                    else:
                        window['-CHECK_NAME-'].update('User name acceptable')
                elif event == '-PASSWORD-':
                    if value["-PASSWORD-"] == '':
                        window['-CHECK_PASSWORD-'].update('Password not acceptable')
                    else:
                        window['-CHECK_PASSWORD-'].update('Password acceptable')
                elif event == 'Enter':
                    # הוספה בדיקה שכל הערכים ניתנים להרשמה
                    canEnter = True
                    userName = value["-NAME-"]
                    passWord = value["-PASSWORD-"]
                    if userName == '' or userName == '':
                        canEnter = False
                    print(userName)
                    print(passWord)
                    if canEnter:
                        # שליחה לשרת
                        self.c.Send_Sing_Up(Setup_User, userName, passWord)
                        window1.hide()
                        window2 = self.win.main_win()
                    elif event == sg.WIN_CLOSED or 'Exit':
                        # סגירת חיבור לשרת
                        self.c.Send_Command_To_Server(Close_Connection)
                        break

            if window == window2:
                if event == 'All Users Group Chat':
                    window2.hide()
                    print('check')
                    window3 = self.win.chat_win()

                elif event == sg.WIN_CLOSED or 'Exit':
                    window2.un_hide()
                    # סגירת חיבור לשרת
                    self.c.Send_Command_To_Server(Close_Connection)
                    break

            if window == window3:
                if event == 'SEND':
                    query = value['-QUERY-'].rstrip()
                    # send the message
                    # EXECUTE YOUR COMMAND HERE
                    print('The command you entered was {}'.format(query), flush=True)
                if event == 'GO BACK':
                    window3.close()
                    window2.un_hide()

        window.close()




class Gui_Layout:
    def __init__(self, sg):
        self.sg = sg
        #הוספת גדלים צבעים ופונטים אחידים

    def wellcome_win(self):
        sign_in = [[sg.Text('SIGN-IN', font='Any 20')],
                   [sg.Text(size=(25, 1), text='user name')], [sg.Input(key='-NAME-', enable_events=True)],
                   [sg.Text(size=(25, 1), text='password')], [sg.Input(key='-PASSWORD-', enable_events=True)],
                   [sg.Text(size=(25, 1), k='-CHECK_NAME-')],
                   [sg.Text(size=(25, 1), k='-CHECK_PASSWORD-')],
                   [sg.Button('Enter')]]

        log_in = [[sg.Text('LOG-IN', font='Any 20')],
                  [sg.T('This is some random text')],
                  [sg.T('This is some random text')],
                  [sg.T('This is some random text')],
                  [sg.T('This is some random text')]]

        layout = [[sg.Column(sign_in, size=(450, 250))], [sg.Column(log_in, size=(450, 320))]]

        return sg.Window('Wellcome page', layout, margins=(0, 0), finalize=True)

    def main_win(self):
        layout = [[sg.Text('YOUR CHATS')],
                  [sg.Button('All Users Group Chat')]]
        return sg.Window('Second Window', layout, finalize=True)

    def chat_win(self):
        # שם הקבוצה יהיה עצם שיועבר לפה
        # תהיה קבלה של המשתמש מהשרת של שם הקבוצה המשתתפים וההודעות
        layout = [[sg.Text('*Chat name*', size=(40, 1))],
                  [sg.Output(size=(110, 20), font=('Helvetica 10'))],
                  [sg.Multiline(size=(70, 5), enter_submits=False, key='-QUERY-', do_not_clear=False),
                   sg.Button('SEND', button_color=(sg.YELLOWS[0], sg.BLUES[0]), bind_return_key=True),
                   sg.Button('ok', button_color=(sg.YELLOWS[0], sg.BLUES[0])),
                   sg.Button('GO BACK', button_color=(sg.YELLOWS[0], sg.GREENS[0]))]]
        return sg.Window('Chat window', layout, finalize=True, default_button_element_size=(8, 2),
                         use_default_focus=False)


a = Client_Input(sg)
