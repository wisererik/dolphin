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

import six
import abc


@six.add_metaclass(abc.ABCMeta)
class StorageDriver(object):

    def __init__(self, storage):
        self.storage = storage

    @staticmethod
    def get_registry():
        raise NotImplementedError()

    @abc.abstractmethod
    def get_storage(self, context):
        pass

    @abc.abstractmethod
    def list_pools(self, context):
        pass

    @abc.abstractmethod
    def list_volumes(self, context):
        pass

