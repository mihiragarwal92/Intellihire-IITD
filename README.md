# Intellihire Employment Management Software Documentation

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


**1. Introduction**

Overview: The Intellihire Employment Management Software is an innovative solution designed to revolutionize the hiring process by leveraging advanced AI and machine learning technologies.

Purpose: The purpose of this documentation is to provide a comprehensive guide to understanding, using, and managing the Intellihire software.

Scope: This documentation covers the software's features, user guides, technical details, and administration procedures.

**2. Key Features*

•	Job Postings
•	Candidate Sourcing
•	Applicant Tracking
•	Automated Communication
•	Interview Scheduling
•	Candidate Assessment
•	Predictive Analytics
•	Diversity and Inclusion
•	Feedback and Reporting
•	Integration with HR Systems
•	Continuous Learning
•	Realtime ChatBot
•	Template for Face Recognition


**3.# Features for recruiters :-
>Post job posts.
>Recieve applicantions on the job post with access to candidate's full profile and resume.
>Shortlist candidates for further rounds.
>Search for relevant candidates for a job post.
>Search through entire resume database and have access to all resumes.
>Basic Dashboard for track candidate for the interview application.
>Personality Prediction trait using ocean five

# Features for job seekers:-
>Build your profile and add your resume.
>Search for jobs with various filters to suit your needs.
>Save a job post or apply for jobs directly with a single click.
>See status of your applications.

![Alt text](carousel-1.jpg)

This is a high-level overview of the system architecture. The actual architecture may involve more details and considerations based on the specific technologies and platforms used in the implementation of the Intellihire Employment Management Software.
**4. User Guide**
•	Login/Logout
•	Contact Us
•	Make Profile
•	Personality Test

5. Administrator Guide
•	Analyse the registered employees.
•	Post Jobs with respect to locations
•	Track the current performance of the employee
•	Schedule meeting with the Job seeker.
6. Technical Details
Tech Stacks Used:
Backend-
•	Django
•	ML Algorithms (Logistic Regression)
Front End
•	HTML
•	CSS
•	SCSS
•	Javascript
•	Bootstrap4.0
DataBase
•	SQLite


7. Implementation

For further development the above mentioned tech stack should be used. Multiple modules requires the integration with backend and front end. 
8. Support and Maintenance

9. Conclusion

This documentation is designed to guide users, administrators, and developers through the usage, setup, and management of the Intellihire Employment Management Software. It serves as a comprehensive resource for understanding the software's features, architecture, and best practices.

For further inquiries, assistance, or feedback, please contact our support team at [mihiragarwal15@gmail.com][rajsahu012002@gmail.com].

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
![Altextt ](https://github.com/mihiragarwal92/Intellihire-IITD/blob/main/landing%20main.png?raw=true)    
![Altextt ](https://github.com/mihiragarwal92/Intellihire-IITD/blob/main/signup.png) 

# Job Portal
Django Job Portal.       


## Installation 
 Use git commands to copy repo

#Create a Virtual Environment and install Dependencies.
If you don't have the virtualenv command yet, you can find installation instructions here. Learn more about Virtual Environments.
$ pip install virtualenv

#Create a new Virtual Environment for the project and activate it.

$ virtualenv venv
$ source venv/bin/activate

## Install requirements

```
pip install -r requirements.txt
```
## Database

```
Set the database from settings.py
```

## To migrate the database open terminal in project directory and type
```
python manage.py makemigrations
python manage.py migrate
```
create superuser in Django
python manage.py createsuperuser(create admin panel username and password)
Current (email -admin12@gmail.com ,password-12345)

## Collects all static files in your apps
```
python manage.py collectstatic
```

## Run the server
```
python manage.py runserver
```
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Main directory file

*   `jobs`
 * `urls.py` - path reference to the app URLs
 * default django project files, such as: `settings.py`, `wsgi.py`, `asgi.py` etc.
		* `jobsapp` - app directory
		*  `Personality` - app directory
		* `Recognition` - app directory
		* `Accounts` - app directory


  * `static` - directory containing the JavaScript and CSS files inside the app directory within
        
  * `templates` - directory containing the HTML templates inside the app directory within
   
  * `manage.py` - default django file
  * `README.md` - this readme file

## for Quiz app
* cd Quiz
perform same steps for Quiz app
* Create a Virtual Environment and install Dependencies.
* Create a new Virtual Environment for the project and activate it.
* install requirements.
* migrate the databse
** python manage.py runserver
![Altextt ](https://github.com/mihiragarwal92/Intellihire-IITD/blob/main/Landing%20page.png)    

*This Project is prepared by TEAM JSS (Mihir Agarwal,Raj Sahu) under the supervision of Prof. Jyoti Kumar and Prof. Greeshma Sharma (Design Dept-IITD). We're extremely grateful to the mentors to gave us this opportunity to intern for this project that motivated us to learn and grow more. We've put our sincerest efforts while building this project from scratch.*

<div align="center">
    <h3>========Thank You=========</h3>
</div>







