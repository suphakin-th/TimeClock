# README

# Setting Up
### Project
* clone project
* use docker for run project in easy way

### Docker 
* After config volumes path already, run this command

> $ docker-compose up -d
> 
### Database
* run this command for exec to Database

> $ docker-compose exec mariadb bash<br/>
> $ # mysql -uroot -ppassword<br/>
> MariaDB [(none)]> CREATE DATABASE "DatabaseName" CHARACTER SET utf8 COLLATE utf8_thai_520_w2;

* open new terminal in project path and exec this command for create table in database

> $ docker-compose exec backend bash<br/>
> $ python manage.py migrate
