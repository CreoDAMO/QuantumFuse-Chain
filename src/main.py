from flask import Flask, render_template

app = Flask(__name__, template_folder='templates')

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/wallet')
def wallet():
    return render_template('wallet.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
