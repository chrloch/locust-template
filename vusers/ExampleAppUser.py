from vusers.GenericUsers import ProfileBasedUser, StepStructuredUser
from locust import HttpUser, between
from bs4 import BeautifulSoup
import requests 

class ExampleAppUser(ProfileBasedUser, StepStructuredUser, HttpUser):
    """ Example of a project's virtual user base class: 
        Things, that all your virtual users have in common should go here. 

        In this example, our application is a browser app, therefore we inherit from HttpUser 
        and also add a method to our simulation base class that makes use of 
        BeautifulSoup for HTML parsing. 

        There's also an example of how to use a test data server. If different user types use
        different test data, that snippet could also call a method that is to be implemented
        by the user  type class. 
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.test_data = None


    def on_start(self):      
        # Loading test data when the user starts, so that it is queried from test data server
        # upon arrival of users.
        if self.test_data is None and "test-data-server" in self.profile["hosts"]: 
            response = requests.get( f'{self.profile["hosts"]["test-data-server"]}/bucket/accounts')
            #self.test_data = response.json()

        self.step( "TC0_01 Login", self.step_login )


    def parse(self, html, mode='html.parser'):  # We will use this as shown below in the step definition
        """ Returns a BeautifulSoup object from the given text. 
            mode may be \'html.parser\' or \'xml\' for example"""
        return BeautifulSoup(html, features=mode)

# ----- Step definitions -----

# The steps that are defined here exist in multiple user types and they will inherit them 

    def step_login(self):
        # Go to login page
        response = self.client.get(f'{self.profile["hosts"]["my-app-server"]}/')
        page = self.parse(response.text) 
        # The call to self.parse is explicit, because depending on the call we make, we could as well get a JSON doc
        # or other data structure

        self.requesttoken = page.head.attrs['data-requesttoken']
        self.log.info(f'REQUESTTOKEN {self.requesttoken}')

        # Login with username & password
        loginform = {
            'user':             self.test_data['username'],
            'password':         self.test_data['password'],
            'requesttoken':     self.requesttoken
        }
        response = self.client.post(f'{self.profile["hosts"]["my-sso-server"]}/login', data=loginform )
        self.logStatus( response, cookies=True )        
        assert response.ok

    def step_go_to_my_folder(self):
        self.log.info('Going to my folder')

    def step_close_view(self):
        self.log.info('Closing the view')
