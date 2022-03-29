import PySimpleGUI as pg

pg.theme("DarkAmber")

layout = [
    [pg.Text("choose action")],
    [pg.Button("sign in")], [pg.Button("close connection")]
]
# Create the window
window = pg.Window("Demo", layout)

# Create an event loop
while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the OK button
    if event == "OK" or event == pg.WIN_CLOSED:
        break

window.close()