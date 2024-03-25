import asyncio
import os
import time
from time import localtime, strftime
from typing import Coroutine

import geojson
import geopandas as gpd
import httpx as httpx
import plotly.io as pio

from oqapi_config import (
    HEADERS,
    INPUTDIR,
    INPUTFILES,
    NO_OF_RETRIES,
    NO_PARALLEL_REQUESTS,
    PLOTDIR,
    OQAPIURLINDICATOR,
    TOPIC,
)


def import_boundary(infile, inputdir) -> gpd.GeoDataFrame:
    """Import the boundary file and return a GeoDataFrame."""
    if infile is not None:
        path_to_file = os.path.join(inputdir, infile)
        df = gpd.read_file(path_to_file)

        if df.crs != 4326:
            df = df.to_crs(4326)

    return df


async def gather_with_semaphore(tasks: list, *args, **kwargs) -> Coroutine:
    """A wrapper around `gather` to limit the number of tasks executed at a time."""
    # Semaphore needs to be initiated inside the event loop
    semaphore = asyncio.Semaphore(NO_PARALLEL_REQUESTS)

    async def sem_task(task):
        async with semaphore:
            return await task

    return await asyncio.gather(*(sem_task(task) for task in tasks), *args, **kwargs)


async def get_indicators(feature, index, regionname) -> tuple:
    """Get the indicator for the given feature and retry if unsuccessful."""
    print(f"\t\tCalculating Index for Region {regionname}, Feature {index}")
    bpolys = geojson.FeatureCollection(
        [geojson.Feature(geometry=feature.geometry[index])]
    )
    for tryno in range(NO_OF_RETRIES):
        try:
            result = await query_indicator(bpolys)
            ind_value = result[0]["result"]["value"]
            ind_class = result[0]["result"]["class"]
            ind_figure = result[0]["result"]["figure"]
        except httpx.TimeoutException as err:
            if tryno < NO_OF_RETRIES - 1:
                print(
                    f"\nAn error occured: File {regionname}, Index {index}. Retrying to Calculate"
                )
                # wait 10 seconds before retrying
                time.sleep(10)
                continue
            else:
                print(
                    f"\nAn error occured: File {regionname}, Index {index}, error type: {type(err)}\n"
                )
                raise
        except httpx.HTTPError as err:
            if tryno < NO_OF_RETRIES - 1:
                print(
                    f"\nAn error occured: File {regionname}, Index {index}. Retrying to Calculate"
                )
                # wait 10 seconds before retrying
                time.sleep(10)
                continue
            else:
                print(
                    f"\nAn error occured: File {regionname}, Index {index}, error message: {err.response.text}\n"
                )
                raise
        break

    return ind_value, ind_class, ind_figure


async def query_indicator(bpolys) -> dict:
    """Query the indicator for the given boundary."""
    parameters = {
        "topic": TOPIC,
        "bpolys": bpolys,
    }
    async with httpx.AsyncClient(timeout=httpx.Timeout(300, read=660)) as client:
        response = await client.post(
            OQAPIURLINDICATOR, headers=HEADERS, json=parameters
        )
    response.raise_for_status()
    result = response.json()["result"]

    return result


def save_figure(figure, index, regionname) -> None:
    """Save the mapping saturation figure to a file."""
    datapath = os.path.join(
        PLOTDIR,
        (regionname + "_mapping-saturation-plot" + "_feature_" + str(index) + ".png"),
    )
    if not os.path.exists(PLOTDIR):
        os.makedirs(PLOTDIR)

    pio.write_image(figure, datapath, format="png")


async def main():
    start_time = time.time()

    if len(INPUTFILES) == 0:
        for filename in os.listdir(INPUTDIR):
            INPUTFILES.append(filename)

    # set counter of files to process in order to track progress
    count_files_done = 0

    for region in INPUTFILES:
        print(f"Working on file {count_files_done + 1} of {len(INPUTFILES)}")
        errorlog = []

        regionname = region.split(".")[0]

        all_features = import_boundary(region, INPUTDIR)
        all_features["map_sat_value"] = None
        all_features["map_sat_class"] = None

        # create tasklist
        tasks = []
        print(f"\tCalculating Indicator for {len(all_features)} Features.")
        for index in all_features.index:
            row = all_features.loc[[index]]
            # create tasks for all Indicators to create
            tasks.append(get_indicators(row, index, regionname))

        # await the result for all food reports
        tasks_results = await gather_with_semaphore(tasks, return_exceptions=True)

        # write Indicator result to each feature
        for index, result in enumerate(tasks_results):
            if isinstance(result, Exception):
                message = getattr(result, "message", repr(result))
                print(
                    f"\nAn error occured: File {regionname}, Index {index}, error message: {message}"
                )
                errorlog.append([regionname, f"Index {index}", message])
            else:
                all_features.at[index, "map_sat_value"] = result[0]
                all_features.at[index, "map_sat_class"] = result[1]
                # save_figure(result[2], index, regionname)
                save_figure(result[2], all_features.at[index, "SOV_A3"], regionname)

        if len(errorlog) == 0:
            print("\tNo errors occured.")
        else:
            print(f"\n{len(errorlog)} errors occured! \n\n {errorlog}")
            errorlog_path = os.path.join(
                INPUTDIR + f"ErrorLog_Mapping-Saturation_{regionname}.txt"
            )
            with open(errorlog_path, "w") as file:
                for item in errorlog:
                    # write each item on a new line
                    file.write("%s\n" % item)

        resultname = os.path.join(
            INPUTDIR, (regionname + "_Mapping-Saturation" + ".geojson")
        )
        with open(resultname, "w") as f:
            f.write(all_features.to_json())

        count_files_done += 1

    if len(INPUTFILES) == 1:
        print("File saved. Done!")
    else:
        print("Files saved. Done!")

    end_time = time.time()
    print(
        f"Ended at {strftime('%Y-%m-%d %H:%M:%S', localtime(end_time))}. Runtime: "
        f"{(end_time - start_time) / 60} minutes"
    )


if __name__ == "__main__":
    asyncio.run(main())
