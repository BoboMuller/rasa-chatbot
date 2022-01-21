# rasa-chatbot
Chatbot built with Rasa


This little programm was something we had to do for a class.

It is a chatbot for the train operator Deutsche Bahn. It can give you information about which train you have to take to go from point A to point B. You can also ask about the price and about the arrival time. It can do some smaller things as well like explaining what it can besides this. 


Example:  

User: Bring mich nach München

Bot: Um von Passau Hbf nach München Hbf zu kommen musst du um 18:26 zum Gleis Nummer 3 gehen.

User: Ich will von Nürnberg nach Deggendorf

Bot: Um von Nürnberg Hbf nach Deggendorf Hbf zu kommen musst du um 18:33 zum Gleis Nummer 9 gehen. Umstiege sind bei Plattling erforderlich.

.
.
.

You need to download or clone this repository first.

Afterwards you have to create a virtual environment.

Then you should upgrade pip to at least 21.3.1, because the old versions have a problem with downloading rasa.

In this virtual env you install rasa with: __pip install rasa==3.0.4__

Spacy is needed to process your sentences. Install it with __pip install spacy__.

Next you have to type this: __spacy download de_core_news_md__

Then you go into the directory you cloned/downloaded and type: rasa shell

In another cmd window you go into the same virtual environment and then to the downloaded/cloned folder and type: __rasa run actions__

Edit:
I noticed that some Sanic server packages are currently causing trouble here is a solution that helped me:

__pip install sanic==21.6.0__

__pip install Sanic-Cors==1.0.1__

__pip install sanic-jwt==1.6.0__

__pip install sanic-plugin-toolkit==1.2.0__

__pip install Sanic-Plugins-Framework==0.9.5__

__pip install sanic-routing==0.7.2__
