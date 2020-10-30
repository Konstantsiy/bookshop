Software Requirements Specifications (SRS) for Bookshop
***version 1.0.0***
# 1. Introduction
## 1.1 Purpose
A store where you can search and buy books through PayPal payment system.
## 1.2 Scope
The objective of this project is to create and implement a website bookstore. The website will allow users to create and maintain individual secured accounts, search the      Bookshop database for textbooks, and make secured online credit card purchases. Users will be able to search for the required books by various characteristics. 
# 2. Overall Description
## 2.1 Product Respective
The bookshop is not a component of a larger system, it is a self-powered product.
The bookshop system will interact with the credit card processing system to process purchases on the site. The system will also interact with a bookstore inventory database that records the number of books available sold in inventory.

![alt text](https://github.com/Konstantsiy/bookshop/blob/master/docs/system.png)
## 2.2. Product Features
The following list of function descriptions explains the major features of the Online Bookshop:
- Account registration.
- Account login.
- Search for books.
- View book descriptions and authors.
- Add to shopping cart.
- Delete from shopping cart.
- Account logout.
## 2.3. Operating Environment
Bookshop will primarily act as a web service that will be supported on web browsers including Google Chrome and Firefox 18. Underlying operating system is Windows or Linux.
Bookstore will be running on local host that has [Django](https://www.djangoproject.com/download/), [Python 3.8](https://www.python.org/downloads/), and [MySQL](https://dev.mysql.com/downloads/) running on it.
# 3. Requirement Specifications 
## 3.1 User Requirements
Users of the website must know how to navigate in a website. The initial users of our software front end will be people who are familiar with navigating a web browser and managing a desktop or laptop.
## 3.2 Performance Requirements
The performance requirements are as follows:
- System login/logout shall take less than 5 seconds.
- Searches shall return results within 10 seconds.
- Orders shall be processed within 10 seconds.
## 3.3 Design Constraints
The Bookshop shall conform to the following design constraints:
- Able to support PC platform.
- System supports all web browsers.
## 3.4 Security
Users will be able to access only their own personal information and not that of other users. Purchases will be handled through a secure system to ensure the protection of user’s credit card and personal information.
