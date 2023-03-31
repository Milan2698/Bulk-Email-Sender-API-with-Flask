from flask import Flask, request, render_template, redirect, session
from flask_mail import Mail, Message
import pandas as pd
  
app = Flask(__name__)
app.secret_key = 'secret_key'
mail = Mail(app) # instantiate the mail class
  
# configuration of mail
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'Enter your mail id here'   ###############################
app.config['MAIL_PASSWORD'] = 'Enter your password here'   ###############################
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

@app.route('/', methods=["GET","POST"])
def upload():
    if request.method == "POST":
        subject = request.form['subject']
        message = request.form['message']
        start = request.form['from']
        end = request.form['to']
        file = request.files['file']
        df = pd.read_csv(file)
        email_list = df['email'].tolist()
        session['subject'] = subject
        session['message'] = message
        session['email_list'] = email_list
        session['start'] = start
        session['end'] = end
        return redirect('mail')
    return render_template('index.html')


@app.route("/mail")
def index():
   email_list = session.get('email_list', [])
   subject = session.get('subject', [])
   message = session.get('message', [])
   start = session.get('start', [])
   end = session.get('end', [])
   if len(email_list)>=int(end):
      for i in email_list[int(start)-1:int(end)]:
        msg = Message(
                        subject,
                        sender ='Enter your mail id here',   ###############################
                        recipients = [i]
                    )
        msg.body = message
        mail.send(msg)

   else:
      for i in email_list[int(start)-1:]:
        msg = Message(
                        subject,
                        sender ='Enter your mail id here',  ###############################
                        recipients = [i]
                    )
        msg.body = message
        mail.send(msg)

   return 'Sent'




if __name__ == '__main__':
   app.run(debug = True)