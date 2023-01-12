from flask import Flask, render_template, request
import requests
import smtplib
import passwords
blog_data_url = "https://api.npoint.io/78338809c13dc4e9a158"

my_email = passwords.my_email
to_email = passwords.to_email
my_pass = passwords.my_pass



app = Flask(__name__)
response = requests.get(url=blog_data_url)
response.raise_for_status()
blog_data = response.json()

@app.route("/")
def home_page():
    return render_template("index.html", data=blog_data)

@app.route("/about")
def about_page():
    return render_template("about.html")

@app.route("/post/<int:id>")
def get_blog_post(id):
    current_blog = blog_data[id-1]
    return render_template('post.html', post_data=current_blog)

@app.route("/contact", methods=['POST', "GET"])
def contact_page():
    if request.method == 'GET':
        return render_template("contact.html", msg_sent=False)
    elif request.method == 'POST':
        name = request.form['input_name']
        email = request.form['input_email']
        phone = request.form['input_phone']
        message = request.form['input_message']
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=my_email, password=my_pass)
            connection.sendmail(
                from_addr=my_email,
                to_addrs=to_email,
                msg=f"Subject: New Message - {name}\n\n{name}\n{email}\n{phone}\n{message}"
            )
        return render_template("contact.html", msg_sent=True)

if __name__ == "__main__":
    app.run(host="localhost", port=5001, debug=True)
