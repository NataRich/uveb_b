from flask_mail import Message

from .. import mail


class SendMail:
    @staticmethod
    def auth(dct, code):
        msg = Message('email-auth-do-not-reply', recipients=[dct['email']])
        msg.html = f"""<b>Welcome, {dct['username']}!</b> <br/>
                       <p>Please confirm you email address by the following code:</p>
                        <br/>
                        <b>{code}</b>
                        <br/>
                       <p>We are happy to see you join in us! Enjoy!</p>
                    """
        mail.send(msg)

    @staticmethod
    def forget_password(dct, code):
        msg = Message('email-auth-do-not-reply', recipients=[dct['email']])
        msg.html = f"""<b>You are modifying your password</b> <br/>
                       <p>Please confirm you email address by the following code:</p>
                        <b>{code}</b>
                    """
        mail.send(msg)

    @staticmethod
    def notice_password_change(dct):
        msg = Message('email-auth-do-not-reply', recipients=[dct['email']])
        msg.html = f"""<b>Welcome, {dct['username']}!</b> <br/>
                           <p>You have successfully changed your password!</p>
                        """
        mail.send(msg)
