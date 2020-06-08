# Copyright 2020 The SODA Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""

**periodical task manager**

"""

from oslo_config import cfg
from oslo_log import log
from oslo_service import periodic_task
from oslo_utils import importutils

from dolphin import coordination
from dolphin import manager
from dolphin.drivers import manager as driver_manager
from dolphin.exporter import base_exporter
from dolphin.task_manager import rpcapi as task_rpcapi

LOG = log.getLogger(__name__)
CONF = cfg.CONF
CONF.import_opt('periodic_interval', 'dolphin.service')


class TaskManager(manager.Manager):
    """manage periodical tasks"""

    RPC_API_VERSION = '1.0'

    def __init__(self, service_name=None, *args, **kwargs):
        super(TaskManager, self).__init__(*args, **kwargs)
        self.task_rpcapi = task_rpcapi.TaskAPI()

    @periodic_task.periodic_task(spacing=2, run_immediately=True)
    @coordination.synchronized('lock-task-example')
    def _task_example(self, context):
        """Periodical task, it will use coordination for
        distribute synchronization.
        """
        LOG.info("Produce task, say hello ...")
        self.task_rpcapi.say_hello(context)

    def say_hello(self, context, request_spec=None,
                  filter_properties=None):
        try:
            LOG.info("Consume say hello task ...")
            # get resource data, use static data for example here
            data = {
                'device_id': '123456',
                'pool_num': '4',
            }
            # report data to northbound platform
            base_exporter.dispatch_example_data(data)

        except Exception:
            pass

    def sync_storage_resource(self, context, storage_id, resource_task):
        LOG.debug("Received the sync_storage task: {0} request for storage"
                  " id:{1}".format(resource_task, storage_id))
        cls = importutils.import_class(resource_task)
        device_obj = cls(context, storage_id)
        device_obj.sync()

    def remove_storage_resource(self, context, storage_id, resource_task):
        cls = importutils.import_class(resource_task)
        device_obj = cls(context, storage_id)
        device_obj.remove()

    def remove_storage_in_cache(self, context, storage_id):
        LOG.info('Remove storage device in memory for storage id:{0}'
                 .format(storage_id))
        drivers = driver_manager.DriverManager()
        drivers.remove_driver(storage_id)
