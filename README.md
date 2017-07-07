# Quasar

## DoSomething.Org Data Platform

### Extended Description 

* All Infrastructure Tools and Code
* All ETL Code and Scripts
* Data Warehousing Code
* A Bright Light and Hope towards illuminating the dark corners of social injustice with the power of Data

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

These instructions use`pyenv` to isolate project dependencies in a lightweight virtual environment. You can also use `pythonz` or any other Python environment manager you prefer.

Install pyenv:

```
sudo apt-get install python3-venv
mkdir ~/.pyenvs
cd ~/.pyenvs
```

Set up environment directory for quasar:

```
pyvenv quasar
source quasar/bin/activate
```

You should now see the environment name prefixing your command line. Check Python and `pip` versions:

```
(quasar) xianny@machine ~/.pyenvs $
(quasar) xianny@machine ~/.pyenvs $ python --version
Python 3.5.2
(quasar) xianny@machine ~/.pyenvs $ pip --version
pip 9.0.1 from /home/xianny/.pyenvs/quasar/lib/python3.5/site-packages (python 3.5)
(quasar) xianny@machine ~/.pyenvs $ 

```

### Installing

Install Python requirements:

```
cd $QUASAR_PROJECT_DIR/etl-scripts
pip install --user -r requirements.txt
```

If you run into errors, you might need:

```
sudo apt-get install libmysqlclient-dev
sudo apt-get install python3-dev
```

Start the vagrant machine. It runs MySQL:

```
vagrant up
```

### Development

Run this everytime:

```
cd $QUASAR_PROJECT_DIR
source ~/.pyenvs/quasar/bin/activate
```

## Usage

???

## Running the tests

None yet. Let's add automated tests!

### End to end tests

### Coding style tests

### Unit tests

## Deployment

## Built With

[SPECIFICATIONS.md](SPECIFICATIONS.md)

## Contributing

[CONTRIBUTING.md](CONTRIBUTING.md) // add process notes?  
[Pull request template](PULL_REQUEST_TEMPLATE)  
[Issue template](issue_template.md)  

## Versioning

??

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
