from threading import Thread

from src.utility.logger import logger
from src.processor import start_processor
from src.conf import properties_eu, properties_usa
from src import constants as c
from src.conf import properties_mongo as pm
from src.utility.mongo_db import MongoDB


mongo_db = MongoDB(pm.db_con_usa, "M-HH")

conf_col = mongo_db.get_collection("config")

conf = conf_col.find_one({}, {'_id': False})


for unit_name, unit_conf in conf["units"].items():
    for topic_type, topic in unit_conf["topics"].items():
        Thread(target=start_processor, args=(
            unit_conf, [topic], mongo_db, topic_type)).start()
        logger.info(
            f'Started {topic_type} processor thread for {unit_conf["label"]}. Consuming Topic: {topic}')
