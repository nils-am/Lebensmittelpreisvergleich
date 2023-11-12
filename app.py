from flask import Flask, redirect, render_template, request, session, url_for, abort, g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, and_
from datetime import timedelta
import logging 

logging.basicConfig(level=logging.DEBUG) 

app = Flask(__name__)

# Replace these lines with your environment variables
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://sql11660633:wrLMsI537Z@sql11.freemysqlhosting.net:3306/sql11660633"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = '$6q_cHiPltHl&R-wOkOb'
app.config["SESSION_COOKIE_SECURE"] = True

db = SQLAlchemy(app)
if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)

#DB for lebensmittel
class Produkt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    preis = db.Column(db.Numeric(scale=2), unique=False, nullable=False)
    lebensmittel = db.Column(db.String(120), unique=False, nullable=False)
    quali = db.Column(db.String(120), unique=False, nullable=False)
    laden= db.Column(db.String(120), unique=False, nullable=False)
    produktname = db.Column(db.String(120), unique=False, nullable=False)
    kategorie = db.Column(db.String(120), unique=False, nullable=False)
    zusatz = db.Column(db.Numeric(scale=2), unique=False, nullable=True)

    def __init__(self, preis, lebensmittel, quali, laden, produktname, kategorie, zusatz, id=None):
        self.id = id
        self.preis=preis
        self.lebensmittel=lebensmittel
        self.quali=quali
        self.laden=laden
        self.produktname=produktname
        self.kategorie=kategorie
        self.zusatz=zusatz

#DB for Categories
class Kategorie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)

    def __init__(self, name, id=None):
        self.id = id
        self.name=name

#DB for Anbieter
class Anbieter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)

    def __init__(self, name, id=None):
        self.id = id
        self.name=name

#Empty User Before Login
@app.before_request
def before_request():
    g.user = session.get("user")
    print(session)
    print(session.get("user"))
    print(g.user)


#Admin Page with Functionality to add lebensmittel
@app.route('/admin', methods=('GET', 'POST'))
def admin():
    if session:
        message = ""
        lebensmittel = db.session.execute(db.select(Produkt).group_by(Produkt.lebensmittel)).scalars()
        lebensmittel=list(lebensmittel)    
        products = db.session.execute(db.select(Produkt).order_by(Produkt.lebensmittel)).scalars()
        products=list(products)   
        categories = Produkt.query.group_by(Produkt.kategorie).distinct()
        categories = list(categories)
        cat = Kategorie.query.order_by(Kategorie.name).all()
        cat = list(cat)
        anbieter = Anbieter.query.order_by(Anbieter.name).all()
        anbieter=list(anbieter)
        return render_template('admin.html', lebensmittel=lebensmittel, message=message, categories=categories, products=products, user=session["user"], cat=cat, anbieter=anbieter)
    else:
        print(g.user)
        return redirect(url_for("home"))

#Login
@app.route("/login", methods=['POST', "GET"])
def login():
    if request.method == 'POST':
        session.pop('user', None)
        if request.form["password"] == "FR5jafr4swibo*akocr4" and request.form["username"] == "YaraNilsMatura23":
            session["user"] = request.form["username"]
            print(session)
            return redirect(url_for("admin"))
        else: 
            return render_template("login_page.html")
    else:
        return render_template("login_page.html")

#Add Grocery in Admin Panel
@app.route("/add_grocery", methods=["POST", "GET"])
def add_grocery():
    message = ""
    if  request.method == 'POST':
        print("a")
        preis = request.form["preis"]
        lebensmittel = request.form["lebensmittel"]
        quali= request.form["quali"]
        laden= request.form.get("anbieter")
        produktname = request.form["produktname"]
        kategorie = request.form.get("category")
        zusatz = request.form["zusatz"]
        message = ""
        if not preis:
            message = "Bitte geben Sie bei Preis eine Zahl ein."
        if not lebensmittel:
            message = "Bitte geben Sie bei der Lebensmittelbeschreibung einen Text ein."
        if not quali:
            message = "Bitte geben Sie bei der Qualitätsbeschreibung einen Text ein."
        if not laden:
            message = "Bitte geben Sie bei dem Namen des Ladens einen Text ein." 
        if not produktname:
            message = "Bitte geben Sie bei dem Produktnamen einen Text ein."
        if not kategorie:
            message = "Bitte geben Sie bei der Kategorie einen Text ein."
        if not zusatz:
            message = "Bitte geben Sie beim Zusatz einen Text ein."
        if not message:
            neuesl = Produkt(preis=preis, lebensmittel=lebensmittel, quali=quali, laden=laden, produktname=produktname, kategorie=kategorie, zusatz=zusatz)
            db.session.add(neuesl)
            db.session.commit()
            message = "Das neue Lebensmittel wurde hinzugefügt."

        lebensmittel = db.session.execute(db.select(Produkt).group_by(Produkt.lebensmittel)).scalars()
        lebensmittel=list(lebensmittel)    
        products = db.session.execute(db.select(Produkt).order_by(Produkt.lebensmittel)).scalars()
        products=list(products)   
        categories = Produkt.query.group_by(Produkt.kategorie).distinct()
        categories = list(categories)
        cat = Kategorie.query.order_by(Kategorie.name).all()
        cat = list(cat)
        anbieter = Anbieter.query.order_by(Anbieter.name).all()
        anbieter = list(anbieter)
        return render_template('admin.html', lebensmittel=lebensmittel, message=message, categories=categories, products=products, user=session["user"], cat=cat, anbieter=anbieter)

