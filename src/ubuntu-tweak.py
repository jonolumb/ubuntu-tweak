#!/usr/bin/env python
# coding: utf-8

# Ubuntu Tweak - PyGTK based desktop configure tool
#
# Copyright (C) 2007-2008 TualatriX <tualatrix@gmail.com>
#
# Ubuntu Tweak is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Ubuntu Tweak is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

import gtk
import gettext
import os

from Computer import DISTRIB

gettext.install("ubuntu-tweak", unicode = True)

def show_error(message, title = _("Error"), parent = None):
	dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK)
	dialog.set_title(title)
	dialog.set_markup(message)
	dialog.run()
	dialog.destroy()

if __name__ == "__main__":
	if DISTRIB != "feisty" and DISTRIB != "gutsy" and DISTRIB != "hardy":
		show_error(_("Sorry!\n\nUbuntu Tweak can only run on <b>Ubuntu 7.04 or 7.10.</b>\n"))
	else:
		#determine whether the gnome is the default desktop
		if os.getenv("GNOME_DESKTOP_SESSION_ID"):
			from MainWindow import MainWindow
			MainWindow().main()
		else:
			show_error(_("Sorry!\n\nUbuntu Tweak can only run in <b>GNOME Desktop.</b>\n"))
