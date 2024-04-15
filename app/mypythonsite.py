from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import requests
from math import fabs
from locale import format_string

app = Flask(__name__)

name = []
amount = []
value = []

def parse():
    url = "https://www.cbr.ru/currency_base/daily/"
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    currs = soup.findAll('tr')
    info = []
    for unit in currs:
        info.append(unit.text.replace('\n','|'))
    return info

@app.route('/')
@app.route('/index')
def index():
    info=parse()
    info.append('|643|RUB|1|рубль Российской Федерации|1|')
    global name
    global value
    for unit in info:
        info = unit.split('|')
        if any(ch.isdigit() for ch in info[3]):
            name.append('(' + info[1] + '|' + info[2] + ') ' +  info[4])
            value.append((float(info[5].replace(',','.'))/int(info[3])))
    return render_template("index.html", curr_name=name, curr_name2=name)


@app.route('/', methods=['post', 'get'])
def form():
    if request.method == 'POST':
        selected_curr_inp=None
        selected_curr_out=None
        inp_value = request.form.get('num_1')
        if inp_value == '':
            inp_value=0
        else:
            inp_value = float(inp_value)
        if inp_value<0:
            inp_value = fabs(inp_value)
        option1 = request.form.get('droplist1')
        option2 = request.form.get('droplist2')
        for obj in range(len(name)):
            if name[obj][1:4]==option1[1:4]:
                selected_curr_inp=obj
            if name[obj][1:4]==option2[1:4]:
                selected_curr_out=obj
        result = inp_value*value[selected_curr_inp]/value[selected_curr_out]
    return render_template('index.html', ans= str(inp_value)+' '+option1[5:8]+' = ' + format_string('%.2f', result, grouping=True) + ' '+option2[5:8], curr_name=name, curr_name2=name)


if __name__ == '__main__':
    app.run()