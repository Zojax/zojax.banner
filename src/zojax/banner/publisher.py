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
import time, datetime

from zope import interface
from zope.component import getUtility, getMultiAdapter, getAdapter
from zope.location import Location, LocationProxy
from zope.traversing.browser.interfaces import IAbsoluteURL
from zope.app.component.hooks import getSite

from zope.datetime import rfc1123_date
from zope.datetime import time as timeFromDateTimeString

from zope.dublincore.interfaces import ICMFDublinCore

from zope.publisher.browser import BrowserView
from zope.publisher.interfaces import NotFound
from zope.publisher.interfaces.browser import IBrowserPublisher

from zojax.resource.interfaces import IResource

from interfaces import \
    IBanners, IBannerPlace, IBanner, IBannerAlgorithm, IEmptyBanner

_marker = object()


class Banners(BrowserView, Location):
    interface.implements(IBrowserPublisher)

    def __init__(self, parent, context, request):
        self.__parent__ = parent
        self.__name__ = context.__name__

        self.context = context
        self.request = request

    def publishTraverse(self, request, name):
        return self.get(name)

    def browserDefault(self, request):
        if IBannerPlace.providedBy(self.context):
            return getattr(
                BannerWrapper(self.select(), self.request), request.method), ()
        return empty, ()

    def select(self):
        res = getAdapter(
            self.context, IBannerAlgorithm,
            name=self.context.algorithm).choice()
        if IEmptyBanner.providedBy(res):
            return LocationProxy(res, self.context, 'default')
        return res

    def get(self, name, default=None):
        try:
            return self[name]
        except KeyError:
            if default is _marker:
                raise NotFound(None, name)
            return default

    def __getitem__(self, name):
        resource = self.context.get(name)

        if resource is None:
            raise KeyError(name)

        if IBannerPlace.providedBy(resource):
            return Banners(self, resource, self.request)
        else:
            return BannerWrapper(resource, self.request)


class ContainerBanners(Banners):

    def __init__(self, request):
        self.__name__ = u'zojax-banners'

        self.request = request
        self.context = getUtility(IBanners)


class BannerWrapper(Location):
    interface.implements(IResource, IBrowserPublisher)

    attr = None

    def __init__(self, resource, request):
        self.request = request
        self.resource = resource

        self.__name__ = resource.__name__

    def __call__(self):
        name = self.__name__
        url = str(getMultiAdapter((getSite(), self.request), IAbsoluteURL))
        return "%s/@@/zojax-banners/%s" % (url, name)

    def publishTraverse(self, request, name):
        if name == 'logo':
            self.attr = name
            return self.GET
        raise NotFound(None, name)

    def browserDefault(self, request):
        return getattr(self, request.method), ()

    def GET(self):
        request = self.request
        response = request.response

        resource = self.resource
        try:
            modified = ICMFDublinCore(resource).modified
        except TypeError:
            modified = datetime.datetime.now()
        lmt = long(time.mktime(modified.timetuple()))

        header = request.getHeader('If-Modified-Since', None)
        if header is not None:
            header = header.split(';')[0]
            try:    mod_since=long(timeFromDateTimeString(header))
            except: mod_since=None
            if mod_since is not None:
                if lmt > 0 and lmt <= mod_since:
                    response.setStatus(304)
                    return ''

        response.setHeader('Last-Modified', rfc1123_date(lmt))
        return resource.render(request, attr=self.attr)

    def HEAD(self):
        resource = self.resource
        dc = ICMFDublinCore(resource)
        lmt = long(time.mktime(dc.modified.timetuple()))

        response = self.request.response
        response.setHeader('Last-Modified', lmt)
        resource.render(self.request)
        return ''

    def modified(self):
        dc = ICMFDublinCore(self.resource)
        return long(time.mktime(dc.modified.timetuple()))


def empty():
    return ''
