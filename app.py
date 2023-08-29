from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Đặt một mã bí mật cho ứng dụng của bạn
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Sử dụng SQLite, bạn có thể sử dụng cơ sở dữ liệu khác
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Tạo bảng User trong cơ sở dữ liệu
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Tên người dùng đã tồn tại', 'danger')
        else:
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash('Đăng ký thành công. Đăng nhập để tiếp tục', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Tên người dùng hoặc mật khẩu không đúng', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
@app.route('/share_link', methods=['POST'])
@login_required
def share_link():
    if request.method == 'POST':
        link = request.form['link']
        # Xử lý lưu trữ liên kết vào cơ sở dữ liệu hoặc nơi bạn muốn lưu trữ nó.
        # Ví dụ: bạn có thể lưu trữ liên kết trong một bảng riêng trong cơ sở dữ liệu.
        flash('Liên kết đã được chia sẻ', 'success')
    return redirect(url_for('interface'))
