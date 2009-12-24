##############################################################################
#
# Copyright (c) 2008 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""

$Id$
"""
from zope import interface
from zope.proxy import removeAllProxies
from zope.location import LocationProxy
from zope.publisher.interfaces import NotFound
from z3c.traverser.interfaces import ITraverserPlugin

from zojax.banner.interfaces import IBanners, IBannerPlace


class ContainerPublisherPlugin(object):
    interface.implements(ITraverserPlugin)

    def __init__(self, container, request):
        self.context = container
        self.request = request

    def publishTraverse(self, request, name):
        if name in self.context:
            return LocationProxy(
                removeAllProxies(self.context[name]), self.context, name)
        else:
            raise NotFound(self.context, name, request)


def getPath(resource):
    path = []

    while not IBanners.providedBy(resource):
        path.append(resource.__name__)
        resource = getattr(resource, '__parent__', None)
        if resource is None:
            break

    path.reverse()
    return '/'.join(path)
