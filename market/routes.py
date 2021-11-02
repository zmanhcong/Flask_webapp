from market import app
from flask import  render_template
from market.models import Item

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/market')
def market_page():
    items = Item.query.all()
    return render_template('market.html', items=items)
            # items = [
            #     {'id': 1, 'name': 'Phone', 'barcode': '893212299897', 'price': 500},
            #     {'id': 2, 'name': 'Laptop', 'barcode': '123985473165', 'price': 900},
            #     {'id': 3, 'name': 'Keyboard', 'barcode': '231985128446', 'price': 150}
            # ] CÁI NÀY MÌNH LƯU LÊN SQL ALCHEMY DB RỒI LÊN TA DÙNG STAMENT been tren NHÉ. congnm

