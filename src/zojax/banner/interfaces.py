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

from zope import interface, schema
from zope.i18nmessageid import MessageFactory
from zojax.filefield.field import FileField, ImageField
from zojax.content.type.interfaces import IItem

_ = MessageFactory('zojax.banner')



class IBanner(IItem):

    url = schema.TextLine(
        title = _(u"Target URL"),
        description = _(u"Target URL assiciated with banner"),
        default=u'http://www.example.com')

    alt = schema.TextLine(
        title = _(u"Alternative text"),
        description = _(u"Alternative text"),
        default=u'Alternative text')

    code = schema.Text(
        title=_(u"Code of banner"),
        description = _(u"Code of banner"),
        default = u"""<a href="%(url)s" title="%(alt)s"><img src="%(prefix)s%(name)s" alt="%(alt)s"/></a>""",
        required = True)

    beginTime = schema.Time(
        title = _(u"Begin time"),
        description = _(u"Begin time"),
        required=False)

    endTime = schema.Time(
        title = _(u"End time"),
        description = _(u"End time"),
        required=False)

    rate = schema.Int(
        title=_(u"Banner rate"),
        description=_(u"Banner rate"),
        default = 1,
        min = 1,
        max = 100)

    beginDate = schema.Date(
        title = _(u"Banner show begin date"),
        description = _(u"The date when banner show begun"),
        required=False)

    endDate = schema.Date(
        title = _(u"Banner show end date"),
        description = _(u"The date when banner show ends"),
        required=False)

    enabled = schema.Bool(
        title = _(u"Enabled"),
        description = _(u"Enable banner show"),
        required = True,
        default = True)

    logo = ImageField(
        title = _(u'Logo'),
        description = _(u'This image will be shown in sponsor portlet'),
        required = False)

    data = FileField(
        title = _(u'Data'),
        description = _(u'The actual content of the banner.'),
        required = False)

    def isAvailable() :
        """ available flag """


class IEmptyBanner(IBanner):
    """ empty banner """


class IBannerAlgorithm(interface.Interface) :
    """ Banner Choice Algorithm """

    def choice() :
        """ Choice one item from banner place """


class IBannerPlace(IItem):
    """ banner place """

    defaultBanner = ImageField(
        title=_(u'Default banner'),
        description=_(u'This image will be shown when there are no banners'),
        )

    useFakePlace = schema.Bool(
        title = _(u"Use fake place"),
        default = False)

    fakePlaceRoot = schema.TextLine(
        title = _(u'Fake place root'),
        default = u'',
        required = False)

    algorithm = schema.Choice(
        title = _(u'Algorithm'),
        description = u'Algorithm that be used to choice current banner',
        vocabulary = 'zojax.banner.algorithms',
        default = 'Random')


class IBanners(interface.Interface):
    """ banners configlet """
