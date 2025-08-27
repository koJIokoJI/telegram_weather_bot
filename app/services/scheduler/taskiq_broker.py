import logging

from taskiq import TaskiqScheduler, TaskiqEvents, TaskiqState
from taskiq_nats import NatsBroker
from taskiq.schedule_sources import LabelScheduleSource
from taskiq_redis import RedisScheduleSource

from config.config import settings

broker = NatsBroker(servers=settings.nats_servers, queue="mailint_weather_queue")
redis_source = RedisScheduleSource(
    url=f"redis://{settings.redis_host}:{settings.redis_port}"
)
scheduler = TaskiqScheduler(
    broker=broker, sources=[redis_source, LabelScheduleSource(broker)]
)


@broker.on_event(TaskiqEvents.WORKER_STARTUP)
async def startup(state: TaskiqState):
    logging.basicConfig(level=settings.logs.level, format=settings.logs.format)
    logger = logging.getLogger(__name__)
    logger.info("Scheduler started")
    state.logger = logger


@broker.on_event(TaskiqEvents.WORKER_SHUTDOWN)
async def shutdown(state: TaskiqState):
    state.logger.info("Scheduler stopped")
