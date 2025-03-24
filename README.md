##To run app from the product root folder

- Clone repo
- Install packages from requirements.txt - pip install -r requirement.txt
- Create a .env file in the root
- CHeck the env-example file in the root and set required env variable in the ,env file
- Run - "alembic upgrade head" to create db tables
- In development run: uvicorn app.main:app --reload or python -m app.main
