from market import app
from flask import render_template, redirect, url_for, flash, get_flashed_messages, request #request for purchased_item
from market.models import Item, User
from market.forms import RegisterForm, LoginForm, PurchaseItemForm, SellItemForm
from market import db
from flask_login import login_user, logout_user, login_required, current_user

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/market', methods=['GET', 'POST'])
@login_required    #Take out user,#Not loggin yet -> must loggin first, inheritance form UserMixin
def market_page():
    purchase_form = PurchaseItemForm()
    selling_form = SellItemForm()
    if request.method == "POST":
        #Purchase Item Logic
        purchase_item = request.form.get('purchased_item')
        p_item_object = Item.query.filter_by(name=purchase_item).first()
        if p_item_object:
            if current_user.can_purchase(p_item_object):
                p_item_object.buy(current_user)  #function buy: define in forms.py
                # p_item_object.owner = current_user.id
                # current_user.budget -= p_item_object.price
                # db.session.commit()
                flash(f"cng:Congratulation! You purchased {p_item_object.name} for {p_item_object.price}", category='success')
            else:
                flash(f"Unfortunately, you don't have enough money to purchase {p_item_object.name}", category='danger')
        #Sell Item Logic
        sold_item = request.form.get('sold_item')
        s_item_object = Item.query.filter_by(name=sold_item).first()
        if s_item_object:
            if current_user.can_sell(s_item_object):
                s_item_object.sell(current_user)
                flash(f"Congratulation! You sold {s_item_object.name} back to market! ", category='success')
            else:
                flash(f"Something went wrong with selling {s_item_object.name}", category='danger')

        return redirect(url_for('market_page'))

    if request.method == "GET": #reload (refresh) will be OK.
        #items = Item.query.filter_by(owner=None) #purchased item will disapear.
        items = Item.query.all()
        owned_items = Item.query.filter_by(owner=current_user.id) #c???p nh???t th??ng tin theo m???i t??i kho???n t??? db (N???u kh??ng lam b?????c n??y th??: n???u purchase ??? TK A nh??ng v??o TK B c??ng ??? tr???ng th??i ???? mua -> kh??ng nh??n th???y items n??o c???)
        return render_template('market.html', items=items, purchase_form=purchase_form, owned_items=owned_items, selling_form=selling_form)

    #b???i v?? m???i l???n ta refresh webpage th?? s??? c?? 1 pop up x??c nh???n hi???n ra -> ta refactor l???i.
    #if purchase_form.validate_on_submit():
        #print(purchase_form.__dict__)  #Tra k???t qu??? d???ng dictionary.
        #print(purchase_form['purchased_item']) #sau khi submit. result is : <input id="submit" name="submit" type="submit" value="Purchase Item!"> ==> copy this and paste to items_modals.html
        #print(request.form.get('purchased_item')) #request.form: input nhap o ben items_modals da duoc nhap vao form, ta chi can get() thi se lay dc thong tin cua item
    #items = Item.query.all()

            # items = [
            #     {'id': 1, 'name': 'Phone', 'barcode': '893212299897', 'price': 500},
            #     {'id': 2, 'name': 'Laptop', 'barcode': '123985473165', 'price': 900},
            #     {'id': 3, 'name': 'Keyboard', 'barcode': '231985128446', 'price': 150}
            # ] C??I N??Y M??NH L??U L??N SQL ALCHEMY DB R???I L??N TA D??NG STAMENT been tren NH??vvv. congnm

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    # Varidation for Register
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create) # these 2 lines mean that after registration is complete, immediately enter the login state, instead of having to log in.
        flash(f"Account created successfully! You are now logged in as {user_to_create.username}", category='success')
        return redirect(url_for('market_page'))              #If vadication true -> derect page to the market_page
    if form.errors != {}:                                    #If there are not errors from the validations
        for err_msg in form.errors.values():                 #danger: boottrap, red message
            flash(f'There was an error with creating a user: {err_msg}', category='danger')
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first() #tra ve number of user: exg: User21
        if attempted_user and attempted_user.check_password_correction(   #check_password_correction:we created
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username} ', category='success')
            return redirect(url_for('market_page'))
        else:
            flash('Username or password are not match! Please try again', category='danger')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()   #inherit from flask_login built-in function
    flash("You have been logged out!", category='info')
    return redirect(url_for("home_page"))

