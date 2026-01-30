This repository contains the Minimum Viable Product (MVP) for the AssetKeeper asset management system final‑year project.

1. Open the repository in GitHub Codespaces
Your supervisor can run the project directly in the cloud without installing anything locally.

Open the GitHub repository

Click Code

Select the Codespaces tab

Click Create codespace on main

GitHub will automatically create a cloud development environment with:

Python preinstalled

VS Code interface

Terminal access

All project files ready to run

No local setup is required.

2. Navigate to the project folder
If the project folder contains parentheses, it must be quoted in the terminal to avoid a Bash syntax error.

Example:

Code
cd "SoftDevGrProject_Repo-main(2)"
If the terminal reports “No such file or directory”, type:

Code
ls
Then copy the exact folder name shown and use it inside quotes:

Code
cd "<folder name>"
If the project contains a nested folder with the same name, enter it:

Code
cd SoftDevGrProject_Repo-main
3. Install dependencies
If the repository includes a requirements.txt file:

Code
pip install -r requirements.txt
If not, install Django and APScheduler manually:

Code
pip install django
pip install apscheduler
4. Run the application
Start the Django development server:

Code
python manage.py runserver 0.0.0.0:8000
Codespaces requires the 0.0.0.0 binding so the port can be forwarded to the browser.
