from .time_off_requests import TimeoffRequestAPI
from .healthcheck import HealthCheckAPI


def init_routes(api):
    api.add_resource(TimeoffRequestAPI, "/v1/beanbot/slack")
    api.add_resource(HealthCheckAPI, "/v1/beanbot/healthz")
