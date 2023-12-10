## Financial Stock Analysis


# Microservice
    -   The application is designed around a specific business capability - fetching data from an API and providing real-time and historical stock analysis. This aligns with the principle of single responsibility in microservices architecture.
    -   The application is designed to be deployed as a containerized application. A Docker Image is available on Dockerhub for the same. This aligns with the principle of infrastructure automation in microservices architecture.
    -   The application has its own data pipeline, storing data in a Delta Lake in Azure Workspace. This aligns with the principle of decentralized data management in microservices architecture.

# Load Test
    -   The application is designed to manage a high volume of requests. Load testing was performed using Locust, and the results demonstrated that the application can effectively handle up to 10,000 concurrent users. The maximum response time recorded during this load test was 70,000 milliseconds (or 70 seconds). These results underscore the application's adherence to the principle of elasticity in a microservices architecture, as it can scale to accommodate significant traffic and maintain functionality under heavy load.

![Load_Test_Results]("results/Load_Test_v1.png")

# Data Engineering
    -   The application used Pandas for data analysis
    -   The application used PySpark for data wrangling manipulation
    -   The application used Spark SQL for data querying and ETL
    -   The application used Delta Lake for data storage

# Infrastructure as Code (IaC)
    `Your project must utilize an IaC solution for infrastructure setup and management. You can choose among AWS CloudFormation, AWS SAM, AWS CDK, or the Serverless Framework.`

# Continuous Integration and Continuous Delivery (CI/CD)
    `Implement a CI/CD pipeline for your project. It could be through GitHub Actions or AWS Cloud Build or any other relevant tool.`

# Architectural Diagram
    `A clear diagram representing the architecture of your application should be included in your project documentation.`

# GitHub Configurations
    `Your GitHub repository must include GitHub Actions and a .devcontainer configuration for GitHub Codespaces. This should make the local version of your project completely reproducible. The repository should also include GitHub Action build badges for install, lint, test, and format actions.`

# Quantitative Assessment
    The load test results are available in the `results` folder. The system performance showed that the median response time increased after ~ 18,000 users

![plot]("results/system_performance.png")


# Demo Video
[Link]()

# Team Members