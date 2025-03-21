**Compare My Biometrics**
-----------------------
**Goals**:
- My fitbit wellness report is broken
- Visualize changes in biometrics between timeframes and learn the health impact of life changes
	- ADHD meds
	- moving
	- exercising
- Practice tech involved the DataTalks bootcamp

**Constraints**:
- Fits in my DataTalks.club Data Engineering Course Schedule
	- meetings with real clients and and gathering data for a novel project can balloon out the time commitment

Result - [Looker Studio Data Presentation](https://lookerstudio.google.com/reporting/08b71d97-dc73-4d66-a694-e027c0d68330)

PLACE HOLDER INFORMATION BELOW
---
Installation
----------------------
### Clone this repo to your computer.
### Download the data
* Download data files into a "data" folder 
    * create an account at [insert_website.com](http://www.insert_website.com)
    * You can find data_file1 at [this link](http://google.com).
    * You can find data_file2 at [this link](http://google.com).
* Extract all of the `.zip` files you downloaded.
    * On OSX, you can run `find ./ -name \*.zip -exec unzip {} \;`.
    * At the end, you should have a bunch of text files called `Acquisition_YQX.txt`, and `Performance_YQX.txt`, where `Y` is a year, and `X` is a number from `1` to `4`.
* delete all the '.zip' files

### Setup
- Clone this Repo
- dev.fitbit.com > Manage > [Register An App](https://dev.fitbit.com/apps/new/) > [Log in](https://dev.fitbit.com/login)
	- `Continue with Google` if you use your google account
	- **IMPORTANT**: the project `Personal` and using Callback URL `http://127.0.0.1:8080/`
- [example image](https://miro.medium.com/v2/resize:fit:720/format:webp/1*UJHMOYsFZvrBmpNjFfpBJA.jpeg)
- insert the sensitive fitbit API tokens into the `fitbit_tokens.json` file in `airflow-gcp/dags`
- `pip install fitbit`
- run gather_keys script in the a
 	- stores your fitbit authentication tokens locally (in fitbit_tokens.json) 
  	- allows your data to be downloaded for analysis
   	- it may need to be rerun later when your access token expires
  - 	- 
- run download_data script
- run format_to_parquet script

Settings
--------------------

Look in `settings.py` for the configuration options.
Configuration Option Overview:

* `EXAMPLE_CONFIG0` -- config description
* `EXAMPLE_CONFIG1` -- config description
* `EXAMPLE_CONFIG2` -- config description

Private Settings
--------------------
* Create a file named `private.py` in this folder.
    * Add a value named `PRIVATE_TOKEN_EG`
    * Assign your API token to it.

Usage
-----------------------

* Run `mkdir processed` to create a directory for our processed datasets.
* Run `python assemble.py` to combine the `Acquisition` and `Performance` datasets.
    * This will create `Acquisition.txt` and `Performance.txt` in the `processed` folder.
* Run `python annotate.py`.
    * This will create training data from `Acquisition.txt` and `Performance.txt`.
    * It will add a file called `train.csv` to the `processed` folder.
* Run `python predict.py`.
    * This will run cross validation across the training set, and print the accuracy score.

- Run gather tokens script in 

Extending this
-------------------------

If you want to extend this work, here are a few places to start:

* Generate more features in `annotate.py`.
* Switch algorithms in `predict.py`.
* Add in a way to make predictions on future data.
* Try seeing if you can predict if a bank should have issued the loan.
    * Remove any columns from `train` that the bank wouldn't have known at the time of issuing the loan.
        * Some columns are known when Fannie Mae bought the loan, but not before
    * Make predictions.
* Explore seeing if you can predict columns other than `foreclosure_status`.
    * Can you predict how much the property will be worth at sale time?
* Explore the nuances between performance updates.
    * Can you predict how many times the borrower will be late on payments?
    * Can you map out the typical loan lifecycle?

---
