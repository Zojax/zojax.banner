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
from zope.component import getUtility
from zojax.banner.interfaces import IBanners


class SponsorsPortlet(object):

    def update(self):
        banners = []
        for place in getUtility(IBanners).values():
            for banner in place.values():
                if banner.logo is not None and banner.logo.data:
                    banners.append(banner)
        self.banners = banners

        super(SponsorsPortlet, self).update()

    def isAvailable(self):
        return len(self.banners)
