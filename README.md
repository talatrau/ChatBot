# Intent Classfication API

### Technology:
Frontend use **Reactjs** <br>
Backend use **Django** <br>
Pass data with **Rest_API**

### Pre install package:

```
# package for Reactjs
npm install axios

# package for Django
pip install --upgrade pip
pip install Cython
pip install scikit-learn==0.22.2.post1
pip install underthesea
pip install djangorestframework
pip install django-cors-headers
pip install pillow
pip install psycopg2
pip install tensorflow
pip install tf-nightly

# docker for postgresql
docker pull postgresql
```

### Run application:

```
# run docker first with command
docker run --name postsql -d -p 2345:5432 -e POSTGRES_PASSWORD=password postgres

# run Django with command
python chatbot_backend/manage.py makemigrations
python chatbot_backend/manage.py migrate
python chatbot_backend/manage.py runserver

# run Reactjs with command
npm start --prefix chatbot_frontend/
```
