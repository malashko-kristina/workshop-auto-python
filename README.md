### General information
This repository contains backend and frontend autotests written in Python using pytest, request, playwright.

### CI/CD pipeline results
After each pipeline run the allure report is being generated. It can be found in "Summary" section in "Artifacts" on the bottom of the screen. The name of artifact is "allure-report".

Steps to open "allure-report":
1. Download a file on your local computer.
2. Unzip the file "allure-report".
3. In your terminal open "allure-report" folder with  --->  cd *your-path-to*/allure-report.
4. When "allure-report" folder is opened in your terminal use a command  --->  allure open ./
5. After that allure report will be opened in a browser with all graphical results.


### Automated Allure Reports
Allure reports are being generated in a seperate gh-pages branch after pipeline. In order to open a report go to https://malashko-kristina.github.io/workshop-auto-python (the link can be found in Settings -> Pages).
