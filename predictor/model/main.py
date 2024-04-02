import pandas as pd
from prophet import Prophet
import datetime
import requests
import os


def get_hunt_data(api_host: str, api_port: str):
    url = f"http://{api_host}:{api_port}/api/hunt"
    res = requests.get(url)
    if res.status_code != 200:
        raise Exception(res.text)
    df = pd.json_normalize(res.json()["result"])
    return df


def get_hill_data(api_host: str, api_port: str):
    url = f"http://{api_host}:{api_port}/api/hill"
    res = requests.get(url)
    if res.status_code != 200:
        raise Exception(res.text)
    df = pd.json_normalize(res.json()["result"])
    return df


def generate_model(df: pd.DataFrame):
    # parse the necessary dataframe columns
    record_datetimes = pd.to_datetime(df["record_datetime"])
    total_percents = pd.to_numeric(df["total_percent"])
    data = {
        "ds": record_datetimes,
        "y": total_percents
    }
    # create a new dataframe with only the parsed required columns
    df = pd.DataFrame(data=data)
    # remove timezone, since data with timezones are not supported by prophet
    df["ds"] = df["ds"].dt.tz_localize(None)

    # initialize a new prophet model
    model = Prophet()
    # fit the prophet model based on the inputted data
    model.fit(df)
    return model


def make_predictions(model: Prophet):
    start = datetime.datetime.now(datetime.timezone.utc).date()
    delta = datetime.timedelta(days=7)
    end = start + delta

    daterange = pd.date_range(start=start, end=end, freq="30min")

    df = pd.DataFrame(data={"ds": daterange})

    future = model.predict(df)

    future.loc[future["yhat"] < 0, "yhat"] = 0
    future.loc[future["yhat_lower"] < 0, "yhat_lower"] = 0
    future.loc[future["yhat_upper"] < 0, "yhat_upper"] = 0

    return future


def predictions_to_json(predictions: pd.DataFrame):
    predictions_json = []
    for (_index, row) in predictions.iterrows():
        obj = {
            "record_datetime": row["ds"].to_pydatetime().isoformat(),
            "predictions": {
                "total_percent": row["yhat"],
                "total_percent_lower": row["yhat_lower"],
                "total_percent_upper": row["yhat_upper"]
            }
        }
        predictions_json.append(obj)
    return predictions_json


def save_hunt_predictions(predictions_json, api_host: str, api_port: str):
    url = f"http://{api_host}:{api_port}/api/hunt/predictions"
    res = requests.post(url, json=predictions_json)
    if res.status_code != 200:
        raise Exception(res.json())


def save_hill_predictions(predictions_json, api_host: str, api_port: str):
    url = f"http://{api_host}:{api_port}/api/hill/predictions"
    res = requests.post(url, json=predictions_json)
    if res.status_code != 200:
        raise Exception(res.json())


if __name__ == "__main__":
    api_host = os.getenv("API_HOST")
    if api_host is None:
        raise KeyError("environment variable API_HOST not set")

    api_port = os.getenv("API_PORT")
    if api_port is None:
        raise KeyError("environment variable API_PORT not set")

    hunt_data = get_hunt_data(api_host, api_port)
    hunt_model = generate_model(hunt_data)
    hunt_predictions = make_predictions(hunt_model)
    hunt_predictions = predictions_to_json(hunt_predictions)
    save_hunt_predictions(hunt_predictions, api_host, api_port)

    hill_data = get_hill_data(api_host, api_port)
    hill_model = generate_model(hill_data)
    hill_predictions = make_predictions(hill_model)
    hill_predictions = predictions_to_json(hill_predictions)
    save_hill_predictions(hill_predictions, api_host, api_port)
