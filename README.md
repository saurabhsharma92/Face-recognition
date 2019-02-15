# Face-recognition
Initial Setup
USE CASE 1:
Name :	Customer identification
Scenario :	Identify the customers as one biometric authentication
Triggering event : 	Customer turns up at an automated kiosk to gain entrance to a sporting event, make a purchase, and order an alcoholic beverage
Brief description :	Customer identification is validated against the stored record and further account access is approved/rejected accordingly
Actors	Customer
Organisational benefits :	Improved customer satisfaction, frictionless customer experience, improved transaction speed
Preconditions :	Customer and identification history, against which it will be validated must exist
Postconditions :	Customer is identified
                  Access to the related account is granted
                  Functionalities are provided based on his previously saved settings
Flow of activities |	          Actor              |                   	                  System
-------------------------------------------------------------------------------------------------------------
                    |  Customer visits a Point of Sale             |      System looks up for the matching record/data in the backend
                      (POS) and requests login authentication           database and validates the obtained facial imagery against it
                       

Exception conditions : 	None


USE CASE 2:

Name :	Link the identified consumer to their preferred payment methods, preferred communications (email receipt) and prior order history
Scenario :	Customer is trying to make a payment for attending an event
Triggering event :	Customer’s identity has been verified and the system is ready to book the ticket
Brief description :	Customer comes to the ticket booking counter of an event where his/her face is scanned for identification purposes and then makes a payment to purchase a ticket
Actors :	Customer
Organisational benefits :	Remove the hassle of using credit cards, e-wallets, etc. for payment
Preconditions :	Customer’s ID, preferred payment details and preferred medium of communication must be present in the database
Postconditions :	Notify the status of transaction immediately at the location
Send a confirmation message over their preferred medium of communication (email/text) along with the payment receipt
Flow of activities : 	 
Exception conditions :	Customer is not present in the database.
                        Customer’s preferred medium of communication is not valid/missing.
                        Customer’s preferred payment method is not valid/missing.

