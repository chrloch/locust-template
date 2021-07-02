
from locust import User
from locust.env import Environment
import time
import json
import logging

class ProfileBasedUser(User):
    """ A user class that uses the mandatory host string as a profile name. 
        Profiles are JSON files that may contain several hosts and additional settings.
    """
    abstract = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.profile = json.load( open('profiles/'+self.host+'.json'))


class StepStructuredUser(User):
    """A user class that adds features to structure its tasks in logical steps. 
       Every step is preceded by a wait_time.
    """
    abstract = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.log = logging.getLogger(self.__class__.__name__)


    def step( self, logical_name, step_function,  *args, **kwargs):
        """Wrap a function call as a logical test step and precede with think time.

        Positional arguments: 
        - logical_name  : Name of the test case step
        - step_function : the function to call. *args, **kwargs will be passed to it

        Returns the return value of the function that has been wrapped
        """
        
        time.sleep( self.wait_time() )

        self.log.info( f'BEGIN STEP {step_function.__name__}' )
        start_time = time.time()
        result = None
        try:
            result = step_function(*args, **kwargs)
            duration = time.time() - start_time
            self.log.info(f'LEAVING STEP {logical_name}, duration {duration:3f}s')
            self.environment.events.request_success.fire(request_type='Step', name=logical_name, response_time=duration*1000, response_length=0)
        except Exception as ex:
            duration = time.time() - start_time
            self.log.error(f'FAILED STEP {logical_name} after {duration:.3f}s')
            self.environment.events.request_failure.fire(request_type='Step', name=logical_name, response_time=duration*1000, response_length=0, exception=ex)
            self.log.error(f'EXCEPTION: {ex}')
        return result

def get_try_script_instance(user_class, host):
    """Creates an instance of the user class ready for a try-script-test"""
    try:
        import coloredlogs
        coloredlogs.install()
    except:
        pass # If we don't have colored logs, it's not important

    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')

    env = Environment(user_classes=[user_class])
    user_class.host = host
    user_class.is_tryscript = True
    return user_class(env)

