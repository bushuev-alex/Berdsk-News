from celery import shared_task
import logging
import subprocess
import json
import os
# from .schemas import SpiderOrigin, UserName

# logger = logging.getLogger('app')
from dotenv import load_dotenv

load_dotenv()

SPIDER_NAMES = json.loads(os.getenv('SPIDER_NAMES'))
PARSER_CWD = os.getenv('PARSER_CWD')



@shared_task()
def launch_spider(origin: str):
    spidername = SPIDER_NAMES.get(origin)
    print(spidername)
    # spidername = origin.__dict__.get("parsed_from").__dict__.get("_name_")
    try:
        # logger.info(f"Try to launch spider {spidername} ")
        proc_result = subprocess.run([f"curl",
                                      f"http://localhost:6800/schedule.json",
                                      f"-d",
                                      f"project=parser",
                                      f"-d",
                                      f"spider={spidername}",
                                      ], stdout=subprocess.PIPE,
                                     cwd=PARSER_CWD)
        print(proc_result)
        params = json.loads(proc_result.stdout)
        print(params)
        job_id = params["jobid"]
        # logger.info(f"Spider {spidername} is launched with params = {params}")
        print("OK", "Please, wait while parser is working. JobID: ", job_id)
        return job_id
    except Exception as e:
        print(e)
        # logger.debug(e)
        return {"status": "error",
                "data": e,
                "details": e}
