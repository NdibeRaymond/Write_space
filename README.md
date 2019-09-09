# Write_space
WriteSpace is a personal blog built for the purpose of self expression and to learn more about the django framework
http://ndiberaymond.pythonanywhere.com

# To Start

* clone the repository
* create a virtual env
* activate it and `pip install requirements.txt`
* run `python manage.py makemigrations` and `python manage.py migrate` then run `python manage.py runserver` to start the server and serve the project


# To Access The Api

i am assuming you are using curl for this. you can ofcourse copy only the endpoint and maybe make the api call with any requests library to fancy

* to get access token(short lived) => curl -X POST -d "username=<random_username>&password=<random_password>" http://ndiberaymond.pythonanywhere.com/api/token-auth/

* to get refresh token(long lived) => curl -X POST -d "token=your access token goes here" http://127.0.0.1:8000/api/refresh_token/

* to add a comment => curl -H "Authorization: JWT your access token goes here" -X POST -d "text=this is some content" http://ndiberaymond.pythonanywhere.com/api/posts/12/comments/add/

* to edit a comment => curl -H "Authorization: JWT your access token goes here" -X PUT -d "text=this is an edited comment" http://ndiberaymond.pythonanywhere.com/api/posts/comments/44/edit/

* to create a new post => curl -H "Authorization: JWT your access token goes here" -X POST
 -d "title=your post title&post_heading=your post heading&main_im
age=C:image file path(note that there is still an issue here)&text=post text body" http:/
/ndiberaymond.pythonanywhere.com/api/posts/<username>/new/


# ToDo

* add haystack search functionality (no time to add that yet)
* convert the whole frontend to react and access the backend solely through the api
* and yeaa, actually start posting useful stuffs to the blog. lolsssssss