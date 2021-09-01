from flask import Flask, render_template, redirect, url_for, flash,abort,request


app=Flask(__name__)


@app.route('/',methods=["GET","POST"])
def start():
    return "working "




if __name__ == "__main__":
    app.run(debug=True)