# Face-recognition

Reference Document
  * https://pypi.org/project/face-recognition/
  * https://medium.com/@aadimator/how-to-set-up-opencv-in-intellij-idea-6eb103c1d45c#:~:text=Click%20the%20%2B%20icon%20on%20the,the%20Add%20Jar%2FDirectory%20option.&text=Then%20browse%20to%20the%20path,jar%20and%20click%20OK.
  * Python Interpreter - https://www.jetbrains.com/help/idea/configuring-local-python-interpreters.html
  * Install OpenCV python in Windows - https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_setup/py_setup_in_windows/py_setup_in_windows.html
  * Install openCV using pip - https://stackoverflow.com/questions/51853018/how-do-i-install-opencv-using-pip
 
 
 List of Error and steps to resolve
  * https://stackoverflow.com/questions/60007427/cv2-warn0-global-cap-msmf-cpp-674-sourcereadercbsourcereadercb-termina
  * https://stackoverflow.com/questions/31996367/opencv-resize-fails-on-large-image-with-error-215-ssize-area-0-in-funct


### Use Cases for this Application


**USE CASE 1**
```
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
-------------------------------------------------------------------------------------------------------------------
Flow of activities |	          Actor              |                   	                  System
-------------------------------------------------------------------------------------------------------------
                    |  Customer visits a Point of Sale             |      System looks up for the matching record/data in the backend
                      (POS) and requests login authentication           database and validates the obtained facial imagery against it
                       

Exception conditions : 	None
```

**USE CASE 2**
```
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
  Exception conditions :	
    - Customer is not present in the database.
    - Customer’s preferred medium of communication is not valid/missing.
    - Customer’s preferred payment method is not valid/missing.
```
