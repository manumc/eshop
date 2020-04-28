# eshop #

This challenge is a simplified analytics component for an e-commerce site.

## Dependencies ##

This project uses Poetry tool for dependecy management and packaging.

It is assumed that:

  * `python3` is already installed in the system. Otherwise, you can find more information at [python.org](https://www.python.org/)
  * your system is Linux or macOS based.

To install Poetry tool in your system just execute:
``` shell
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
```

<!-- For powershell based systems use: -->
<!-- ``` powershell -->
<!-- (Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python -->
<!-- ``` -->

## How to ... ##

### Download the project ###

``` shell
cd ~
git clone https://github.com/manumc/eshop.git
cd ~/eshop
poetry install
```

### Run the service ###

``` shell
cd ~/eshop
poetry shell
sh run.sh
```
Follow the steps above to run the server and the service. It will run it on `http://0.0.0.0:5050` where a "Hello world" message will welcome the user.

To access the API `http://0.0.0.0:5050/api/v1/report?date=2020-10-08`

You can play with it modifying `date` value.

<!-- http://0.0.0.0:5050/api/v1/report?date=2020-10-08 -->

### Run the tests ###

``` shell
cd ~/eshop
poetry shell
pytest -v ./tests
```

[Property based testing](https://hypothesis.works/articles/what-is-property-based-testing/) has been applied to cover a wider range of test cases. You can find more information here: [hypothesis.works](https://hypothesis.works/)
