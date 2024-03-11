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
    rs1 = None
    rs2 = None
    form = InputForm(request.form)
    if request.method == 'POST':
        try:
            if form.Address.data is not None:
                rs1 = Geo().get_coord(addr=form.Address.data)
            if form.Coordx.data is not None and form.Coordy.data is not None:
                rs2 = Geo().get_address(form.Coordx.data, form.Coordy.data)
                print(form.Coordx.data, form.Coordy.data)             
        except:
            rs = "Ошибка"       
    rs = [rs2, rs1]
    print(rs)
    return render_template('geo.html', form=form, result=rs)

@app.route('/map')
def about():
    return render_template('map.html')

if __name__ == "__main__":
    app.run(
#        debug=True, host=cfg.host, port=cfg.port
        )
    