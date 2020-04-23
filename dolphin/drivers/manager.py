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

from oslo_log import log
from oslo_utils import importutils

from dolphin import db

LOG = log.getLogger(__name__)

DRIVER_MAPPING = {
    "fake_storage": "dolphin.drivers.fake_storage.FakeStorage"
}


class DriverManager(object):

    def __init__(self):
        self.driver_factory = dict()

    def register_storage(self, context, register_info):
        try:
            # Initialize driver based on register info
            driver_key = "_".join((register_info["manufacturer"],
                                   register_info["model"]))
            driver_cls = importutils.import_class(DRIVER_MAPPING[driver_key])
            driver = driver_cls()

            # Register or get storage device info by register info
            storage_info = driver.register_storage(context, register_info)
            storage = db.storage_create(storage_info)

            # Save register info, password should be encoded before saving
            register_info["storage_id"] = storage["id"]
            db.registry_context_create(register_info)

            # Save driver instance into factory
            driver.storage = storage
            self.driver_factory[storage["id"]] = driver
            return storage_info
        except Exception as e:
            LOG.exception("Caught exception when registering a storage")
            raise e

    def get_storage(self, context, storage_id):
        driver = None
        if storage_id in self.driver_factory:
            driver = self.driver_factory[storage_id]
        try:
            if driver is None:
                # Initialize driver based on storage info from database
                storage = db.storage_get(storage_id)
                driver_key = "_".join((storage["manufacturer"],
                                       storage["model"]))
                driver_cls = importutils.import_class(DRIVER_MAPPING[driver_key])
                driver = driver_cls(storage)

                # Register or get storage device info by register info
                storage_info = driver.get_storage(context)
                storage.update(storage_info)
                driver.storage = storage


                # Save register info, password should be encoded before saving
                register_info["storage_id"] = storage["id"]
                db.registry_context_create(register_info)

                # Save driver instance into factory
                driver.storage = storage
                self.driver_factory[storage["id"]] = driver
                return storage_info
        except Exception as e:
            LOG.exception("Caught exception when registering a storage")
            raise e

    def list_pools(self, context):
        pass

    def list_volumes(self, context):
        pass


