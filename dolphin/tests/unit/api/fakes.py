# Copyright 2020 The SODA Authors.
# Copyright 2010 OpenStack LLC.
# All Rights Reserved.
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

import webob.dec
import webob.request

from dolphin import context
from dolphin.api.common import wsgi as os_wsgi
from dolphin.common import config  # noqa


@webob.dec.wsgify
def fake_wsgi(self, req):
    return self.application


class HTTPRequest(os_wsgi.Request):

    @classmethod
    def blank(cls, *args, **kwargs):
        if not kwargs.get('base_url'):
            kwargs['base_url'] = 'http://localhost/v1'
        use_admin_context = kwargs.pop('use_admin_context', False)
        out = os_wsgi.Request.blank(*args, **kwargs)
        out.environ['dolphin.context'] = context.RequestContext(
            is_admin=use_admin_context)
        return out
