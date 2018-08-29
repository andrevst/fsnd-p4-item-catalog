# Item Catalog

_A Udacity Fullstack Web Developer nanodegree project._

## Objectives of the project

This application provides a list of items within a variety of categories as well as provide a user registration and authentication system. Registered users will have the ability to post, edit and delete their own items. 

- The project aim to develop a RESTful web application using the Python framework Flask along with implementation on third-party OAuth authentication. 
- The project attempts to properly use HTTP methods available to work with CRUD (create, read, update and delete) operations.
- Project [rubrick](https://review.udacity.com/#!/rubrics/5/view).

## Development

### Objectives

- [X] Implement a database structure
- [X] Implement basic app to connect with the database
- [X] Implement Route to consult the DB (Read option)
- [X] Implement Route to add data on the DB (Create option)
- [X] Implement Route to edit data on the DB (Update option)
- [X] Implement Route to consult delete data on the DB (Delete option)
- [X] Create templates for the Routes
- [X] Add Style for the Routes
- [X] create Secure Login with Google
- [X] Make Create, Update and Delete routes Secure
- [X] Create Logout

## How to run

### PreRequisites
 - [Python ~2.7](https://www.python.org/)
 - [Vagrant](https://www.vagrantup.com/)
 - [VirtualBox](https://www.virtualbox.org/)
 
### Setup Project:

1. Download [Vagrant](https://www.vagrantup.com/downloads.html) and install.
2. Download [Virtual Box 5.1.x](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1) and install.
3. Fork and Clone or Download [Udacity's Linux-based virtual machine](https://github.com/udacity/fullstack-nanodegree-vm) configuration
4. Find the catalog folder and replace it with the content of this current repository, by either downloading or cloning it from [Here](https://github.com/andrevst/fsnd-p4-item-catalog).

#### Launch Project
1. Launch the Vagrant VM using command: ```$ vagrant up```
2. Update your versions of Flask, _ and _ to match the one used. Use the following commands:

```shell
sudo pip install werkzeug==0.8.3
sudo pip install flask==0.9
sudo pip install Flask-Login==0.1.3
```

3. Run your application within the VM on the folder where you clone this repo run: ```$ python application.py```
4. Access and test your application by visiting [http://localhost:5000](http://localhost:5000).

## Inspirational work from other students

[sagarchoudhary96](https://github.com/sagarchoudhary96/P5-Item-Catalog)

[ddavignon](https://github.com/ddavignon/item-catalog)

[DawoonC](https://github.com/DawoonC/nd-sharables/)

Udacity [ud330](https://github.com/udacity/ud330) was a great help on this.
