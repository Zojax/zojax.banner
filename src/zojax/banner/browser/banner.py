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
from zope.app.component.hooks import getSite
from zope.traversing.browser import absoluteURL

from zojax.wizard.step import WizardStep
from zojax.content.forms.form import AddForm
from zojax.banner.interfaces import IBanner

from publisher import getPath


class AddBanner(AddForm):

    def getName(self, object=None):
        name = self.request.get('add_input_name', '')
        if not name and object is not None:
            name = object.data.filename

        return name

    def nextURL(self):
        container = self.context.__parent__.__parent__
        return '%s/%s/context.html'%(
            absoluteURL(container, self.request), self._addedObject.__name__)


class BannerView(WizardStep):

    def path(self):
        return '%s/@@/zojax-banners/%s'%(
            absoluteURL(getSite(), self.request), getPath(self.context))
