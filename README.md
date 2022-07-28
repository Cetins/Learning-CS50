# EDX CS50 Harvard 2019 | Final Project | Gift Code Generator and Validator Database

This web application based on CS50 Finance but polished with a darker theme by Bootstrap

Aplication has 3 main functions:

* Generates random codes from numbers and letters combination in a range of 8 to 16 characters.
* Checks the code you receive from customer whether the code in still available in database.
* Validate the code when customer used it and deletes from database to prevent multiple use.

### There are 9 display pages and 1 layout page in the web application

#### Index

* logged in user can see the existing codes in a table with the code, type of the code(cash/discount)
* if it's a cash gift card it's displayed as £
* if it's a discount gift card(voucher) it's displayed as % in addition to type column
* index page only displays active code as inactive codes deleted from database once validated

#### Login
* registered users can logged in with username and password

#### Register

* users can register with a username and password
* passwords are not stored as string literals, they are hashed into users table hash column
    
#### Generate

* user can generate codes by
    * choosing a length for the code between 8-16 characters
    * choosing a type for the code: Cash or Discount
    * choosing an amount: an integer with minumum value of 1

#### Check

* users can type their code and check if it exists in their database
* if not match found system displays an error message

#### Checked

* once application finds the code submitted for check, this page is displays a table to display the code

#### Validate

* users can validate the code when a customer wants to use it
* it gives and error if the code can't be found on the database

#### Apology

* error display page when something went wrong

#### Success

* when a query completed with success this page displays a custom message
* for now this page only works for generate code function

#### Database is created with two main tables

- users: to record users username and hash
- codes: to record codes created by users

#### Programming languages and libraries

* HTML
* CSS
* Python
* Flask
* MySql

#### SOURCES

* https://bootswatch.com/
* https://getbootstrap.com/docs/4.1/content/
* https://www.pexels.com
