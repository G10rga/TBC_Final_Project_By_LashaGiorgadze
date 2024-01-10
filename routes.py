from os import path

from flask import render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user

from extensions import app, db, bcrypt
from forms import RegistrationForm, LoginForm, AddProductForm, EditItemForm
from models import User, Item


@app.route("/add_product", methods=['GET', 'POST'])
def add_product():
    Item.query.all()

    form = AddProductForm()
    if form.validate_on_submit():
        file = form.img.data
        filename = file.filename
        file.save((path.join(app.root_path, 'static', filename)))

        new_product = Item(
            category=form.category.data,
            name=form.name.data,
            price=form.price.data,
            img=form.img.data.filename  # Assuming you want to store the filename
        )

        db.session.add(new_product)
        db.session.commit()

        flash("Product Added")
        return redirect("/")
    print(form.errors)

    return render_template("add_product.html", form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('Username is already taken. Please choose a different one.', 'danger')
        else:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            new_user = User(username=form.username.data, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully! You can now log in.', 'success')
            return redirect(
                url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Login failed. Check your username and password.', 'danger')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/')
def index():
    items = Item.query.all()

    return render_template('index.html', items=items)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/store')
def store():
    items = Item.query.all()

    return render_template('store.html', items=items)  # Pass the items to the template


@app.route('/configurator')
def configurator():
    items = Item.query.all()

    return render_template('configurator.html', items=items)


@app.route('/item/<int:item_id>')
def item_details(item_id):
    item = Item.query.get_or_404(item_id)
    return render_template('item_details.html', item=item)


@app.route('/admin/dashboard')
@login_required
def dashboard():
    if current_user.role == 'Admin':
        # Allow access to the admin dashboard
        items = Item.query.all()
        return render_template('admin_dashboard.html', items=items)
    else:
        # Handle non-admin access, perhaps redirect to a different page
        return render_template('non_admin_access.html')


@app.route('/admin/delete_item/<int:item_id>')
@login_required
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash('Item deleted successfully!', 'success')
    return redirect(url_for('dashboard'))


@app.route('/admin/edit_item/<int:item_id>', methods=['GET', 'POST'])
@login_required
def edit_item(item_id):
    item = Item.query.get_or_404(item_id)
    form = EditItemForm(obj=item)

    if form.validate_on_submit():
        item.category = form.category.data
        item.name = form.name.data
        item.price = form.price.data
        db.session.commit()
        flash('Item updated successfully!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('edit_item.html', form=form)


