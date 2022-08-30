# What this app is capable of ?
1. Take the URL of the item being searched, go to the respective page, extract the name of the item, price and store them in a csv.
2. Next time the item is being searched, if different price and email are given for the same item, they are updated.
3. The app keeps parsing the price every 1min and updates in the csv. Thus a graph of the price vs time graph can be drawn. 
4. As soon as the price goes as low or lower than that given by user, an email is triggered to the user's id.

# Setting up locally

1. Clone the repository ```git clone https://github.com/abhilashdzr/Best-Price-Bot.git```
2. Delete all entries, except headers in Database.csv (if any) and any other csv files (if present)
3. Install the requirements ```pip install -r requirements.txt```
4. Export Flask app as ```export FLASK_APP=main.py```
5. Run the app ```flask run```
6. Put your favorite item link in the bar, your bid on the price, email id and wait. Although locally, you have to keep the app running ;)
