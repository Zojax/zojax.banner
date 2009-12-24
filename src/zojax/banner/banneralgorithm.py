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
from random import shuffle, randint
from thread import allocate_lock

from zope import interface, component

from banner import EmptyBanner
from interfaces import IBanners, IBannerPlace, IBannerAlgorithm


class BannerAlgorithmBase(object) :
    interface.implements(IBannerAlgorithm)
    component.adapts(IBannerPlace)

    def __init__(self, context):
        self.context = context

    def values(self):
        return (x for x in self.context.values() if x.isAvailable())

    def choice(self):
        """ Choice one banner """


class BannerAlgorithmRandom(BannerAlgorithmBase) :

    def choice(self):
        """ Choice one banner by simpler random way """
        imgs = []
        sum = 0
        for img in self.values():
            imgs.append(img)
            sum += img.rate

        if imgs:
            rnd = randint(0,sum-1)
            pos = 0
            for img in imgs :
                pos += img.rate
                if pos > rnd :
                    break
        else:
            img = EmptyBanner(self.context.defaultBanner)

        return img


class BannerAlgorithmRound(BannerAlgorithmBase) :

    queue = []

    lock = allocate_lock()

    def choice(self) :
        """ Choice one banner by simpler random way """

        self.lock.acquire()
        try :
            while True :
                try :
                    img = self.queue.pop()
                    break
                except IndexError :
                    for img in self.values():
                        self.queue.extend([img] * int(img.rate))

                    if not self.queue :
                        img = EmptyBanner(self.context.defaultBanner)
                        break

                    shuffle(self.queue)
        finally :
            self.lock.release()

        return img
