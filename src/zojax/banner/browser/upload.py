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
from cStringIO import StringIO
import os.path, zipfile, tarfile

from zope import event
from zope.lifecycleevent import ObjectCreatedEvent

from zojax.wizard.step import WizardStep
from zojax.filefield.data import FileData
from zojax.statusmessage.interfaces import IStatusMessage

from zojax.banner.banner import Banner
from zojax.banner.interfaces import _, IBanner


class UploadBanners(WizardStep):
    """ batch uploads """

    def update(self):
        request = self.request

        if 'form.upload' in request:
            files = []
            filenames = []

            context = self.context

            for key, val in request.form.items():
                if key.startswith('file_'):
                    files.append((key, val))

            for key, file in files:
                for name, resource in self.unpack(file):
                    name = os.path.split(name)[-1]
                    if name in context:
                        del context[name]

                    context[name] = resource

                IStatusMessage(request).add(_(u'Files have been uploaded.'))
                self.redirect('../')

    def unpack(self, file):
        filename = os.path.split(file.filename)[1]

        file_data = []
        extracted = 0

        pre, ext = os.path.splitext(filename)
        file.seek(0)

        if ext in ('.tar', '.gz', '.tgz', '.bz2', '.tbz2'):
            if ext == '.tar':
                tar = tarfile.open(name=filename, mode='r|', fileobj=file)
            elif ext in ('.gz', '.tgz'):
                tar = tarfile.open(name=filename, mode='r|gz', fileobj=file)
            elif ext in ('.bz2', '.tbz2'):
                tar = tarfile.open(name=filename, mode='r|bz2', fileobj=file)

            for ti in tar:
                if ti.isreg():
                    file_data.append(
                        (ti.name, StringIO(tar.extractfile(ti).read())))

        elif ext == '.zip':
            zip = zipfile.ZipFile(file, "r")
            for name in zip.namelist():
                file_data.append((name, zip.read(name)))
        else:
            file_data.append((filename, file))

        for name, data in file_data:
            fn = os.path.split(name)[1]

            if fn:
                file = Banner(unicode(fn))
                file.data = FileData(data, fn)
                event.notify(ObjectCreatedEvent(file))

                yield name, file
