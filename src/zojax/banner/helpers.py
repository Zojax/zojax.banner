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
import time
from zope import interface, component
from zope.dublincore.interfaces import ICMFDublinCore
from zojax.cacheheaders.interfaces import IModificationInfo

from interfaces import IBanner


class ModificationInfo(object):
    component.adapts(IBanner)
    interface.implements(IModificationInfo)

    def __init__(self, resource):
        self.resource = resource

    def modified(self):
        dc = ICMFDublinCore(self.resource)
        return long(time.mktime(dc.modified.timetuple()))
