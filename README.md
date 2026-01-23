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

bash
cd "SoftDevGrProject_Repo-main(2)"
This avoids the bash syntax error you saw earlier.

3. Create and activate a virtual environment
Codespaces supports this out of the box:

bash
python3 -m venv venv
source venv/bin/activate
(Windows-style activation isn’t needed because Codespaces runs Linux.)

4. Install dependencies
If you have a requirements.txt:

bash
pip install -r requirements.txt
If not, you can skip this step.

5. Run the application
Depending on your framework:

If Django
bash
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
Codespaces requires the 0.0.0.0 binding so the port can be forwarded.


