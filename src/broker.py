from dishka.integrations.faststream import setup_dishka
from faststream import FastStream
from faststream.rabbit import RabbitBroker

from src.infrastructure.broker.consumers.product import rmq_product_router
from src.main import config, container

broker = RabbitBroker(url=config.rabbitmq.rmq_url)
app = FastStream(broker)
broker.include_routers(rmq_product_router)

setup_dishka(container, app)
