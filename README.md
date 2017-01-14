## Mutual Funds (public repo)  

"Financial aggregator and news provider"

Technology stack: Python, Django, PostgreSQL, Redis, HTML, CSS, JS, Vagrant, Celery, NginX, Gunicorn 

![alt tag](https://s3-eu-west-1.amazonaws.com/bernatskyys/github/1.png)

#### Quick tour
The main feature of this website is real time and scheduled parsers.  
Every day website automatically updates all information. For this purpose there are two complex parsers which work
based on cron time.  

- Also when you are adding new `Fund` there is also realtime parser which is asynchronously parsing information  

![alt tag](https://s3-eu-west-1.amazonaws.com/bernatskyys/github/2.png)  

- Here we are adding `Fund`. As you can see there is only three fields necessary, other fields will be parsed automatically.  

![alt tag](https://s3-eu-west-1.amazonaws.com/bernatskyys/github/3.png)  

- Awesome notification:)  

![alt tag](https://s3-eu-west-1.amazonaws.com/bernatskyys/github/4.png)  

- When `Fund` is parsed there is also async notification.  

![alt tag](https://s3-eu-west-1.amazonaws.com/bernatskyys/github/5.png)  

- Here you can see what exactly information was parsed  

![alt tag](https://s3-eu-west-1.amazonaws.com/bernatskyys/github/6.png)  

- And a lot of parsed history date :)  P.S. about 34k history ticks per fund    

![alt tag](https://s3-eu-west-1.amazonaws.com/bernatskyys/github/7.png)  

