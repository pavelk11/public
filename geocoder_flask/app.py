from flask import Flask, request, render_template
from decimal import Decimal
from yandex_geocoder import Client
import config as cfg
from wtforms import Form, FloatField, StringField

class InputForm(Form):
    Coordx = FloatField(
        label='Широта', default = 57.991387)
    Coordy = FloatField(
        label='Долгота', default = 56.203444)
    Address = StringField(
        label='Адрес', default = 'Россия, Пермь, шоссе Космонавтов, 111Ик2')
 
class Geo():
    client = Client(cfg.yapi)   
    def get_address(self, x ,y):
        res = self.client.address(Decimal(y), Decimal(x))
        return res
    def get_coord(self, addr):
        coord = self.client.coordinates(addr)
        return [float(coord[0]),float(coord[1])]

app = Flask(__name__)

@app.route('/geo', methods=['GET', 'POST'])
def geo():
    form = InputForm(request.form) 
    if request.method == 'POST':
        if request.form["action"] == "Получить координаты":
            if form.Address.data is not None:
                rs1 = Geo().get_coord(addr=form.Address.data)
                rs2 = None
        if request.form["action"] == "Получить адрес":
            if form.Coordx.data is not None and form.Coordy.data:         
                rs2 = Geo().get_address(form.Coordx.data, form.Coordy.data)   
                rs1 = None     
    elif request.method == 'GET':
        rs1 = [form.Coordy.data, form.Coordx.data]
        rs2 = form.Address.data
    rs = [rs2, rs1]  
    return render_template('geo.html', form=form, result = rs)
        
        

if __name__ == "__main__":
    app.run(
#        debug=True, host=cfg.host, port=cfg.port
        )
    