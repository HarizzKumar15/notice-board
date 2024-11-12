from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notices.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Notice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<Notice {self.title}>"

@app.route('/')
def index():
    notices = Notice.query.order_by(Notice.id.desc()).all()
    return render_template('index.html', notices=notices)

@app.route('/add', methods=['GET', 'POST'])
def add_notice():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        notice_count = Notice.query.count()
        if notice_count >= 6:
            oldest_notice = Notice.query.order_by(Notice.id.asc()).first()
            db.session.delete(oldest_notice)
            db.session.commit()

        new_notice = Notice(title=title, content=content)

        db.session.add(new_notice)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('add_notice.html')

@app.route('/delete/<int:id>', methods=['POST'])
def delete_notice(id):
    notice_to_delete = Notice.query.get_or_404(id)
    db.session.delete(notice_to_delete)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  
    app.run(debug=True, port=8080)

