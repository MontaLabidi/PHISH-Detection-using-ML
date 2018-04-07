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

    $ pip install -r requirements.txt

    
Then simply apply the migrations:

    $ python manage.py migrate
    

You can now run the development server:

    $ python manage.py runserver
    
# Classification model Setup
This section is optional if you are just looking to use the application since it is already set up with a model,
 but if you want to tweak on the classification model used then fellow these steps.
 
### Feature Extraction
The first step to create our classification model PhishRod will be using to identify phishing websites
is to construct a labeled dataset to train the model with. 

For that we need to have a list of phishing and non phishing websites that we will extract a set of features from.

The details about the features implemented can be found here: [Features.md](web_scraping/feature_extraction/Features.md)

The set of phishing and non phishing website that were the input to our feature extraction are respectively:

-   `verified_online.json` this is a Json with an array of verified phishing websites from [PhishTank.com](https://phishtank.com),
 a great platform for combating phishing as well, and it exposes its database for developers, you can get it [here](https://phishtank.com/developer_info.php) 
-   `top-1m.csv` this is a csv with the top 1 million trusted websites from [Alexa](https://www.alexa.com/topsites),
 this will serve as our non phishing websites list. 

After providing these two files in the `data` directory, its just a matter of running our feature extraction scripts:

-   `Extract_Features.py` and `Extract_Features_Non_Phish.py` to extract the phishing and non phishing dataset respectively.
These are highly multi-threaded scripts that follow the Thread pool design.

-   `DataProcess_non_Phish.py` is an attempt to use processes instead of threads, the results were less efficient
 than the thread's probably due to the lack of computation power (only tested on 2 cores machine).

To run the extraction scripts simply use these commands:

    $ python web_scraping\feature_extraction\Extract_Features.py
    $ python web_scraping\feature_extraction\Extract_Features_Non_Phish.py


### Training the model

After the previous step we should have 2 new files under `data` called `extracted_Non_Phish.csv` and `extracted_Phish.csv`
that will serve as the input to our model training:

-   `classifier.py` has the pipeline to train and test then dump the model to `classifier.pkl` python object
that will be used after to verify the URL entered to PhishRod. It also has a section to cross validate the model
and visualise the different aspects of it such as feature importance.
So if any changes need to be brought to PhishRod classification model it should live there.

To run the classifier script on have the model, simply run

    $ python classifier/classifier.py


# Usage

After finishing the [installation](#installation) PhishRod should now be accessible at [localhost](http://127.0.0.1:8000).

Tha interface is simple, with one input area to enter the URL and a button to identify whether the website
is a phish or not.
When scrolling the user will find some statistics around recent tests, and a way to send feedback and contact the Admin.

![page_scroll](https://user-images.githubusercontent.com/36813986/117393896-ffad6280-aeec-11eb-9b7b-086e1b150392.png)


### Identifying a phishing website
After Sending a URL the user will have the results shortly after:
* Phish not detected: a lock animation will appear, and a rating space for the user to send his rating on the results
![phish_not_detected](https://user-images.githubusercontent.com/36813986/117427822-5337a480-af1d-11eb-9bb4-ca08a50d1efe.png)

* Phish detected: a Bomb animation will appear, and a rating space for the user to send his rating on the results
![phish_detected](https://user-images.githubusercontent.com/36813986/117427799-4e72f080-af1d-11eb-9112-4cb488b11f53.png)


### Administration

PhishRod is equipped with an Admin space where an administrator will be able to review any recent activities. 
To access it, got to [localhost/admin](http://127.0.0.1:8000/admin)
*   A login page will appear where the admin can provide his credentials:
![admin_login](https://user-images.githubusercontent.com/36813986/117428152-b45f7800-af1d-11eb-89d8-d4620f2a406c.png)

*   After the successful login, the admin will have a simple landing page:
![admin_main_menu](https://user-images.githubusercontent.com/36813986/117393885-fa501800-aeec-11eb-91fc-08702e81fe29.png)

*   The Admin can access the reviews by clicking on the Reviews button:
![admin_reviews](https://user-images.githubusercontent.com/36813986/117393886-fb814500-aeec-11eb-8d62-a52cc2f95080.png)

*   The Admin can access the URLs recently entered by clicking on the URL button:
![admin_url](https://user-images.githubusercontent.com/36813986/117393888-fc19db80-aeec-11eb-959c-ae3e0b997c36.png)
