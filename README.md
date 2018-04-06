# PhishRod

![main_page](https://user-images.githubusercontent.com/36813986/117393890-fcb27200-aeec-11eb-9d7a-d6359da34a78.png)

The goal of this project is to provide minimalistic django project template that everyone can use, which _just works_ out of the box and has the basic setup you can expand on. 

Template is written with django 1.11 and python 3 in mind.

### Features

* Single web application

* Allows the user to:
    * Identify phishing attacks
    
    * Give their feedback by writing reviews
    
    * Visualize statistics about phish attacks tested with PhishRod
    
* A contact form that gets sent to the Admin email

* An Admin space to:
    * Review the usage of the application
    
    * Visualize users’ reviews


# Getting Started

### Requirements

* Python (3.6 +)
* Django (2.4 +)

We **highly recommend** to use these exact versions of Python and Django because this project is not tested with the 
other releases.

### Installation

For this step, we recommend setting up a virtual environment and activating it, this is optional:
 [Python 3 Virtual Environment Tutorial](https://docs.python.org/3/tutorial/venv.html)

Install project dependencies:

    pip install -r requirements.txt

    
Then simply apply the migrations:

    $ python manage.py migrate
    

You can now run the development server:

    $ python manage.py runserver
    
# Configuration: Classification model
This section is optional if you are just looking to use the application since it is already set up,
 but if you want to tweak on the classification model used in the app the fellow these steps.
 
### feature extraction


### Training the model



# Usage

PhishRod should now be accessible at http://127.0.0.1:8000/

![page_scroll](https://user-images.githubusercontent.com/36813986/117393896-ffad6280-aeec-11eb-9b7b-086e1b150392.png)


### Identifying a phishing website

Phish detected:
![phish_not_detected](https://user-images.githubusercontent.com/36813986/117427822-5337a480-af1d-11eb-9bb4-ca08a50d1efe.png)

Phish not detected:
![phish_detected](https://user-images.githubusercontent.com/36813986/117427799-4e72f080-af1d-11eb-9112-4cb488b11f53.png)


### Administration

![admin_login](https://user-images.githubusercontent.com/36813986/117428152-b45f7800-af1d-11eb-89d8-d4620f2a406c.png)

![admin_main_menu](https://user-images.githubusercontent.com/36813986/117393885-fa501800-aeec-11eb-91fc-08702e81fe29.png)

![admin_reviews](https://user-images.githubusercontent.com/36813986/117393886-fb814500-aeec-11eb-8d62-a52cc2f95080.png)

![admin_url](https://user-images.githubusercontent.com/36813986/117393888-fc19db80-aeec-11eb-959c-ae3e0b997c36.png)
