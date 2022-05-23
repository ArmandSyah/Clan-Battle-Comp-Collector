# CBCC-Data-Extractor (Muimi)

Basically, this program is a pipeline that will read all the required data from the current latest priconne database info, in order to retrieve characters and clan battle boss info and then push that data into the database controlled by the Rest api.

If you're interested in running the entire CBCC project locally, you will need to configure and run this data extractor

## Requirements
- Python3 (3.8 or lower. Any higher and then errors will occur when trying to install some of the dependencies listed in the requirements.txt)
- AWS - the images that are pulled from the game (character icons, boss icons) get stored into an AWS S3 bucket. For this pipeline to work, make sure to have the following set up: 
  - Make sure to have an S3 bucket set up. Make sure in this bucket that you don't block public access, otherwise the ui won't be able to display the images. Keep note of the name of the bucket, as well as it's AWS region
  - Set up an IAM user with and give it permissions to read the S3 bucket you previously set up. Then set up an access key for this user
- (Optional) API Keys for Microsoft Translate, DeepL and Yandex. 
  - The translation service for the pipeline rotates through multiple translation service in case one fails or the limit has been hit

## Instructions
1. Rename the `config.ini.example` file to `config.ini`
  - Under the `[aws]` section of the config, put in your aws bucket name and aws region name in the respective fields
  - In the `[usedtranslationapis]` section, set each of those translate variables to either `true` or `false` depending on which of the services you wish to use.
    - Do note that Microsoft Translate, DeepL and Yandex will require API keys, so set these to false if you don't have an api key on hand for any of these services
    - Make sure that at least one of these services is set to true, otherwise piepline will fail
  - Do not touch any of the other fields in the config.ini file
2. Make sure you have your aws access keys set as environment variables in your system. In addition, if you are using the translation services that requires API keys, make sure to set those api keys as environment variables in the following manner
```
## Unix
export MICROSOFT_API_KEY=<Microsoft Translate key>
export YANDEX_API_KEY=<Yandex key>
export DEEPL_API_KEY=<DeepL key>

## Windows
set MICROSOFT_API_KEY=<Microsoft Translate key>
set YANDEX_API_KEY=<Yandex key>
set DEEPL_API_KEY=<DeepL key>
```  
3. Create the virtual environment, activate it and then install all required libraries
```
## Create the virtual environment
pip install virtualenv # install this package if you haven't done it yet
virtualenv --python 3.8 venv

## Activate the virtual environment

## unix
source venv/bin/activate

## windows
venv\Scripts\activate

## install the python packages
pip install -r requirements.txt
```
4. Now you can run the pipeline via the command line. There are two ways to do this:
- `python -m start init` - This will run the start script with the `init` flag enabled. With the flag enabled, the intermediate json files stored before sending game data to our db gets deleted, and the process of game data retrieval starts fresh. Use this command to seed a database that is empty (has no character, boss or clan battle schedule info)
- `python -m start` - Without the init flag, characters that have been retrieved will get checked for updated information, any new charactrers are added to the json files and any new boss data or clan battle schedule data is retrieved. Use this command to update your backend if it has already been seeded previously.