#Add Category in Admin Panel
@app.route("/add_category", methods=["GET", "POST"])
def add_category():
    if request.method == "POST":
        name = request.form["cat"]
        print(name)
        print("test")
        neuek = Kategorie(name=name)
        db.session.add(neuek)
        db.session.commit()

    lebensmittel = db.session.execute(db.select(Produkt).group_by(Produkt.lebensmittel)).scalars()
    lebensmittel=list(lebensmittel)    
    products = db.session.execute(db.select(Produkt).order_by(Produkt.lebensmittel)).scalars()
    products=list(products)   
    categories = Produkt.query.group_by(Produkt.kategorie).distinct()
    categories = list(categories)
    cat = Kategorie.query.order_by(Kategorie.name).all()
    cat = list(cat)
    return render_template("admin.html", lebensmittel=lebensmittel, products=products, categories=categories, cat=cat)
        
#Add Anbieter in Admin Panel
@app.route("/add_anbieter", methods=["GET", "POST"])
def add_anbieter():
    if request.method == "POST":
        name = request.form["anbieter"]
        print(name)
        neuerA = Anbieter(name=name)
        db.session.add(neuerA)
        db.session.commit()

    lebensmittel = db.session.execute(db.select(Produkt).group_by(Produkt.lebensmittel)).scalars()
    lebensmittel=list(lebensmittel)    
    products = db.session.execute(db.select(Produkt).order_by(Produkt.lebensmittel)).scalars()
    products=list(products)   
    categories = Produkt.query.group_by(Produkt.kategorie).distinct()
    categories = list(categories)
    cat = Kategorie.query.order_by(Kategorie.name).all()
    cat = list(cat)
    anbieter = Anbieter.query.order_by(Anbieter.name).all()
    anbieter = list(anbieter)
    return render_template("admin.html", lebensmittel=lebensmittel, products=products, categories=categories, cat=cat, anbieter=anbieter)

#Grocery Delete Function
@app.route('/grocery/delete/<int:id>')
def delete(id):
    grocery = Produkt.query.filter_by(id=id).first()
    if not grocery:
        abort(404)
    db.session.delete(grocery)
    db.session.commit()
    return redirect(url_for("admin"))

#Category Delete Function
@app.route('/category/delete/<int:id>')
def catdel(id):
    category = Kategorie.query.filter_by(id=id).first()
    if not category:
        abort(404)
    db.session.delete(category)
    db.session.commit()
    return redirect(url_for("admin"))

#Anbieter Delete Function
@app.route('/anbieter/delete/<int:id>')
def anbieter_delete(id):
    anbieter = Anbieter.query.filter_by(id=id).first()
    if not anbieter:
        abort(404)
    db.session.delete(anbieter)
    db.session.commit()
    return redirect(url_for("admin"))

#Grocery Update Page
@app.route('/grocery/update/<int:id>', methods=('GET', 'POST'))
def update(id):
    message = ""
    grocery = Produkt.query.filter_by(id=id).first()
    if not grocery:
        abort(404)
    if request.method == 'POST':
        grocery.preis=request.form["preis"]
        grocery.lebensmittel=request.form["lebensmittel"]
        grocery.quali=request.form["quali"]  
        grocery.laden=request.form["laden"]  
        grocery.produktname=request.form["produktname"]
        grocery.kategorie=request.form["kategorie"]
        grocery.zusatz=request.form["zusatz"]
        if not grocery.preis:
            message = "Bitte geben Sie bei Preis eine Zahl ein."
        if not grocery.lebensmittel:
            message = "Bitte geben Sie bei der Beschreibung einen Text ein."
        if not grocery.quali:
            message = "Bitte geben Sie bei der Beschreibung einen Text ein."   
        if not grocery.laden:
            message = "Bitte geben Sie bei der Beschreibung einen Text ein."   
        if not grocery.produktname:
            message = "Bitte geben Sie bei der Beschreibung einen Text ein."
        if not grocery.kategorie:
            message = "Bitte geben Sie bei der Beschreibung einen Text ein."
        if not grocery.zusatz:
            message = "Bitte geben Sie bei der Beschreibung einen Text ein.-"
        if not message:
            db.session.commit()
            return redirect(url_for("admin"))
    lebensmittel = db.session.execute(db.select(Produkt).group_by(Produkt.lebensmittel)).scalars()
    lebensmittel=list(lebensmittel)
    products = db.session.execute(db.select(Produkt).order_by(Produkt.lebensmittel)).scalars()
    products=list(products)   
    categories = Produkt.query.group_by(Produkt.kategorie).distinct()
    categories = list(categories)
    cat = Kategorie.query.order_by(Kategorie.name).first()
    cat = list(cat)
    return render_template('update.html', grocery=grocery, message=message, lebensmittel=lebensmittel, categories=categories, products=products, cat=cat)

