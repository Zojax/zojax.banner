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
from zope.schema import getFieldNames
from zope.traversing.browser import absoluteURL
from zope.app.component.hooks import getSite

from zojax.banner.interfaces import IBanner


class SponsorView(object):
    """ SponsorView """

    def code(self):
        """ fill code property with values """
        context = self.context

        d = dict([(x, getattr(context, x)) for x in getFieldNames(IBanner)])

        container = context.__parent__
        name = u'/'.join(['/@@/zojax-banners',
                          context.__parent__.__name__, context.__name__,'logo'])
        if container.useFakePlace :
            d['prefix'] = container.fakePlaceRoot
            d['name'] = name
        else :
            d['prefix'] = absoluteURL(getSite(), self.request)
            d['name'] = name

        return context.code % d


class BannerView(object) :
    """ BannerView """

    def code(self):
        """ fill code property with values """
        context = self.context

        d = dict([ (x, getattr(context, x)) for x in  getFieldNames(IBanner)])

        container = context.__parent__
        name = u'/'.join(['/@@/zojax-banners',
                          context.__parent__.__name__, context.__name__])
        if container.useFakePlace :
            d['prefix'] = container.fakePlaceRoot
            d['name'] = name
        else :
            d['prefix'] = absoluteURL(getSite(), self.request)
            d['name'] = name

        return context.code % d


class EmptyBannerView(object) :
    """ BannerView """

    def src(self):
        """ banner source """
        return '%s/@@/zojax-banners/%s' % (
            absoluteURL(getSite(), self.request),
            self.context.__parent__.__name__)
