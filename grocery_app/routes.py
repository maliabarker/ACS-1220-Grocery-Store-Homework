from flask import Blueprint, request, render_template, redirect, url_for, flash
from datetime import date, datetime
from grocery_app.models import GroceryStore, GroceryItem, User
from grocery_app.forms import GroceryStoreForm, GroceryItemForm, SignUpForm, LoginForm
from grocery_app import bcrypt
from flask_login import login_user, logout_user, current_user, login_required
import flask_login

# Import app and db from events_app package so that we can run app
from grocery_app.extensions import app, db

main = Blueprint("main", __name__)
auth = Blueprint("auth", __name__)

##########################################
#              Main Routes               #
##########################################

@main.route('/')
def homepage():
    all_stores = GroceryStore.query.all()
    # print(all_stores)
    print(current_user)
    return render_template('home.html', all_stores=all_stores)

@main.route('/new_store', methods=['GET', 'POST'])
@login_required
def new_store():
    # TODO: Create a GroceryStoreForm
    form = GroceryStoreForm()
    if form.validate_on_submit():
        new_store = GroceryStore(
            title = form.title.data,
            address = form.address.data,
            created_by = current_user
        )
        db.session.add(new_store)
        db.session.commit()
        flash('New Store Created')
        return redirect(url_for('main.store_detail', store_id=new_store.id))

    # TODO: Send the form to the template and use it to render the form fields
    return render_template('new_store.html', form=form)

@main.route('/new_item', methods=['GET', 'POST'])
@login_required
def new_item():
    # TODO: Create a GroceryItemForm
    form = GroceryItemForm()
    if form.validate_on_submit():
        new_product = GroceryItem(
            name=form.name.data,
            price=form.price.data,
            category=form.category.data,
            photo_url=form.photo_url.data,
            store=form.store.data,
            created_by = current_user
        )
        print(new_product)
        db.session.add(new_product)
        db.session.commit()
        flash('New Product Added')
        return redirect(url_for('main.item_detail', item_id=new_product.id))

    # TODO: Send the form to the template and use it to render the form fields
    return render_template('new_item.html', form=form)

@main.route('/store/<store_id>', methods=['GET', 'POST'])
@login_required
def store_detail(store_id):
    store = GroceryStore.query.filter_by(id=store_id).one()
    form = GroceryStoreForm(obj=store)

    print(store.id)
    if form.validate_on_submit():
        store.title = form.title.data,
        store.address = form.address.data

        db.session.add(store)
        db.session.commit()

        flash('Store successfully updated')
        return redirect(url_for('main.store_detail', store_id=store.id))

    # TODO: Send the form to the template and use it to render the form fields
    store = GroceryStore.query.filter_by(id=store_id).one()
    return render_template('store_detail.html', store=store, form=form)

@main.route('/item/<item_id>', methods=['GET', 'POST'])
@login_required
def item_detail(item_id):
    item = GroceryItem.query.filter_by(id=item_id).one()
    form = GroceryItemForm(obj=item)

    if form.validate_on_submit():
        item.name = form.name.data
        item.price = form.price.data
        item.category = form.category.data
        item.photo_url = form.photo_url.data
        item.store = form.store.data

        db.session.add(item)
        db.session.commit()

        flash('Item successfully updated')
        return redirect(url_for('main.item_detail', item_id=item.id))
    # TODO: Send the form to the template and use it to render the form fields
    item = GroceryItem.query.filter_by(id=item_id).one()
    return render_template('item_detail.html', item=item, form=form)

@main.route('/add_to_shopping_list/<item_id>', methods=['GET', 'POST'])
@login_required
def add_to_shopping_list(item_id):
    item = GroceryItem.query.get(item_id)
    print(item)
    current_user.shopping_list_items.append(item)
    db.session.add(current_user)
    db.session.commit()
    flash(f'{item.name} added to your shopping list')
    return redirect(url_for('main.item_detail', item_id=item.id))

@main.route('/delete_from_shopping_list/<item_id>', methods=['GET', 'POST'])
@login_required
def delete_from_shopping_list(item_id):
    item = GroceryItem.query.get(item_id)
    print(item)
    current_user.shopping_list_items.remove(item)
    db.session.add(current_user)
    db.session.commit()
    flash(f'Deleted {item.name} from your shopping cart')
    return redirect(url_for('main.shopping_list', shopping_list=current_user.shopping_list_items))

@main.route('/shopping_list')
@login_required
def shopping_list():
    shopping_list = current_user.shopping_list_items
    return render_template('shopping_list.html', shopping_list=shopping_list)

##########################################
#              Auth Routes               #
##########################################

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    print('in signup')
    form = SignUpForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            username=form.username.data,
            password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        flash('Account Created.')
        print('created')
        return redirect(url_for('auth.login'))
    print(form.errors)
    return render_template('signup.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        login_user(user, remember=True)
        print(user)
        next_page = request.args.get('next')
        flash(f'Logged in successfully as {user.username}')
        return redirect(next_page if next_page else url_for('main.homepage'))
    return render_template('login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.homepage'))

