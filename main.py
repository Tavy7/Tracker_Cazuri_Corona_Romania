import requests
import datetime


def getData():
	url = "https://coronavirus-tracker-api.herokuapp.com/v2/locations/186"
	return requests.get(url).json()

def addEndKey(dateStr):
	endKey = "T00:00:00Z"
	return dateStr + endKey

def getTodayDate():
	return addEndKey(str(datetime.date.today()))

def getYesterdayDate(i):
	return addEndKey(str(datetime.date.today() - datetime.timedelta(days = i)))

def inputDateObject():
	print("Prima inregistrare este la data de: 22-01-2020.")

	zi = input("Ziua = ")

	if len(zi) == 1:
		aux = zi
		zi = '0' + aux

	luna = input("Luna = ")

	if len(luna) == 1:
		aux = luna
		luna = '0' + aux
	
	an = int(input("An = "))

	return datetime.datetime(int(an), int(luna), zi)

def getProcent(x, y):
	return float(x) / float(y)  * 100

def meniu(timelines):
	print("\n1 - Numar cazuri dupa data")
	print("2 - Numar morti dupa data")
	print("0 - Iesire")

	x = input()

	if int(x) != 0 and int(x) != 1 and int(x) != 2:
		print("Input gresit!")
		meniu(timelines)
		return

	if int(x) == 0:
		return

	date = addEndKey(str(inputDateObject()))

	if int(x) == 1:
		if date in timelines['confirmed']:
			print (timelines['confirmed'][date])
		else:
			print ("Nu exista inregistrari pentru data introdusa.")
		return

	if int(x) == 2:
		if date in timelines['deaths']:
			print (timelines['deaths'][date])
		else:
			print ("Nu exista inregistrari pentru data introdusa.")
		return

def getTodayStats(timelines):
	i = 2

	if getTodayDate() in timelines['confirmed']['timeline']:
		i = 1
	
	ieri = (getYesterdayDate(i))

	cazuri_ieri = timelines['confirmed']['timeline'][ieri]
	decese_ieri = timelines['deaths']['timeline'][ieri]

	cazuri_azi = timelines['confirmed']['latest'] - cazuri_ieri
	decese_azi = timelines['deaths']['latest'] - decese_ieri

	return (cazuri_azi, decese_azi)
	

def printData(data):

	location = data['location']

	print("Tara: " + location['country'])
	print("Populatie curenta: {}".format(location['country_population']))
	print("Procentaj bonlnavi: {}".format(getProcent(location['latest']['confirmed'], location['country_population'])))
	

	latest = location['latest']
	print("\nCazuri totale: {}".format(latest['confirmed']))
	print("Decese totale: {}".format(latest['deaths']))

	dateAzi = getTodayStats(location['timelines'])

	print("\nCazuri noi azi: {}".format(dateAzi[0]))
	print("Decese noi azi: {}".format(dateAzi[1]))


	print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
	print ("\nDate actualizate la: " + data['location']['last_updated'][:10])

	meniu(location['timelines'])



def main():
	data = getData()
	printData(data)

if __name__ == "__main__":
	main()
