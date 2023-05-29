from flask import Flask,render_template
app = Flask(__name__)
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/registro',methods=["GET", "POST"])
def registro():
    return render_template("registro.html")

if __name__ == "__main__":
    app.run(debug=True)


 