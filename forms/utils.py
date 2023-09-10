from django.core.mail import BadHeaderError, send_mail


def send_email(subject, message, from_email, to_email):
    if subject and message and from_email:
        try:
            send_mail(subject, message, from_email, to_email)
        except BadHeaderError:
            return "Invalid header found."
        return "/contact/thanks/"
    else:
        return "Make sure all fields are entered and valid."


def send_activation_email(subject, message, from_email, to_email):
    pass


def send_activation_change_email(subject, message, from_email, to_email):
    pass


def send_reset_password_email(subject, message, from_email, to_email):
    pass


def send_forgotten_username_email(subject, message, from_email, to_email):
    pass