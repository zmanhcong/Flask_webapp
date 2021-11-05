from market import db, login_manager #installed in __init__.py
from market import bcrypt #installed in __init__.py
from flask_login import UserMixin #use for login: it contain: is_authenticated(login_required use in routes.py), is_active,is_anonymous, get_id()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)) #The function you set should take a user ID (a unicode) and return a user object, or None if the user does not exist.
                                        #You will need to provide a user_loader callback. This callback is used to reload the user object from the user ID stored in the session. It should take the unicode ID of a user, and return the corresponding user object.

class User(db.Model, UserMixin):  #db.Model:inhert from Model,It’s stored on the SQLAlchemy instance you have to create
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=1000)
    items = db.relationship('Item', backref='owned_user', lazy=True) #backref: back refferent: tu dong tim primary_key
    @property #this a a property of property() function: it contain: getter, setter, delet, init
    def prettier_budget(self):
        if len(str(self.budget)) >= 4:
            return f'{str(self.budget)[:-3]},{str(self.budget)[-3:]}$' #1000 -> [1] + [,000]
        else:
            return f"{self.budget}$"


    @property #getter
    def password(self):
        return self.password

    @password.setter  #getter: set value for property, use for user authen, we encrypt password
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password) #return True or False.... bcrypt.check_password_hash:built-in function

    def can_purchase(self, item_obj):
        return self.budget >= item_obj.price   #Only can purchase if budget >= price

    def can_sell(self, item_obj):
        return item_obj in self.items  #Chung minh la minh so huu, nen minh co the ban

class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30),nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    barcode = db.Column(db.String(length=12),nullable=False, unique=True)
    description = db.Column(db.String(length=1024), nullable=False, unique=True)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))  #foreignKey: tim primary key
                                                               #limit length of string, nullable=False:this is constraint, it mean NOT NULL in that column, unique=True  indicates that the Index should be created with the unique flag.(name not duplicate)


    def __repr__(self):
        return f'Item {self.name}'                              #data duoc nhap tu commmand vao database -> khi ta them chuc nang này thì nó sẽ hiện tên chứ không hiện ra item.

    def buy(self, user):
        self.owner = user.id
        user.budget -= self.price
        db.session.commit()
        # p_item_object.owner = current_user.id (p_item_object -> self...... p_item_object -> user)
        # current_user.budget -= p_item_object.price
        # db.session.commit()

    def sell(self, user):
        self.owner = None  #nguoc lai voi bye
        user.budget += self.price
        db.session.commit()