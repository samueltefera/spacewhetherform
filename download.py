from json import load
from unicodedata import name
from downloadClass import SessionWithHeaderRedirection
import requests
import os
import patoolib
import datetime
from dotenv import load_dotenv
load_dotenv()
current_date = datetime.date.today()

year = str(current_date.year)
year_ext = year[-2:]

day_of_year = str(current_date.timetuple().tm_yday)

# create session with the user credentials that will be used to authenticate access to the data

username = os.getenv('USER_NAME')
password= os.getenv('password')

session = SessionWithHeaderRedirection(username, password)


# the url of the file we wish to retrieve

#url = "https://cddis.nasa.gov/archive/gnss/products/ionex/2022/193/"

url = r"https://cddis.nasa.gov/archive/gnss/products/ionex/2022/" + day_of_year +r"/c2pg" + day_of_year+r"0."+ year_ext+r"i.Z"

# extract the filename from the url to be used when saving the file

filename = url[url.rfind('/')+1:]  

print(filename)

def download():
    global filename, url,session
    try:

        # submit the request using the session

        response = session.get(url, stream=True)

        print(response.status_code)



        # raise an exception in case of http errors

        response.raise_for_status()  



        # save the file
        TEC_fil = os.getcwd() + '\\TECfile\\' + filename
        TEC_fil_ = os.getcwd() + '\\TECfile\\'
        with open(TEC_fil, 'wb') as fd:

            for chunk in response.iter_content(chunk_size=1024*1024):

                fd.write(chunk)



    except requests.exceptions.HTTPError as e:

        # handle any errors here

        print(e)

    

    patoolib.extract_archive(TEC_fil,outdir=os.getcwd() + '\\TECfile\\')
    os.getcwd()
    return True
    