#Home Page
@app.route("/")
def home():
    categories = Produkt.query.group_by(Produkt.kategorie).distinct()
    categories = list(categories)
    lebensmittel = Produkt.query.group_by(Produkt.lebensmittel).distinct()
    lebensmittel=list(lebensmittel)                                   
    cat = Kategorie.query.order_by(Kategorie.name).all()      
    cat = list(cat)                                                          
    return render_template("home.html", lebensmittel=lebensmittel, categories=categories, cat=cat)


#Product Page
@app.route("/product/<produktname>")
def product(produktname):
    cat = Kategorie.query.order_by(Kategorie.name).all()      
    cat = list(cat)  
    categories = Produkt.query.group_by(Produkt.kategorie).distinct()
    categories = list(categories)   
    products = db.session.query(Produkt).filter(Produkt.produktname == produktname).order_by(Produkt.preis).all()
    products = list(products)
    lebensmittel = db.session.execute(db.select(Produkt).group_by(Produkt.lebensmittel)).scalars()
    lebensmittel = list(lebensmittel)
    return render_template("product.html", products=products, lebensmittel=lebensmittel, cat=cat, categories=categories)

#Search Function
@app.route("/search", methods=["POST"])
def search():
    categories = Produkt.query.group_by(Produkt.kategorie).distinct()
    categories = list(categories)
    lebensmittel = db.session.execute(db.select(Produkt).group_by(Produkt.lebensmittel)).scalars()
    lebensmittel = list(lebensmittel)
    searched=request.form ['searched']
    searched= "%{}%".format(searched)

    subquery = (
        db.session.query(
            Produkt.produktname,
            func.min(Produkt.preis).label("min_preis")
        )
        .filter(Produkt.lebensmittel.like(searched))
        .group_by(Produkt.produktname)
        .subquery()
    )

    results_lebensmittel = (
        db.session.query(Produkt)
        .join(subquery, and_(Produkt.produktname == subquery.c.produktname, Produkt.preis == subquery.c.min_preis))
        .filter(Produkt.lebensmittel.like(searched))
    )
    subquery = (
        db.session.query(
            Produkt.produktname,
            func.min(Produkt.preis).label("min_preis")
        )
        .filter(Produkt.produktname.like(searched))
        .group_by(Produkt.produktname)
        .subquery()
    )

    results_produktname = (
        db.session.query(Produkt)
        .join(subquery, and_(Produkt.produktname == subquery.c.produktname, Produkt.preis == subquery.c.min_preis))
        .filter(Produkt.produktname.like(searched))
    )
    subquery = (
        db.session.query(
            Produkt.produktname,
            func.min(Produkt.preis).label("min_preis")
        )
        .filter(Produkt.kategorie.like(searched))
        .group_by(Produkt.produktname)
        .subquery()
    )

    results_kategorie = (
        db.session.query(Produkt)
        .join(subquery, and_(Produkt.produktname == subquery.c.produktname, Produkt.preis == subquery.c.min_preis))
        .filter(Produkt.kategorie.like(searched))
    )
    subquery = (
        db.session.query(
            Produkt.produktname,
            func.min(Produkt.preis).label("min_preis")
        )
        .filter(Produkt.laden.like(searched))
        .group_by(Produkt.produktname)
        .subquery()
    )

    results_anbieter = (
        db.session.query(Produkt)
        .join(subquery, and_(Produkt.produktname == subquery.c.produktname, Produkt.preis == subquery.c.min_preis))
        .filter(Produkt.laden.like(searched))
    )


    results= results_produktname.union(results_lebensmittel).union(results_kategorie).union(results_anbieter)
    message=""
    if results:
        results=results
    else:
        message = "Für Ihre Suche gab es keine Resultate. Überprüfen Sie Ihre Anfrage auf Schreibfehler oder nutzen Sie unsere Produktlise."
    searched = searched.replace('%', '').replace('{', '').replace('}', '')
    print(results)
    return render_template("product_results.html", searched=searched, results=results, message=message, lebensmittel=lebensmittel, categories=categories)


