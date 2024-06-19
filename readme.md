## AWS Lambda Templeate

This respository can be used as a starting point to build an AWS lambda project.
It includes a lambda handler with simple examples of:

* Using an api
* Uploading a file to s3
* storing data to a mysql database

It includes basic tests for all of the functionality above, and a packaging tool.
In the "deployment" folder you will find the `build.bat` script which creates a lambda zip file or a zip file of the
dependencies layer.

## Future action items

* Use poetry instead of two requirements files
* Automatically find all relevant source files
* Build a mock database
* Support other OS (mac, linux)
* Support AMD lambda
* Run tests in a docker which simulates the AWS lambda environment