# locust-template

A template project for load tests based on the Locust Python framework.

## Abstract

When load testing in complex projects, there is often more than one host involved
in the same test run. Likewise, there are multiple test stages or acceptance 
environments. Sometimes, results have to be reported in a kind of business view
rather than a technical view. So the number of calls to an endpoint may not be 
a value that is understood but the number of business process executions may be
requested. 

Many load testing tools, especially commercial ones, have a support for this kind
of requirements built in - with all the advantages and disadvantages of such an 
approach. 

Instead of aiming for a feature-itis infested version of Locust, this project aims
to provide a project template that shows how additional features can be 
implemented on project level and which can be extended as needed by those who
are actually involved with the testing. 

## Folder structuce

The structure of the template is a suggestion. You may add or remove folders as 
it suits your project. Some people may, for example, want to add a pytest suite
and have it use the same implementation of test case steps that the Locust virtual
users do. 

As for this example, the structure is as follows:

* `vusers` contains virtual user definitions. These are typically classes
    that define *what* a virtual user does. It also contains some generic
    user types from which your actual user types can inherit features. 
* `scenarios` holds the main locust files for each test execution. You will 
    probably always start your load test with somthing like this: 
    ```
    locust -f scenarios/my_scenario.py
    ```
    The scenario typically defines the ratio of different user types in the
    test execution.
* `profiles` is used here for something that breaks with the original concept of 
    Locust having all behavior defined by Python code (and not declarative domain
    language), but I found it particulary useful especially in larger projects.

    Don't worry though: It is completely optional to use. 

    When your virtual user class inherits from GenericUsers.ProfileBasedUser, then
    the ``host``-field no longer expects to hold an URL but the name of a profile
    file, which can define different parameters. 


## Writing VUsers

This template project is optimized for using inheritance to structure
virtual user files.

Instead of working with TaskSets, I prefer to use inheritance because that makes 
it easier to make users share use case logic that consists of more than simple 
sequences of requests. 

A typical class tree without using any of the template's 
generic classes could look like this: 

```
  locust.User
     |
     +---locust.HttpUser
     |      |
     |      +---YourProjectWebUser            (common methods, like login, logout)
     |             |
     |             +YourProjectType1User      (individual tasks)
     |             |
     |             +YourProjectType2User      (individual tasks)
     |
     +---YourProjectSqlUser
            |
            +---YourProjectType3User          (non-HTTP use cases)
```


Using generic classes from the template project and multiple inheritance
```
  locust.User
     |
     +---locust.HttpUser                   ]
     |                                     |
     +---GenericUsers.ProfileBasedUser     ]---+
     |                                     |   |
     +---GenericUsers.StepStructuredUser   ]   |
                                               |
               +-------------------------------+
               |
            YourProjectWebUser               (Example: ExampleAppUser.py)
               |
               +---YourProjectType1User      (Example: ExampleAppType1User.py)
               |
               +---YourProjectType2User   

```
## The generic user classes

* ``ProfileBasedUser`` replaces the host field with a profile name. Expects the
    profile to be located in the ``profiles`` folder and following the naming
    scheme ``f"{profileName}.json"`` 
* ``StepStructuredUser`` adds features to structure its tasks in logical steps. 
    Every step is preceded by a wait_time.
* ``TryScriptAwareUser`` allows to change behavior depending on whether a user
    is running in try script mode or not. Ideally you should not need this.

## Working with profiles

As soon as your project has endpoints on more than one server, you will notice
that one host field is not enough. However, the idea to specify the environment 
against which a test is to be executed in a simple dialog like in Locust, is 
pretty handy when you are working on staged environments. 

When you work with profile based users, you can define your environments in JSON
files, e.g. 
 - ``DevFrontend.json``
 - ``DevBackend.json`` 
 - ``Integration.json``
 - ``PreProd.json`` 

and so on. When running a test, the environment name, e.g. ``Integration`` goes 
into the host field and all the hosts which are configured for the environment
are available to your virtual user. 

You can put any setting or variable that you want into a profile file and even 
when your environment only has one host, it may still be useful to change the 
meaning of t he host field to profile for your purpose. 

Profiles always affect a test as a whole. It is not possible to run a test 
with 40% Profile1 and 60% Profile2. Settings that differ between two groups
of virtual users can be made in the scenario file. 

## Writing scenarios

A scenario file is just another name for a locustfile. I've still chosen to 
name it differently, because a virtual user file is technically a locustfile too. 

There are only two things that need to be done in a scenario file:
1. import all user classes that are part of the scenario
2. assign a weight attribute to them

The weight is applied to the total number of users that you spawn in the test.
so if you have `UserType1.weight = 1` and `UserType2.weight = 3`, a test with
100 VUsers will have 25 Type1 and 75 Type2 users.

### Additional settings in the scenario

You can override a virtual user's wait time in the scenario. This is very
useful when you have both a stress test scenario and a load test scenario. 

If your user's behavior is based on some probability values, it's a good idea
to put the limits in a class variable that can be overridenn in a profile.
With this, you can have scenarios with different likeliness of a certain 
user behavior.







