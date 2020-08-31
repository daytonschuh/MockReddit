################# TESTING POST METHODS #################
# Create a user
curl -d 'id=2147483647&user_name=test_user&email=thisisatest@gmail.com&first_name=Johnny&last_name=Test&password=password&karma=0' http://localhost:5000/register

# Create a post
curl -d 'post_id=2147483647&user_name=test_user&title=Test&text=Test&community=Test&resource_url=www.thisisatest.com' http://localhost:5000/create_post

# Send a message
curl -d 'id=2147483647&message_id=2147483647&user_from=dean_su&user_to=test_user&contents=ThisIsATest&flag=Favorite' http://localhost:5000/send_message

################# TESTING PUT METHODS ##################
# Update email
curl -X PUT -d 'id=2147483647&user_name=test_user&email=thisisatest@gmail.com&first_name=Johnny&last_name=Test&password=password&karma=0' http://localhost:5000/update_email

# Increment Karma
curl -X PUT -d 'id=2147483647&user_name=test_user&email=thisisatest@gmail.com&first_name=Johnny&last_name=Test&password=password&karma=0' http://localhost:5000/increment_karma

# Decrement Karma
curl -X PUT -d 'id=2147483647&user_name=test_user&email=thisisatest@gmail.com&first_name=Johnny&last_name=Test&password=password&karma=0' http://localhost:5000/decrement_karma

# Upvote a post
curl -X PUT http://localhost:5000/up_vote_post/2147483647

# Downvote a post
curl -X PUT http://localhost:5000/down_vote_post/2147483647

# Favorite a message
curl -X PUT http://localhost:5000/favorite_message/2147483647

################# TESTING GET METHODS ##################
# Retrieve a post
curl http://localhost:5000/retrieve_post/2147483647

# Get n most recent posts from a community
curl http://localhost:5000/list_posts_comm/News/3

# Get n most recent posts to any community
curl http://localhost:5000/list_posts/3

# Report the number of up and down votes
curl http://localhost:5000/list_post_votes/2147483647

# List n top-scoring posts
curl http://localhost:5000/list_n_post_votes/5

# Post-identifying list
curl http://localhost:5000/list_post_votes_in_list/Test

################# TESTING DELETE METHODS ###############
# Delete a message
curl -X DELETE http://localhost:5000/delete_message/2147483647

# Delete a post
curl -X DELETE http://localhost:5000/delete_post/2147483647

# Deactivate Account
curl -X DELETE http://localhost:5000/deactivate_account/test_user
