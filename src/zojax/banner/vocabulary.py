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
from zope.component import getSiteManager, getUtility
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from interfaces import IBannerPlace, IBannerAlgorithm, IBanners


def BannerAlgorithmsVocabulary(context):
    return SimpleVocabulary.fromValues(
        [x for x,y in getSiteManager(context).adapters.lookupAll(
                (IBannerPlace,), IBannerAlgorithm
                )]
        )


def BannerPlacesVocabulary(context):
    banners = getUtility(IBanners)
    return SimpleVocabulary(
        [SimpleTerm(x.__name__, x.__name__, x.title) for x in banners.values()]
        )
