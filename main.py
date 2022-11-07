from datetime import datetime
from mapping import QueryAPI
import pandas as pd
import logging
import time


if __name__ == '__main__':
    # Initializing logging
    logging.basicConfig(level=logging.INFO)

    run_time = time.time()
    logging.info(f"{datetime.now()} : Running...")

    # Getting the data
    data = QueryAPI().get_data()

    # Saving it to a file to do some data visualization later on
    try:
        data.to_csv('data.csv')
        logging.info('Successfully saved the queried data')
    except Exception as e:
        logging.error(f"Couldn't save the data : {e}")
    finally:
        logging.info(f"{datetime.now()} : Done running with total execution time {round(time.time() - run_time, 2)}s")
