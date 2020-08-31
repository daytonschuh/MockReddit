from locust import HttpLocust, TaskSet, task, between


class TestingTasks(TaskSet):

    # Testing Posts
    @task(1)
    def register_user(self):
        self.client.post("/register", data={'id': '2147483647',
                                            'user_name': 'test_user',
                                            'email': 'thisisatest@gmail.com',
                                            'first_name': 'Johnny',
                                            'last_name': 'Test',
                                            'password': 'password',
                                            'karma': '0'})

    @task(1)
    def create_post(self):
        self.client.post("/create_post", data={'post_id':'2147483647',
                                               'user_name':'test_user',
                                               'title':'Test',
                                               'text':'Test',
                                               'community':'Test',
                                               'resource_url':'www.thisisatest.com'})

    @task(1)
    def send_message(self):
        self.client.post("/send_message", data={'id':'2147483647',
                                                'message_id':'2147483647',
                                                'user_from':'dean_su',
                                                'user_to':'test_user',
                                                'contents':'ThisIsATest',
                                                'flag':''})

    # Testing Puts
    @task(1)
    def update_email(self):
        self.client.put("/update_email", data={'user_name':'test_user',
                                               'email':'thisisatest@gmail.com'})

    @task(1)
    def increment_karma(self):
        self.client.put("/increment_karma", data={'user_name':'test_user'})

    @task(1)
    def decrement_karma(self):
        self.client.put("/decrement_karma", data={'user_name':'test_user'})

    @task(1)
    def up_vote_posts(self):
        self.client.put("/up_vote_post/2147483647")

    @task(1)
    def down_vote_posts(self):
        self.client.put("/down_vote_post/2147483647")

    @task(1)
    def list_favorite_messsage(self):
        self.client.put("/favorite_message/2147483647")

    # Testing Gets
    @task(1)
    def retrieve_post(self):
        self.client.get("/retrieve_post/2147483647")

    @task(1)
    def retrieve_post_list(self):
        self.client.get("/list_posts/3")

    @task(1)
    def list_post_votes(self):
        self.client.get("/list_post_votes/2147483647")

    @task(1)
    def list_n_post_votes(self):
        self.client.get("/list_n_post_votes/5")

    @task(1)
    def list_post_votes_in_list(self):
        self.client.get("/list_post_votes_in_list/Test")

    # Testing Deletes
    @task(1)
    def delete_post(self):
        self.client.delete("/delete_post/2147483647")

    @task(1)
    def delete_message(self):
        self.client.delete("/delete_message/2147483647")

    @task(1)
    def deactivate_account(self):
        self.client.delete("/deactivate_account/test_user")



class WebsiteWeeb(HttpLocust):
    task_set = TestingTasks
    wait_time = between(1,2)