'''
@app.route("/abc")
def abc():
    subquery = (
        db.session.query(
            Produkt.produktname,
            func.min(Produkt.preis).label("min_preis")
        )
        .filter(Produkt.lebensmittel == "Bananen")
        .group_by(Produkt.produktname)
        .subquery()
    )

    results_lebensmittel = (
        db.session.query(Produkt)
        .join(subquery, and_(Produkt.produktname == subquery.c.produktname, Produkt.preis == subquery.c.min_preis))
        .filter(Produkt.lebensmittel == "Bananen")
    )
    subquery = (
        db.session.query(
            Produkt.produktname,
            func.min(Produkt.preis).label("min_preis")
        )
        .filter(Produkt.produktname == "Banane Fairtrade")
        .group_by(Produkt.produktname)
        .subquery()
    )

    results_produktname = (
        db.session.query(Produkt)
        .join(subquery, and_(Produkt.produktname == subquery.c.produktname, Produkt.preis == subquery.c.min_preis))
        .filter(Produkt.produktname == "Banane Fairtrade")
    )
    subquery = (
        db.session.query(
            Produkt.produktname,
            func.min(Produkt.preis).label("min_preis")
        )
        .filter(Produkt.kategorie == "Früchte & Gemüse")
        .group_by(Produkt.produktname)
        .subquery()
    )

    results_kategorie = (
        db.session.query(Produkt)
        .join(subquery, and_(Produkt.produktname == subquery.c.produktname, Produkt.preis == subquery.c.min_preis))
        .filter(Produkt.kategorie == "Früchte & Gemüse")
    )  
    return render_template("test.html", results_lebensmittel=results_lebensmittel, results_produktname=results_produktname, results_kategorie=results_kategorie)
'''

#Lebensmittel Seite
@app.route("/lebensmittel/<lebensmittelbezeichnung>")
def lebensmittel(lebensmittelbezeichnung):
    categories = Produkt.query.group_by(Produkt.kategorie).distinct()
    categories = list(categories)
    lebensmittel = db.session.execute(db.select(Produkt).group_by(Produkt.lebensmittel)).scalars()
    lebensmittel=list(lebensmittel)    
    subquery = (
        db.session.query(
            Produkt.produktname,
            func.min(Produkt.preis).label("min_preis")
        )
        .filter(Produkt.lebensmittel==lebensmittelbezeichnung)
        .group_by(Produkt.produktname)
        .subquery()
    )

    results = (
        db.session.query(Produkt)
        .join(subquery, and_(Produkt.produktname == subquery.c.produktname, Produkt.preis == subquery.c.min_preis))
        .filter(Produkt.lebensmittel==lebensmittelbezeichnung)
    )
    searched = lebensmittelbezeichnung
    return render_template("lebensmittel_results.html", results=results, searched=searched, categories=categories, lebensmittel=lebensmittel)

#Page for all Lebensmittel inside a Category
@app.route("/kategorie/<kategorie>")
def kategorie(kategorie):
    categories = Produkt.query.group_by(Produkt.kategorie).distinct()
    categories = list(categories)
    lebensmittel = db.session.execute(db.select(Produkt).group_by(Produkt.lebensmittel)).scalars()
    lebensmittel = list(lebensmittel)    
    results = db.session.query(Produkt.kategorie, Produkt.lebensmittel).filter(Produkt.kategorie == kategorie).distinct().all()
    results = list(results)
    searched = kategorie
    return render_template("category_results.html", results=results, searched=searched, categories=categories, lebensmittel=lebensmittel)

#Logout
@app.route("/dropsession")
def dropsession():
    session.pop("user", None)
    return redirect(url_for("home"))

#Grocery List Function
@app.route("/tempsearch")
def tempsearch():
    q = request.args.get("q")
    print(q)
    q= "%{}%".format(q)
    if q:
        res1 = db.session.query(Produkt).filter(Produkt.produktname.like(q)).group_by(Produkt.produktname)
        res2 = db.session.query(Produkt).filter(Produkt.lebensmittel.like(q)).group_by(Produkt.produktname)
        res = res1.union(res2).all()
    else:
        res = []
    return render_template("tempsearch.html", res=res)

#Grocery List Function
@app.route("/pop/<current_item>")
def pop(current_item):
    current_item=current_item
    print(current_item)
    return render_template("pop.html", current_item=current_item)