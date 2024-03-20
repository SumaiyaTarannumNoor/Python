To Create and Use a Python Virtual Environment

1. To create

   python -m venv env (For Windows)

   python3 -m venv env (for mac)

   env here is whatever you want to name your virtual enviroment to be.

2. To activate the environment in windows -

   - env\Scripts\activate.bat

   or, env\Scripts\activate

   To activate the environment in MAC

   - source env/bin/activate

3. To deactivate, just type

   - deactivate

4. To see all the packages within the environment

   - pip list

5. To install request package

   - pip install request

6. To push into github and/or deployment we don't need the whole env, we only need requirements.

   To get all the requirements of our projects particular environment

   - pip freeze > requirements.txt

7. To install everything from requirements.txt

   - pip install -r requirements.txt

8. Create your virtual environment in your project folder, where all the other Python files, folders, and dependencies are kept. Also, do not put anything inside virtual environment folder, for example, do not keep anything inside env.

9. To delete or remove the folder, ... Just Delete.

   or,

   - del env (for Windows)

   - rmdir env (for Windows)

   - rm -r env (for Mac)
