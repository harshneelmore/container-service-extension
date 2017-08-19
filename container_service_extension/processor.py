# container-service-extension
# Copyright (c) 2017 VMware, Inc. All Rights Reserved.
# SPDX-License-Identifier: BSD-2-Clause

from pkg_resources import resource_string
import base64
from cluster import Cluster
from cluster import Node
from cluster import TYPE_MASTER
from container_service_extension.provisioner import Provisioner
import json
import yaml
import logging
import time
import traceback
from threading import Thread
import uuid

LOGGER = logging.getLogger(__name__)

OK = 200
CREATED = 201
ACCEPTED = 202
INTERNAL_SERVER_ERROR = 500

OP_CREATE_CLUSTER = 'CLUSTER_CREATE'
OP_DELETE_CLUSTER = 'CLUSTER_DELETE'


class ServiceProcessor(object):

    def __init__(self, config, verify, log):
        self.config = config
        self.verify = verify
        self.log = log
        self.provisioner = Provisioner(host=config['vcd']['host'],
                                       username=config['vcd']['username'],
                                       password=config['vcd']['password'],
                                       version=config['vcd']['api_version'],
                                       verify=config['vcd']['verify'],
                                       log=config['vcd']['log'])
        self.provisioner.connect_sysadmin()

    def process_request(self, body):
        LOGGER.debug('request body: %s' % json.dumps(body))
        reply = {}
        request_headers = body['headers']
        request_host = request_headers['Host']
        request_vcloud_token = request_headers['x-vcloud-authorization']
        requestUri = body['requestUri']
        request_version = request_headers['Accept'].split('version=')[-1]
        tokens = requestUri.split('/')
        cluster_op = None
        cluster_id = None
        get_swagger_json = False
        get_swagger_yaml = False
        if len(tokens) > 3:
            cluster_id = tokens[3]
            if cluster_id == '':
                cluster_id = None
            if cluster_id == 'swagger.json':
                get_swagger_json = True
                cluster_id = None
            if cluster_id == 'swagger.yaml':
                get_swagger_yaml = True
                cluster_id = None
        if len(tokens) > 4:
            cluster_op = tokens[4]
            if cluster_op == '':
                cluster_op = None
        if len(body['body']) > 0:
            try:
                request_body = json.loads(base64.b64decode(body['body']))
            except:
                request_body = None
        else:
            request_body = None

        tenant_info = self.provisioner.connect_tenant(body)

        request_user_name = tenant_info.get('user_name')
        request_org_name = tenant_info.get('org_name')
        if body['method'] == 'GET':
            if get_swagger_json is True:
                reply = self.get_swagger_json_file()
            elif get_swagger_yaml is True:
                reply = self.get_swagger_yaml_file()
            elif cluster_id is None:
                reply = self.list_clusters()
        elif body['method'] == 'POST':
            if cluster_id is None:
                reply = self.create_cluster(request_body)
        elif body['method'] == 'DELETE':
            reply = self.delete_cluster(request_body, cluster_id)
        LOGGER.debug('---\nid=%s\nmethod=%s\nuser=%s\norg_name=%s\n'
                     'vcloud_token=%s\ncluster_id=%s\ncluster_op=%s' %
                     (body['id'], body['method'], request_user_name,
                      request_org_name, request_vcloud_token, cluster_id,
                      cluster_op))
        LOGGER.debug('request:\n%s' % json.dumps(request_body))
        return reply

    def get_swagger_json_file(self):
        yaml_response = None
        try:
            file_name = resource_string('container_service_extension',
                                        'swagger/swagger.yaml')
            yaml_response = yaml.load(file_name)
        except:
            raise Exception("Swagger file not found: check installation.")
        json_response = json.loads(json.dumps(yaml_response))
        real_response = {}
        real_response['body'] = json_response
        real_response['status_code'] = OK
        return real_response

    def get_swagger_yaml_file(self):
        yaml_response = None
        try:
            file_name = resource_string('container_service_extension',
                                        'swagger/swagger.yaml')
            yaml_response = yaml.load(file_name)
        except:
            raise Exception("Swagger file not found: check installation.")
        real_response = {}
        real_response['body'] = yaml_response
        real_response['status_code'] = OK
        return real_response

    def list_clusters(self):
        result = {}
        clusters = []
        try:
            result['body'] = clusters
            result['status_code'] = OK
        except Exception:
            LOGGER.error(traceback.format_exc())
            result['body'] = []
            result['status_code'] = INTERNAL_SERVER_ERROR
            result['message'] = traceback.format_exc()
        return result

    def create_cluster(self, body):
        result = {}
        result['body'] = {}
        cluster_name = body['name']
        cluster_vdc = body['vdc']
        node_count = body['node_count']
        LOGGER.debug('about to create cluster with %s nodes', node_count)
        result['body'] = 'can''t create cluster'
        result['status_code'] = INTERNAL_SERVER_ERROR
        if not self.provisioner.validate_name(cluster_name):
            result['body'] = {'message': 'name is not valid'}
            return result
        if self.provisioner.search_by_name(cluster_name) is not None:
            result['body'] = {'message': 'cluster already exists'}
            return result
        cluster_id = str(uuid.uuid4())
        try:
            raise Exception({'message': 'not implemented'})
            # task = Task(session=vca_system.vcloud_session,
            #             verify=self.config['vcd']['verify'],
            #             log=self.config['vcd']['log'])
            # operation_description = 'creating cluster %s (%s)' % \
            #     (cluster_name, cluster_id)
            # LOGGER.info(operation_description)
            # status = 'running'
            # details = '{"vdc": "%s"}' % \
            #          (cluster_vdc)
            # create_task = create_or_update_task(task,
            #                                     OP_CREATE_CLUSTER,
            #                                     operation_description,
            #                                     cluster_name,
            #                                     cluster_id,
            #                                     status,
            #                                     details,
            #                                     prov)
            # if create_task is None:
            #     return result
            # response_body = {}
            # response_body['name'] = cluster_name
            # response_body['cluster_id'] = cluster_id
            # response_body['task_id'] = create_task.get_id().split(':')[-1]
            # response_body['status'] = status
            # response_body['progress'] = None
            # result['body'] = response_body
            # result['status_code'] = ACCEPTED
            # thread = Thread(target=self.create_cluster_thread,
            #                 args=(cluster_id,))
            # thread.daemon = True
            # thread.start()
        except Exception as e:
            result['body'] = e.message
            LOGGER.error(traceback.format_exc())
        return result

    def delete_cluster(self, body, cluster_id):
        result = {}
        result['body'] = {}
        LOGGER.debug('about to delete cluster with id: %s', cluster_id)
        result['status_code'] = INTERNAL_SERVER_ERROR
        details = self.provisioner.search_by_id(cluster_id)
        if details is None or details['name'] is None:
            result['body'] = {'message': 'cluster not found'}
            return result
        cluster_name = details['name']
        try:
            raise Exception('not implemented')
        except Exception as e:
            result['body'] = e.message
            LOGGER.error(traceback.format_exc())
            return result

    def create_cluster_thread(self, cluster_id):
        pass

    def delete_cluster_thread(self, cluster_id):
        pass