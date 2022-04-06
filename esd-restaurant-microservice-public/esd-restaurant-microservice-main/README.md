# esd-restaurant-microservice

## 🧀 IS213 Enterprise Solution Development - Team 5 - Cheesecake 🍰 ##
### Team Members: ###
* Li Dai Li Felix - felixli.2020@scis.smu.edu.sg
* Quentin Quek Zhen Ming - quentinquek.2020@scis.smu.edu.sg
* Chia Yu-En Aloysius - yechia.2020@scis.smu.edu.sg
* Ho Zhi Ying - zhiying.ho.2020@scis.smu.edu.sg
* Davidson Rajasekar - davidsonr.2020@scis.smu.edu.sg

## 🍣 Project Overview 🍣 ##
A queue, order and menu management system developed for restaurants.

## 🔧 Installation Guide 🪛 ##
1. Configure yaml file database environment variable to SQL database of choice 
    * SQL import file included in config_files
2. Change microservice API keys as required
3. Run Kong API Gateway and import the snapshot file
    * Kong snapshot file included in config_files
4. Run `docker-compose up -d`
5. Host UI pages with WAMP or any other web server
    * A dockerfile to build a Apache web server can be found in config_files
    * By default, the enterprise solution is configured to use the host's port 8080 as it's web server
    * Map the host's port 8080 to the container's port 80
6. Browse to the web server and enjoy!

## !! Important Things to Note !! ##
1. Stripe API (payment.py): Include your own api key
2. Twilio API (notification.py): Include your own account SID and auth key 
3. Mailgun API (notification_email.py): Include your api key
4. Database (db_creds.py): Include your database details here. (E.g. hostname, username, password)