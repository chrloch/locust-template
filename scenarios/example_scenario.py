from vusers.ExampleAppType1User import ExampleAppType1User
from locust import between

# For the sake of an example, we just clone Type1 to make Type2
class ExampleAppType2User(ExampleAppType1User):
    pass

# In this scenario, Type1 users are 3 times as many as Type2 users
ExampleAppType1User.weight = 3
ExampleAppType2User.weight = 1

# We can override wait time in the scenario
ExampleAppType1User.wait_time = between( 2.0, 5.0 )
ExampleAppType2User.wait_time = between( 3.0, 8.0 )