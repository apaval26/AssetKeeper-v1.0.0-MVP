# AssetKeeper v1.0.0 MVP
This repository contains  the Minimum Viable Product for the AssetKeeper asset management system final year project.

1. Open the repository in Codespaces
Your supervisor can do this directly from your repo:

Click Code

Select Codespaces

Click “Create codespace on main”

GitHub will automatically create a cloud development environment with:

Python preinstalled

VS Code interface

Terminal access

Your project files ready to run

No local setup needed.

2. Navigate to the project folder
If your MVP is inside a subfolder with parentheses, they must be quoted:
cd "SoftDevGrProject_Repo-main(2)"
This avoids the bash syntax error you saw earlier.

If no directory found message is displayed, type ls in the console and copy and paste the SoftDevGrProject_Repo-main(2) from there with the quotation marks and add it to the cd command.

Then type cd SoftDevGrProject_Repo-main command twice.

4. Install dependencies
If you have a requirements.txt:
pip install -r requirements.txt in the terminal.
If not, you can skip this step.

5. Install Django and ApScheduler(If not included)

pip install django
pip install apscheduler(automated notifications)

6. Run the application
python manage.py runserver 
Codespaces requires the 0.0.0.0 binding so the port can be forwarded.


