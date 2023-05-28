# Job Search Website
This is a job search website built using Django, Adzuna API, Bootstrap, JavaScript, Python, HTML, and CSS. The website allows users to browse job listings, search for specific jobs based on various criteria, and save job listings for later reference. It is designed to be mobile-responsive, ensuring a seamless experience across different devices.

## Distinctiveness and Complexity
This project satisfies the distinctiveness and complexity requirements in the following ways:

1. **Distinctiveness**: The job search website offers unique features and functionalities that set it apart from other projects in the course. It leverages the Adzuna API to fetch real-time job data, providing users with up-to-date job listings from various sources. The integration of the Adzuna API and the development of a custom search engine differentiate this project from others.
2. **Complexity**: The website incorporates a range of technologies and frameworks to create a robust and dynamic user experience. It utilizes Django as the back-end framework, allowing for efficient data management and seamless integration with the front-end. JavaScript is used to enhance the user interface and provide interactive features such as real-time search suggestions and advanced search options. The project also incorporates HTML and CSS to ensure a visually appealing and mobile-responsive design.

## Requirements
To meet the requirements of the project, the following criteria have been fulfilled:

- The web application is distinct from other projects in the course by leveraging the Adzuna API, providing real-time job listings, and implementing custom search functionality.
- It is more complex than other projects by incorporating Django on the back-end, JavaScript on the front-end, and ensuring mobile responsiveness.
- The website's features, such as browsing job categories, selecting the country, specifying job criteria, and performing advanced searches, demonstrate its uniqueness and complexity.
- By adhering to these requirements, the job search website offers a user-friendly platform for finding, saving, and managing job listings effectively.

## File Structure
The project's file structure is organized as follows:

- \`**README.md**\`: This file provides documentation and instructions for running the application.
- \`**requirements.txt**\`: Contains a list of the required Python packages and their versions for the project.
- \`**manage.py**\`: The entry point for executing various Django commands.
- \`**finalproject/**\`: The main Django project directory.
    - \`**settings.py**\`: Configuration file for Django project settings, including database configuration, installed apps, and static file paths.
    - \`**urls.py**\`: Defines the project's URL patterns and their corresponding views.
    - \`**wsgi.py**\`: WSGI application entry point for deployment.
- \`**jobsearch/**\`: Django app directory for handling job-related functionality.
    - \`**models.py**\`: Contains Django models for representing job listings, user profiles, and saved job listings.
    - \`**views.py**\`: Defines the views and request handlers for rendering job listings, search results, and user actions.
    - **templates/**: Directory for storing HTML templates used by the app.
    - \`**static/**\`: Directory for storing static files such as CSS stylesheets, JavaScript files, and images.
- **Other Django-related files**: These files are automatically generated by Django and are used for database migrations, caching, and other internal operations.

## Running the Application
To run the job search website, follow these steps:

1. Clone the project repository to your local machine.

    ```git clone https://github.com/diandrarad/cs50w-finalproject.git```

2. Make sure you have Python and Django installed on your system.
3. Install the required Python packages by running the following command in the project's root directory:

    ```pip install -r requirements.txt```
    
4. Set up the database by executing the following commands:

    ```python manage.py makemigrations jobsearch```
    
    ```python manage.py migrate```
    
5. Obtain an API key from Adzuna API and update the APP_ID and APP_KEY variables with your own credentials in the settings.py file located in the project directory.

    ```APP_ID = 'your_app_id'```
    
    ```APP_KEY = 'your_app_key'```

6. Start the development server by running the following command:

    ```python manage.py runserver```

7. Open your web browser and visit \`http://localhost:8000\` to access the job search website.
