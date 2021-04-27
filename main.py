from bs4 import BeautifulSoup
import requests
from discord_webhooks import DiscordWebhooks
import datetime


def get_website(url):
	r = requests.get(url)
	return r.text

def updates():
	my_data = get_website("https://www.worldometers.info/coronavirus/")

	# creating soup instance for extracting data
	soup = BeautifulSoup(my_data, "html.parser")

	# creating an empty dictionary to store all the values
	msg = {}

	for data in soup.find_all("div", class_="maincounter-number")[0].find_all("span"):
		latest_cases = data.get_text()
		msg['Total Cases'] = latest_cases

	for data in soup.find_all("div", class_="maincounter-number")[1].find_all("span"):
		latest_deaths = data.get_text()
		msg['Total Deaths'] = latest_deaths

	for data in soup.find_all("div", class_="maincounter-number")[2].find_all("span"):
		recovered = data.get_text()
		msg['Total Recovered'] = recovered

	return msg

def custom_countries_updates(country_name):
	new_data = get_website("https://www.worldometers.info/coronavirus/#countries")
	soup = BeautifulSoup(new_data, "html.parser")

	# making this empty list for appending all the available countries on the website
	countries_available = []
	for data in soup.find_all("a", class_="mt_a"):
		all_countries = data.get_text()
		countries_available.append(all_countries)

	# getting our heading row
	thead = soup.find("thead").find("tr").find_all("th")

	# appendind all headings into a list
	heading_list = []
	for w in thead:
		heading_list.append(w.get_text())

	# empty list for append all the values of countries stats
	values_list = []
		
	if (country_name in countries_available):

		# finding the parent tag using the value
		a_string = soup.find(string=country_name)
		parent_string = a_string.find_parent("a")
		grand_parent_string = parent_string.find_parent("td")

		for item in grand_parent_string.find_parent("tr").find_all("td"):
			values_list.append(item.get_text())

	else:
		print("Country Not Found!")


	# converting our two lists into a dictionary using zip function
	res = dict(zip(heading_list, values_list))
	return res

def send_msg_discord(msg, cases, deaths, recovered):
	webhook_url = ""   # add your discord webhook url here

	WEBHOOK_URL = webhook_url
	webhook = DiscordWebhooks(WEBHOOK_URL)

	current_time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")

	webhook.set_footer(text=f"Last Updated: {current_time}")
	webhook.set_content(title="CoronaVirus Latest Update", description=msg)

	webhook.add_field(name="Cases", value=cases, inline=True)
	webhook.add_field(name="Deaths", value=deaths, inline=True)
	webhook.add_field(name="Recovered", value=recovered, inline=True)

	webhook.send()


if __name__ == '__main__':
	user_choice = int(input("Which data you want to see?\n1. World\t2. Custom Country\n"))

	if(user_choice==1):
		print("Searching....")
		world_data = updates()
		for item in world_data:
			print(f"{item}: {world_data[item]}\n")

	elif(user_choice==2):
		user_input = input("Enter the Country Name, whose data you want to see\n")
		print("Searching....")

		custom_data = custom_countries_updates(user_input)
		for item in custom_data:
			print(f"{item}: {custom_data[item]}\n")
	else:
		print("Your input is invalid!")
  
  
  # if you want to send updates to your Discord Server then, uncomment the following code and please make sure that you have entered your Discord Webhook Url in it's Function
  
	# dictm = updates()
	# getting values from the key of dictionary
	# c = dictm['Total Cases']
	# d = dictm['Total Deaths']
	# r = dictm['Total Recovered']
	# send_msg_discord("Check the list", c, d, r)
