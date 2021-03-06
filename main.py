import requests
import datetime
import matplotlib.pyplot as plt


def getData():
	url = "https://coronavirus-tracker-api.herokuapp.com/v2/locations/186"
	return requests.get(url).json()

def addEndKey(dateStr):
	endKey = "T00:00:00Z"
	return dateStr + endKey

def getTodayDate():
	return addEndKey(str(datetime.date.today()))

def getDateIDaysAgo(i):
	return addEndKey(str(datetime.date.today() - datetime.timedelta(days = i)))

def getDate1DayBefore(date):
	return addEndKey(str(date - datetime.timedelta(days = 1))[:10]) 

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
	return datetime.datetime(int(an), int(luna), int(zi))

def getProcent(x, y):
	return float(x) / float(y)  * 100

def cazuriNoiZilnice(cazuri):
	cazuriMax = 0

	print("Data\t\tNumar cazuri\tNumar cazuri noi")
	aux = 0
	for i, j in zip(cazuri, cazuri.values()):
		if j == 0:
			continue

		print(i[:10], "\t", j, "\t\t", j - aux)

		if j - aux > cazuriMax:
			cazuriMax = j - aux
			dataCazuriMax = i[:10]

		aux = j

	print("\n\nApogeul de cazuri noi a fost la data {}, cu {} cazuri.".format(dataCazuriMax, cazuriMax))

def afisareGraficCazuriNoi(cazuri):
	label, height = [], []

	aux = 0
	luna = "none"
	for i, j in zip(cazuri, cazuri.values()):
		if j == 0:
			continue
		height.append(int(j - aux))
		aux = j

		if str(i)[6] != luna:
			luna = str(i)[6]
			label.append(luna)
			continue

		label.append(str(i)[8:10])

	plt.bar(range(1, len(height) + 1), height,
	 tick_label = label, width = 0.7, color = 'black')


	plt.xlabel('Date') 
	plt.ylabel("Numar cazuri")
	plt.title("Cazuri noi zilnice")

	plt.show()

def afisareGrafiCazuri(cazuri):
	label, height = [], []
	luna = "none"
	
	for i, j in zip(cazuri, cazuri.values()):
		if j == 0:
			continue
		height.append(int(j))

		if str(i)[6] != luna:
			luna = str(i)[6]
			label.append(luna)
			continue

		label.append(str(i)[8:10])

	plt.bar(range(1, len(height) + 1), height,
	 tick_label = label, width = 0.7, color = 'black')


	plt.xlabel('Date') 
	plt.ylabel("Numar cazuri")
	plt.title("Cazuri noi zilnice")

	plt.show()

def meniu(timelines):
	print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
	print("\n 1 - Numar cazuri dupa data")
	print(" 2 - Numar morti dupa data")
	print(" 3 - Numar cazuri noi zilnice")
	print(" 4 - Grafic cazuri noi zilnice")
	print(" 5 - Grafic cazuri totale")
	print(" 0 - Iesire")

	x = input()

	if x not in ['1', '2', '3', '4', '5', '0']:
		print("Input gresit!")
		meniu(timelines)
		return

	if x == '0':
		return

	if x == '3':
		cazuriNoiZilnice(timelines['confirmed']['timeline'])
		meniu(timelines)
		return

	if x == '4':
		afisareGraficCazuriNoi(timelines['confirmed']['timeline'])
		meniu(timelines)
		return

	if x == '5':
		afisareGrafiCazuri(timelines['confirmed']['timeline'])
		meniu(timelines)
		return


	dataAzi = inputDateObject()
	dataIeri = getDate1DayBefore(dataAzi)

	dataAzi = addEndKey(str(dataAzi)[:10])

	print(dataAzi)
	print(dataIeri)

	if x == '1':
		confirmed = timelines['confirmed']['timeline']
		if dataAzi in confirmed:
			print ("La data selectata au fost {} cazuri.\nDin care {} noi.".format(
				confirmed[dataAzi], confirmed[dataAzi] - confirmed[dataIeri]))
		else:	
			print ("Nu exista inregistrari pentru data introdusa.")
		return

	if x == '2':
		decese = timelines['deaths']['timeline']
		if dataAzi in decese:
			print ("La data selectata au fost {} decese.\nDin care {} noi.".format(
				decese[dataAzi], decese[dataAzi] - decese[dataIeri]))
		else:
			print ("Nu exista inregistrari pentru data introdusa.")
		return

def getTodayStats(timelines):
	i = 2

	if getTodayDate() in timelines['confirmed']['timeline']:
		i = 1
	
	ieri = (getDateIDaysAgo(i))

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


	print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
	print ("\nDate actualizate la: " + data['location']['last_updated'][:10])

	meniu(location['timelines'])



def main():
	printData(getData())

if __name__ == "__main__":
	main()
