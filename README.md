# Financial Stock Analysis


## Microservice

-   The application is designed around a specific business capability - fetching data from an API and providing real-time and historical stock analysis. This aligns with the principle of single responsibility in microservices architecture.
-   The application is designed to be deployed as a containerized application. A Docker Image is available on Dockerhub for the same. This aligns with the principle of infrastructure automation in microservices architecture.
-   The application has its own data pipeline, storing data in a Delta Lake in Azure Workspace. This aligns with the principle of decentralized data management in microservices architecture.

## Load Test
-   The application is designed to manage a high volume of requests. Load testing was performed using Locust, and the results demonstrated that the application can effectively handle up to 10,000 concurrent users. The maximum response time recorded during this load test was 70,000 milliseconds (or 70 seconds). These results underscore the application's adherence to the principle of elasticity in a microservices architecture, as it can scale to accommodate significant traffic and maintain functionality under heavy load.

![Load_Test_Results](/results/Load_Test_v1.png)

## Data Engineering
-   The application used Pandas for data analysis
-   The application used PySpark for data wrangling manipulation
-   The application used Spark SQL for data querying and ETL
-   The application used Delta Lake for data storage

## Infrastructure as Code (IaC)
`Infrastructure as Code (IaC)` is a practice in which the infrastructure setup is written in code files, rather than manually configured. These code files can be version-controlled and reviewed, allowing for easy changes and rapid disaster recovery.

Here's how your project satisfies the Infrastructure as Code requirement:

`Dockerization:` We have containerized the application using Docker. The Dockerfile serves as a form of Infrastructure as Code, as it automates the process of setting up the application environment.

`Hosting on Azure ACR:` We have used Azure Resource Manager (ARM) templates scripts to automate the deployment of your Docker containers to Azure ACR, this is also a form of Infrastructure as Code.

`Data Pipeline Setup:` The setup of the data pipeline (from API to Delta Lake in Azure Workspaces) is automated using Azure Workflows that are scheduled to run daily, this is another example of Infrastructure as Code.

## Continuous Integration and Continuous Delivery (CI/CD)
    `Implement a CI/CD pipeline for your project. It could be through GitHub Actions or AWS Cloud Build or any other relevant tool.`

## Architectural Diagram
    `A clear diagram representing the architecture of your application should be included in your project documentation.`

## GitHub Configurations
    `Your GitHub repository must include GitHub Actions and a .devcontainer configuration for GitHub Codespaces. This should make the local version of your project completely reproducible. The repository should also include GitHub Action build badges for install, lint, test, and format actions.`

## Quantitative Assessment
-    The load test results are available in the `results` folder. The system performance showed that the median response time increased after ~ 18,000 users

![plot](results/system_performance.png)


## Demo Video
[Link]()

## Team Members


#

## File Index

Files in this repository include:


## 1. Readme
  The `README.md` file is a markdown file that contains basic information about the repository, what files it contains, and how to consume them


## 2. Requirements
  The `requirements.txt` file has a list of packages to be installed for any required project. Currently, my requirements file contains some basic python packages.


## 3. Codes
  This folder contains all the code files used in this repository - the files named "Test_" will be used for testing and the remaining will define certain functions


## 4. Resources and Templates
  -  This folder contains any other files relevant to this project. 
    -  `index.html` - an HTML File containing the front end view of the text generator page
    -  `result.html` - an HTML File containing the result view of the text generator model


## 5. CI/CD Automation Files


  ### 5(a). Makefile
  The `Makefile` contains instructions for installing packages (specified in `requirements.txt`), formatting the code (using black formatting), testing the code (running all the sample python code files starting with the term *'Check...'* ), and linting the code using pylint


  ### 5(b). Github Actions
  Github Actions uses the `main.yml` file to call the functions defined in the Makefile based on triggers such as push or pull. Currently, every time a change is pushed onto the repository, it runs the install packages, formatting the code, linting the code, and then testing the code functions


  ### 5(c). Devcontainer
  
  The `.devcontainer` folder mainly contains two files - 
  * `Dockerfile` defines the environment variables - essentially it ensures that all collaborators using the repository are working on the same environment to avoid conflicts and version mismatch issues
  * `devcontainer.json` is a json file that specifies the environment variables including the installed extensions in the virtual environment
