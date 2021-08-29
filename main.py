import requests
from datetime import datetime
import pytz
import smtplib
import time

MY_LAT = 37.566536  # Your latitude
MY_LONG = 126.977966  # Your longitude
MY_EMAIL = "test@gmail.com"
MY_PASSWORD = "abcd1234"

parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}


def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    if MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LONG - 5 <= iss_longitude <= MY_LONG + 5:
        return True


def is_night():
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()

    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    # time_now_utc = datetime.now().astimezone(pytz.timezone("utc")).strftime("%d-%b-%Y %H:%M:%S.%f")
    # time_now_hour = int(time_now_utc.split(" ")[1].split(":")[0])

    # SIMPLER WAY:
    time_now_utc = datetime.now().astimezone(pytz.timezone("utc")).hour

    if sunset <= time_now_utc <= sunrise:
        return True


while True:
    time.sleep(60)
    if is_iss_overhead() and is_night():
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(MY_EMAIL, MY_PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=MY_EMAIL,
                msg="Subject=Look in the sky!\n\nTHE ISS IS IN THE SKY"
            )