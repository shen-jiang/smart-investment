import pandas as pd
from flask import Flask, render_template, session, redirect, url_for, flash, request, escape
import flask
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)

def import_data(filename, risk_level):
    df = pd.read_excel('stock_data/'+ filename +'.xlsx', converters = {'Stock ID':str})
    df.columns = ['Stock_ID', 'Name', 'Area', 'Industry', 'PE_ratio', 'General_Capital', 'Risk_Level', 'Label']
    df = df[df.Risk_Level == risk_level]
    return list(df.T.to_dict().values())

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/currency', methods=['GET', 'POST'])
def currency():
    return render_template('currency.html')

@app.route('/risk_test', methods=['GET', 'POST'])
def risk_test():
    if request.method == 'POST':
        score = 0
        for i in range(12):
            temp = request.form['Q' + str(i+1)]
            if temp == "B":
                score += 1
            elif temp == "C":
                score += 2

        if score < 7:
            result = "Averse"
        elif score < 20:
            result = "Neutral"
        else:
            result = "Preference"

        session['risk_level'] = result
        session['result'] = 'risk ' + result
        print(result)
        return redirect(url_for('.stock_list', result = result))


    return render_template('risk_test.html')

@app.route('/stock_list', methods=['GET', 'POST'])
def stock_list():
    result = session['result']

    file_list = ['Beverage', 'Computer_APP', 'Gold', 'Logistics', 'Media_Marketing',
                 'Public_Transportation', 'Real_Estate', 'Securities', 'Semiconductor', 'Diversified_Finance']
    stock_data = []
    for industry in file_list:
        stock_data.append(import_data(industry, session['risk_level']))
        print(industry + " loaded")


    if request.method == 'POST':
        stock_id = request.form['stock']
        session['stock_id'] = stock_id
        print(stock_id)
        return redirect(url_for('.stock_predict', Stock_Name = stock_id))

    file_list.remove('Beverage')

    return render_template('stock_list.html', Beverages = stock_data[0], Computer_APP = stock_data[1],
                           Gold = stock_data[2], Logistics = stock_data[3], Media_Marketing = stock_data[4],
                           Public_Transportation = stock_data[5], Real_Estate = stock_data[6], Securities = stock_data[7],
                           Semiconductor = stock_data[8], Diversified_Finance = stock_data[9], industry_list = file_list)

@app.route('/stock_analysis', methods=['GET', 'POST'])
def stock_predict():
    stock_id = session['stock_id']
    return render_template('stock_analysis.html', Stock_ID = stock_id)

@app.route('/stock_enter', methods=['GET', 'POST'])
def stock_enter():
    return render_template('stock_enter.html')

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/about_us', methods=['GET', 'POST'])
def about_us():
    return render_template('about_us.html')

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=4501)
    # manager.run()
