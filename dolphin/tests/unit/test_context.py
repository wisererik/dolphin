#    Copyright 2020 The SODA Authors.
#    Copyright 2011 OpenStack LLC
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import pytest

from dolphin import context


class TestContextTest:

    def test_request_context_elevated(self):
        user_context = context.RequestContext(
            'fake_user', 'fake_project', is_admin=False)
        assert not user_context.is_admin
        assert [] == user_context.roles
        admin_context = user_context.elevated()
        assert not user_context.is_admin
        assert admin_context.is_admin
        assert 'admin' not in user_context.roles
        assert 'admin' in admin_context.roles

    def test_request_context_read_deleted(self):
        ctxt = context.RequestContext('111',
                                      '222',
                                      read_deleted='yes')
        assert 'yes' == ctxt.read_deleted

        ctxt.read_deleted = 'no'
        assert 'no' == ctxt.read_deleted

    def test_request_context_read_deleted_invalid(self):

        with pytest.raises(ValueError):
            context.RequestContext('111',
                                   '222',
                                   read_deleted=True)
        with pytest.raises(ValueError):
            ctxt = context.RequestContext('111', '222')
            setattr(ctxt, 'read_deleted', True)
