# Copyright 2021 The SODA Authors.
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

from delfin.drivers import driver
from delfin.drivers.netapp.dataontap import netapp_handler
from delfin.drivers.netapp.dataontap.netapp_handler import NetAppHandler


class NetAppCmodeDriver(driver.StorageDriver):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.netapp_handler = netapp_handler.NetAppHandler(**kwargs)
        self.netapp_handler.login()

    def reset_connection(self, context, **kwargs):
        self.netapp_handler.login()

    def get_storage(self, context):
        return self.netapp_handler.get_storage()

    def list_storage_pools(self, context):
        return self.netapp_handler.list_storage_pools(self.storage_id)

    def list_volumes(self, context):
        return self.netapp_handler.list_volumes(self.storage_id)

    def list_controllers(self, context):
        pass

    def list_ports(self, context):
        pass

    def list_disks(self, context):
        pass

    def list_alerts(self, context, query_para=None):
        return self.netapp_handler.list_alerts(query_para)

    def list_qtrees(self, context):
        pass

    def list_quotas(self, context):
        pass

    def list_filesystems(self, context):
        pass

    def list_shares(self, context):
        pass

    def add_trap_config(self, context, trap_config):
        pass

    def remove_trap_config(self, context, trap_config):
        pass

    @staticmethod
    def parse_alert(context, alert):
        return NetAppHandler.parse_alert(alert)

    def clear_alert(self, context, alert):
        return self.netapp_handler.clear_alert(alert)

    @staticmethod
    def get_access_url():
        return 'https://{ip}'
