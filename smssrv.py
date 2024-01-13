import serial,time
from serial.tools import list_ports
from flask import Flask, request, render_template

comports = list_ports.comports()

for comport in comports:
    print(comport)

comport = input('input port number: ')
port = serial.Serial("COM"+comport, baudrate=9600, timeout=1)

def send_command(cmd, sleep=1):
    port.write(cmd.encode())
    time.sleep(sleep)
    ret = ""
    while 1:
        line = port.readline().decode()
        if len(line) == 0:
            break
        ret += line
    print(ret)
    return ret

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = request.form.get('ATCommand')
        result = ''
        lines = [l.strip() for l in data.strip().split('\r')]
        for i in range(len(lines[:-1])):
            result += send_command(lines[i]+'\r')
        result += send_command(lines[-1])
        result += send_command(chr(26))
        return result
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
