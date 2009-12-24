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
from zope.traversing.browser import absoluteURL

from zojax.wizard.button import WizardButton
from zojax.content.forms.form import AddForm


class AddBannerPlace(AddForm):

    def nextURL(self):
        container = self.context.__parent__.__parent__
        return '%s/%s/context.html'%(
            absoluteURL(container, self.request), self._addedObject.__name__)


# back action
class BackButton(WizardButton):

    def actionHandler(self):
        return self.wizard.redirect('%s/'%absoluteURL(
                self.wizard.__parent__.__parent__, self.request))


backButton = BackButton(title = u'Back', weight = 500)
