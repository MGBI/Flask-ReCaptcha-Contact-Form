"""
Contact form : Implementing ReCaptcha with Flask.

Read how it works at : http://techmonger.github.io/5/python-flask-recaptcha/
"""

import os
from flask import Flask, request, redirect, render_template, url_for, flash
import json
import requests

app = Flask(__name__)

# Secret for message flashing

app.secret_key = 'change-this'


def get_env_setting(setting, default=None, obligatory=True):
    """Get the environment setting or return an exception"""
    var = os.getenv(setting, default)
    if not var and obligatory:
        raise RuntimeError('Set the {} env variable'.format(setting))
    return var


# reCAPTCHA keys
sitekey = get_env_setting("RECAPTCHA_SITE_KEY")
secret = get_env_setting("RECAPTCHA_SECRET_KEY")


@app.route("/", methods=["GET", "POST"])
def home():
    """ Redirecting from home to contact form """
    return redirect(url_for("contact"))


@app.route("/contact/", methods=["GET", "POST"])
def contact():
    """ Renders contact form on get and processes it on post. """

    if request.method == "POST":
        request.form['name']
        request.form['email']
        request.form['message']
        captcha_response = request.form['captcha-response']

        if is_human(captcha_response):
            # Process request here
            status = "Details submitted successfully."
        else:
            # Log invalid attempts
            status = "Sorry! Bots are not allowed."

        flash(status)
        return redirect(url_for('contact'))

    return render_template("contact.html", sitekey=sitekey)


def is_human(captcha_response):
    """ Validating recaptcha response from google server.
        Returns True captcha test passed for the submitted form
        else returns False.
    """
    payload = {'response': captcha_response, 'secret': secret}
    response = requests.post(
        "https://www.google.com/recaptcha/api/siteverify", payload)
    response_text = json.loads(response.text)
    flash(response_text)
    return response_text['success']


if __name__ == '__main__':
    app.run(host='0.0.0.0')
