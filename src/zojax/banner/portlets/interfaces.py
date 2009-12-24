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
from zope import interface, schema
from zojax.banner.interfaces import _


class IBannerPortlet(interface.Interface):
    """ Banner portlet """

    label = schema.TextLine(
        title = _(u'Label'),
        default = _(u'Banner'),
        required = False)

    decoration = schema.Bool(
        title = _(u'Portlet decoration'),
        description = _(u'Show portlet decoration, or just banner.'),
        default = True,
        required = False)

    place = schema.Choice(
        title= _(u'Banner Place'),
        vocabulary="zojax.banner.places")


class ISponsorsPortlet(interface.Interface):
    """ Sponsors portlet """

    label = schema.TextLine(
        title = _(u'Label'),
        default = _(u'Sponsors'),
        required = False)

    decoration = schema.Bool(
        title = _(u'Portlet decoration'),
        description = _(u'Show portlet decoration, or just sponsors.'),
        default = True,
        required = False)
