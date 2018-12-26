import datetime

def date_to_string(date):	
	difference = datetime.datetime.utcnow() - date
	if difference.days // 365 >= 1:
		if difference.days // 365 == 1:
			return "1 vuosi sitten"
		return str(difference.days // 365) + " vuotta sitten"
	if difference.days // 30 >= 1:
		if difference.days // 30 == 1:
			return "1 kuukausi sitten"
		return str(difference.days // 30) + " kuukautta sitten"
	if difference.days // 7 >= 1:
		if difference.days // 7 == 1:
			return "1 viikko sitten"
		return str(difference.days // 7) + " viikkoa sitten"
	if difference.days >= 1:
		if difference.days == 1:
			return "1 päivä sitten"
		return str(difference.days) + " päivää sitten"
	if difference.seconds // 3600 >= 1:
		if difference.seconds // 3600 == 1:
			return "1 tunti sitten"
		return str(difference.seconds // 3600) + " tuntia sitten"
	if difference.seconds // 60 >= 1:
		if difference.seconds // 60 == 1:
			return "1 minuutti sitten"
		return str(difference.seconds // 60) + " minuuttia sitten"
	if difference.seconds == 1:
		return "1 sekunti sitten"
	return str(difference.seconds) + " sekuntia sitten"

