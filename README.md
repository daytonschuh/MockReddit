# MockReddit

## Introduction
  This project was developed with python in the PyCharm IDE using Flask and SQLAlchemy. It implements post, account, vote and message microservices by making use of HTTP methods. Early development testing was done using Postman, but has since been updated to test through bash scripts and Locustio. Foreman manages the process of our WSGI container, Gunicorn.

## Tech Stack
  - Python
  - Gunicorn
  - Foreman
  - Caddy
  - Locustio
  - Flask
  - Flask-Login
  - Flask_SQLAlchemy
  - Flask_Marshmallow
  - Marshmallow_SQLAlchemy
  - Pytz
  
  
## Running the Project
  - Clone the repository on a linux machine
  ```git clone https://github.com/daytonschuh/MockReddit```
  - Navigate to the correct directory
  ```cd MockReddit```
  - Install the libraries in Terminal(1)
  ```bash autoinstall.sh```
  - Start the loadbalancer in Terminal(1)
  ```ulimit -n 8192 && caddy```
  - Start the wsgi process in Terminal(2)
    ```foreman start -m accounts=3,posts=3,votes=3,messages=3```
  - Test the server in Terminal(3)
    - For validation testing: ```bash testall.sh```    
    - For system load testing: ```locust --host=http://localhost:5000 --locustfile locustfile.py --no-web -c 100 -r 10```
    
## API Routing
|                            URI                             |     Method    |            Response            |
| ---------------------------------------------------------- | ------------- |--------------------------------|
| /api/v1/register                                           |      POST     | 201: Success <br> 409: Failure |
| /api/v1/create_post                                        |      POST     | 201: Success <br> 409: Failure |
| /api/v1/send_message                                       |      POST     | 201: Success <br> 409: Failure |
| /api/v1/update_email                                       |      PUT      | 202: Success <br> 404: Failure |
| /api/v1/increment_karma                                    |      PUT      | 202: Success <br> 404: Failure |
| /api/v1/decrement_karma                                    |      PUT      | 202: Success <br> 404: Failure |
| /api/v1/upvote_post/<int:post_id>                          |      PUT      | 202: Success <br> 404: Failure |
| /api/v1/downvote_post/<int:post_id>                        |      PUT      | 202: Success <br> 404: Failure |
| /api/v1/favorite_message/<int:message_id>                  |      PUT      | 202: Success <br> 404: Failure |
| /api/v1/retrieve_post/<int:post_id>                        |      GET      | 202: Success <br> 404: Failure |
| /api/v1/list_posts_by_comm/<string:community>/<int:number> |      GET      | 202: Success <br> 404: Failure |
| /api/v1/list_posts/<int:number>                            |      GET      | 202: Success <br> 404: Failure |
| /api/v1/list_post_votes/<int:post_id>                      |      GET      | 202: Success <br> 404: Failure |
| /api/v1/deactivate_account/<int:user_id>                   |     DELETE    | 202: Success <br> 404: Failure |
| /api/v1/delete_post/<int:post_id>                          |     DELETE    | 202: Success <br> 404: Failure |
| /api/v1/delete_message/<int:message_id>                    |     DELETE    | 202: Success <br> 404: Failure |
