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
import datetime
from pytz import utc

from zope import interface, component
from zope.interface.common.idatetime import ITZInfo
from zope.schema.fieldproperty import FieldProperty
from zope.security.management import queryInteraction
from zope.lifecycleevent.interfaces import IObjectCopiedEvent

from zojax.catalog.utils import getRequest
from zojax.content.type.item import PersistentItem
from zojax.filefield.field import FileFieldProperty
from zojax.filefield.interfaces import IFile

from interfaces import IBanner, IEmptyBanner


class BannerBase(object):
    interface.implements(IBanner)

    title = FieldProperty(IBanner['title'])

    description = FieldProperty(IBanner['description'])

    url = FieldProperty(IBanner['url'])

    alt = FieldProperty(IBanner['alt'])

    code = FieldProperty(IBanner['code'])

    beginTime = FieldProperty(IBanner['beginTime'])

    endTime = FieldProperty(IBanner['endTime'])

    rate = FieldProperty(IBanner['rate'])

    beginDate = FieldProperty(IBanner['beginDate'])

    endDate = FieldProperty(IBanner['endDate'])

    enabled = FieldProperty(IBanner['enabled'])

    data = FileFieldProperty(IBanner['data'])

    logo = FileFieldProperty(IBanner['logo'])

    def render(self, request, attr=None):
        if attr is not None:
            return getattr(self, attr).show(request, filename=self.__name__)
        return self.data.show(request, filename=self.__name__)

    def isAvailable(self):
        if self.data is None or not self.data.data:
            return False
        tz = ITZInfo(getRequest(), utc)
        lt = datetime.datetime.now(tz).timetz()

        beginTime, endTime = self.beginTime, self.endTime
        if self.beginTime is not None and self.beginTime.tzinfo is None:
            beginTime = self.beginTime.replace(tzinfo=tz)
        if self.endTime is not None and self.endTime.tzinfo is None:
            endTime = self.endTime.replace(tzinfo=tz)
        return (
            self.enabled
            and self.data is not None
            and self.data.data
            and (
                beginTime is None
                or endTime is None
                or  beginTime <= lt <= endTime
                or  (
                    beginTime >= endTime
                    and (
                        endTime <= lt
                        or  lt <= beginTime
                        )
                    )
                )
            and (
                self.beginDate is None
                or self.beginDate <= datetime.date.today()
                )
            and (
                self.endDate is None
                or self.endDate >= datetime.date.today()
                )
            )


class Banner(BannerBase, PersistentItem):
    pass


class EmptyBanner(BannerBase):
    interface.implements(IEmptyBanner)

    __name__ = 'empty'

    def __init__(self, data):
        self.data = data

    def isAvailable(self):
        return True


@component.adapter(IBanner, IObjectCopiedEvent)
def bannerCopiedEvent(resource, event):
    if IBanner.providedBy(event.original):
        if IFile.providedBy(resource.data):
            resource.data.afterCopy(event.original.data)
        if IFile.providedBy(resource.logo):
            resource.logo.afterCopy(event.original.logo)
