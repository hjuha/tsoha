import datetime

def date_to_string(date):
	timezone = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo

	date += timezone.utcoffset(date)
	today = datetime.datetime.now()

	hour = str(date.hour)
	minute = str(date.minute)

	if len(hour) == 1:
		hour = "0" + hour
	if len(minute) == 1:
		minute = "0" + minute

	if date.date() == today.date():
		return "Tänään " + hour + ":" + minute
	elif (date + datetime.timedelta(1)).date() == today.date():
		return "Eilen " + hour + ":" + minute
	else:
		return str(date.day) + "." + str(date.month) + "." + str(date.year)
		