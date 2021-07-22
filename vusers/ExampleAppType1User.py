from vusers.ExampleAppUser import ExampleAppUser
from vusers.GenericUsers import get_try_script_instance
from locust import task, between

class ExampleAppType1User(ExampleAppUser):
    """ Example of a projects virtual user class.
        This class represents a user type, something like BackendOfficeUser, CustomerUser, ReportingUser etc.
    """

    @task
    def test_case_1(self):
        self.step("TC1_01 Go to my folder", self.step_go_to_my_folder )             # A step defined in base class
        self.step("TC1_02 Upload a PDF", self.step_upload_file, "sample-pdf.pdf" )  # A step defined in local class
        self.step("TC1_03 Close View", self.step_close_view )


    @task
    def test_case_2(self):
        self.step("TC2_01 Go to my folder", self.step_go_to_my_folder )
        self.step("TC2_02 Upload small image", self.step_upload_file, "sample-pic-1mb.jpeg" )
        self.step("TC2_03 Upload large image", self.step_upload_file, "sample-pic-10mb.jpeg" )
        self.step("TC2_04 View Thumbnails" , self.step_view_thumbs )
        self.step("TC2_05 Close View", self.step_close_view )

# ----- Step definitions -----

# The steps that are defined here are unique to this user type
# Common types are inherited from the base class.

    def step_view_thumbs(self):
        self.log.info('Viewing thumbnails')
        # Code goes here

    def step_upload_file(self, filename):
        self.log.info(f'Uploading {filename}')
        # Code goes here

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


def try_script():
    user = get_try_script_instance(ExampleAppType1User, 'ExampleProfile' ) 
    
    # For try-script runs, test data servers are usually not active and we can simply override the test
    # data for our try-script instance
    user.test_data = {"username":"appuser1", "password":input("Enter password: ")}

    # Run the test cases
    user.on_start()
    user.test_case_1()
    user.test_case_2()


if __name__=="__main__": 
    try_script()
