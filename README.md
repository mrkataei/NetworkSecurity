#Funny API
this project provide you some basic api request(POST, GET methods)
<br>
localhost:8000/allowme (GET) open 22 ssh port for you<br>
localhost:8000/checkme (POST) check port "port" field int<br>
localhost:8000/log (GET) response all logs about your ip<br>
localhost:8000/domain (GET) response your domain name<br>
localhost:8000/checkava (POST) check your "link" file available<br>
localhost:8000/domain (GET) check your ip if is not in white-list banned you<br>

<h3>use</h3>
<h3>make migration and migrate with command line</h3><br>
`python .\manage.py makemigrations`<br>
`python .\manage.py migrate`<br>
<h3>run server</h3>
` python .\manage.py runserver`