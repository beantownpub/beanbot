import json
import os

from flask import Response, request
from flask_restful import Resource
from api.libs.logging import init_logger

LOG = init_logger(os.environ.get("LOG_LEVEL"))

class TimeoffRequestException(Exception):
    """Base  class for time off request exceptions exceptions"""

foo = ['__annotations__', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__enter__', '__eq__', '__exit__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_cached_json', '_get_file_stream', '_get_stream_for_parsing', '_load_form_data', '_parse_content_type', 'accept_charsets', 'accept_encodings', 'accept_languages', 'accept_mimetypes', 'access_control_request_headers', 'access_control_request_method', 'access_route', 'application', 'args', 'authorization', 'base_url', 'blueprint', 'cache_control', 'charset', 'close', 'content_encoding', 'content_length', 'content_md5', 'content_type', 'cookies', 'data', 'date', 'dict_storage_class', 'disable_data_descriptor', 'encoding_errors', 'endpoint', 'environ', 'files', 'form', 'form_data_parser_class', 'from_values', 'full_path', 'get_data', 'get_json', 'headers', 'host', 'host_url', 'if_match', 'if_modified_since', 'if_none_match', 'if_range', 'if_unmodified_since', 'input_stream', 'is_json', 'is_multiprocess', 'is_multithread', 'is_run_once', 'is_secure', 'json', 'json_module', 'list_storage_class', 'make_form_data_parser', 'max_content_length', 'max_form_memory_size', 'max_forwards', 'method', 'mimetype', 'mimetype_params', 'on_json_loading_failed', 'origin', 'parameter_storage_class', 'path', 'pragma', 'query_string', 'range', 'referrer', 'remote_addr', 'remote_user', 'root_path', 'root_url', 'routing_exception', 'scheme', 'script_root', 'server', 'shallow', 'stream', 'trusted_hosts', 'url', 'url_charset', 'url_root', 'url_rule', 'user_agent', 'user_agent_class', 'values', 'view_args', 'want_form_data_parsed']
class TimeoffRequestAPI(Resource):

    def post(self):
        LOG.info(request.method)
        LOG.info(request.data)
        LOG.info(request.headers)
        time_off_request = request.get_data()
        LOG.info(time_off_request)
        version = {"app": "beanbot", "version": "0.1.1"}
        return Response(version, mimetype="application/json", status=200)
