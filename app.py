from flask import Flask, request, render_template, redirect, session
from flask_mail import Mail, Message
import pandas as pd
  
app = Flask(__name__)
app.secret_key = 'secret_key'
mail = Mail(app) # instantiate the mail class
  
# configuration of mail
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'firsetest3@gmail.com'
app.config['MAIL_PASSWORD'] = 'hpuaxngyipqqmlkt'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
  
# message object mapped to a particular URL ‘/’
@app.route("/mail")
def index():
   email_list = session.get('email_list', [])
   for i in email_list:
    msg = Message(
                    'Hello',
                    sender ='firsetest3@gmail.com',
                    recipients = [i]
                )
    msg.body = 'Hello, This is trail mail from BroaderAI'
    mail.send(msg)
   return 'Sent'


@app.route('/', methods=["GET","POST"])
def upload():
    if request.method == "POST":
        file = request.files['file']
        df = pd.read_csv(file)
        email_list = df['email'].tolist()
        print(email_list)
        session['email_list'] = email_list
        print(session['email_list'])
        return redirect('mail')
    return render_template('index.html')

if __name__ == '__main__':
   app.run(debug = True)