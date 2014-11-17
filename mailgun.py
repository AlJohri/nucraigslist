import os, requests

def send_simple_message():
    return requests.post(
        "https://api.mailgun.net/v2/mg.nucraigslist.com/messages",
        auth = ("api", os.getenv('MAILGUN_KEY')),
        data = {
        	"from": "Al Johri <al@mg.nucraigslist.com>",
            "to": ["al.johri@gmail.com"],
			"subject": "Hello",
			"text": "Testing some Mailgun awesomness!"
		}
	)

print send_simple_message().content