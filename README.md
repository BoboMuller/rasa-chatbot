# rasa-chatbot
Chatbot built with Rasa


This little programm was something we had to do for a class.

You need to download or clone this repository first.
Afterwards you have to create a virtual environment.
Then you should upgrade pip to at least 21.3.1, because the old versions have a problem with downloading rasa.
In this virtual env you install rasa with: pip install rasa==3.0.4
Then you go into the directory you cloned/downloaded and type: rasa shell

In another directory you go into the same virtual environment, go to the downloaded/cloned folder and type: rasa run actions


Edit: 21.1.2022
The new versions of some dependancies cause trouble and I don't have time to find out what versions have to be used.
I will fix this after the exams mid February.

Relevant code is found in actions/actions.py (API calls and generation of custom answers)
The domain.yml is the file with answers without an API call (excluding custom ones generated with API help)
In data/stories.yml you will find some examples how a dialog can happen
In data/nlu.yml you can find training sentences to trigger some functions of the bot.
