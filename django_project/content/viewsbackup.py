from django.shortcuts import render
from django.http import HttpResponse
from twilio.rest import TwilioRestClient
from django.views.decorators.csrf import csrf_exempt
from multiprocessing import Process
from content.models import Call
import time
import datetime

#  This is the actual prompt on the phone. First method I created, hence index.
def index(request):
	return HttpResponse("""
	<Response>
    		<Gather action="/processFB?number=""" + request.GET['number'] + """&amp;del=""" + request.GET['delay'] + """" method="GET" timeout="100" finishOnKey="*">
        		<Say>Please enter your number and then press star.</Say>
    		</Gather>
	</Response>
	""")

# This determines what string needs to be read out to user on the phone. 
# Also, this saves the information to the database.
def processFB(request):
	returner = ' '
	# This loop constructs the actual string to be read
	for x in range(1, int(request.GET['Digits']) + 1):
		if (x % 15 == 0):
			returner += 'Fizzbuzz, '
		elif (x % 5 == 0):
			returner += 'Buzz, '
		elif (x % 3 == 0):
			returner += 'Fizz, '
		else:
			returner += str(x) + ', '
	# Saves in the db
	sendTo = Call(phoneNumber=request.GET['number'], call_date=str(datetime.datetime.now())[0:19], num_delay=int(request.GET['del']), num_entered=int(request.GET['Digits']))
	sendTo.save() 
	
	# Using TwiML to actually read out to the user.
	return HttpResponse("""
        <Response>
                <Say voice="woman">""" + returner + """</Say>
        </Response>""")
	
# This is essentially my homepage. Called it phaseTwo because it was Phase 2
def phaseTwo(request):
	returner = """<!DOCTYPE html>
	<html>
	<body>
	<form action="/callOther/" method="post">
  		<input type="text" name="numberToCall" placeholder="ex. 12404985209">
  		<input type="number" name="delay" placeholder="Enter # of sec delay">
		<input type="submit" name="submitButton" value="Submit">
	</form>
	<br>
	<table>
		<tr>
			<th>Date and Time</td>
			<th>Phone Number</td>
			<th>Delay Time</td>
			<th>FizzBuzz # Entered</td>
			<th>Replay?</td>
		</tr>"""
	# for call in database of calls
	for x in range(0, len(Call.objects.all())):
		returner += """<tr>
					<td>"""+Call.objects.all()[x].call_date+"""
					<td>"""+Call.objects.all()[x].phoneNumber+"""
					<td>"""+str(Call.objects.all()[x].num_delay)+"""
					<td>"""+str(Call.objects.all()[x].num_entered)+"""
					<td><a href="/replayer?id=""" + str(Call.objects.all()[x].id)+""" ">Replay</a></td>
				<tr>"""

	returner += """</table>
		</body>
        	</html>"""

	return HttpResponse(returner)

def replayer(request):
	call = Call.objects.filter(id=int(request.GET['id']))[0]	

	# Should have just made a function that makes call
	# Get these credentials from http://twilio.com/user/account
        account_sid = "AC3e0484cf1bcbaeb73f7cea2232e6d5d8"
        auth_token = "045d16497a712cd9d7b91e6d25e1ee0e"
        client = TwilioRestClient(account_sid, auth_token)

        # Make the call
        call = client.calls.create(to="+" + call.phoneNumber,  # Any phone number
                from_="+15713932095", # Must be a valid Twilio number
                url="http://162.243.232.192/processFB?Digits=" + str(call.num_entered) + "&number=" + call.phoneNumber + "&del=0" , method="GET")
	return HttpResponse("""<!DOCTYPE html>
        <html>
        <body>Replaying call!</body></html>""")

# Put in csrf_exempt for the sake of this program. Ideally, I would add more security, but hopefully the entire world doesn't want to use this.
@csrf_exempt
def callOther(request):
	# Making sure that the number is valid (US)
	if (len(request.POST['numberToCall']) == 11):

		# Starts the thread that makes it so the delay happens		
		p = Process(target=runner, args=(request.POST['delay'], request.POST['numberToCall'], ))
		p.start()
		# Return the wait page.
		return HttpResponse("""<!DOCTYPE html>
        		<html>
        		<body>
        		Calling """ + request.POST['numberToCall'] + """ in """ + request.POST['delay'] + """ seconds.
        		</body>
	 		</html>""")
	# Incase the user inputs an invalid number
	else:
		return HttpResponse("""<!DOCTYPE html>
                        <html>
                        <body>
			Invalid number provided. Must be 11 digits (1 + number).
                        </body>
                        </html>""")

# Thread studd (actually waiting and making the call)
def runner(delayTime, numberToCall):
	# STOP.
	time.sleep(int(delayTime))
	# Get these credentials from http://twilio.com/user/account
       	account_sid = "AC3e0484cf1bcbaeb73f7cea2232e6d5d8"
        auth_token = "045d16497a712cd9d7b91e6d25e1ee0e"
        client = TwilioRestClient(account_sid, auth_token)

        # Make the call
	# Make the call
        call = client.calls.create(to="+" + numberToCall,  # Any phone number
                from_="+15713932095", # Must be a valid Twilio number
                url="http://162.243.232.192/content?number=" + numberToCall + "&delay=" + delayTime, method="GET")
