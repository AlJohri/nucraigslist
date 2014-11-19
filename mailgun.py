import os, requests
from premailer import transform

with open("email/email.html") as f:
    x = f.read().decode("utf-8")
    html = transform(x)

with open("email/inline-email.html", "w") as f:
    y = html.encode('utf-8')
    f.write(y)

def send_simple_message():
    return requests.post(
        "https://api.mailgun.net/v2/mg.nucraigslist.com/messages",
        auth = ("api", os.getenv('MAILGUN_KEY')),
        data = {
        	"from": "Al Johri <al@mg.nucraigslist.com>",
            "to": ["al.johri@gmail.com", "andrewbayer2016@u.northwestern.edu"],
			"subject": "Hello",
            "html": html,
			# "text": "Testing some Mailgun awesomness!"
		}
	)

# print send_simple_message().content