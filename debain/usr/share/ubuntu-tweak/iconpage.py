import pygtk
pygtk.require("2.0")
import gtk
import gettext
import gconf

from gconfcheckbutton import GConfCheckButton

gettext.install("ubuntu-tweak", unicode = True)

icon_dir = "/apps/nautilus/desktop"

computer_icon = \
{
	"label" : _("Show \"Computer\" icon on desktop"),
	"rename" : _("Rename the \"Computer\" icon: "),
	"visible" : "/apps/nautilus/desktop/computer_icon_visible",
	"name" : "/apps/nautilus/desktop/computer_icon_name",
	"icon" : "gnome-fs-client"
}

home_icon = \
{
	"label" : _("Show \"Home\" icon on desktop"),
	"rename" : _("Rename the \"Home\" icon: "),
	"visible" : "/apps/nautilus/desktop/home_icon_visible",
	"name" : "/apps/nautilus/desktop/home_icon_name",
	"icon" : "gnome-fs-home"
}
	
trash_icon = \
{
	"label" : _("Show \"Trash\" icon on desktop"),
	"rename" : _("Rename the \"Trash\" icon: "),
	"visible" : "/apps/nautilus/desktop/trash_icon_visible",
	"name" : "/apps/nautilus/desktop/trash_icon_name",
	"icon" : "gnome-fs-trash-empty"
}

desktop_icon = (computer_icon, home_icon, trash_icon)

class GConfEntry(gtk.Entry):
	def __activated_cb(self, widget, data = None):
		client = gconf.client_get_default()
		
		print self.get_text()
		client.set_string(data, self.get_text())

	def __init__(self, key):
		gtk.Entry.__init__(self)
		self.connect("activate", self.__activated_cb, key)

		client = gconf.client_get_default()
		name = client.get_string(key)

		if name:
			self.set_text(name)
		else:
			self.set_text(_("Unset"))

class IconPage(gtk.VBox):
	"""Desktop Icon settings"""
	def __button_toggled(self, widget ,data = None):
		client = gconf.client_get_default()
		print data
		value = client.get(data)
		print value

		if value.type == gconf.VALUE_BOOL:
			if widget.get_active():
				client.set_bool(data, True)
				widget.box.set_sensitive(True)
			else:
				client.set_bool(data, False)
				widget.box.set_sensitive(False)

	def __button_toggled_to_entry(self, widget ,data = None):
		if widget.get_active():
			widget.entry.set_sensitive(True)
		else:
			client = gconf.client_get_default()
			client.unset(data)
			widget.entry.set_text(_("Unset"))
			widget.entry.set_sensitive(False)

	def __init__(self):
		gtk.VBox.__init__(self)

		main_vbox = gtk.VBox(False, 5)
		main_vbox.set_border_width(5)
		self.pack_start(main_vbox, False, False, 0)

		label = gtk.Label()
		label.set_markup(_("<b>Desktop Icon settings</b>"))
		label.set_alignment(0, 0)
		main_vbox.pack_start(label, False, False, 0)

		main_button = GConfCheckButton(_("Show desktop icons"), "/apps/nautilus/preferences/show_desktop", "/apps/nautilus/preferences")
		main_button.connect("toggled", self.__button_toggled, "/apps/nautilus/preferences/show_desktop")
		main_vbox.pack_start(main_button, False, False, 0)

		main_button.box = gtk.HBox(False, 10)
		main_vbox.pack_start(main_button.box, False, False,0)

		if not main_button.get_active():
			main_button.box.set_sensitive(False)

		label = gtk.Label(" ")
		main_button.box.pack_start(label, False, False, 0)

		main_button.vbox = gtk.VBox(False, 5)
		main_button.box.pack_start(main_button.vbox, False, False, 0)

		client = gconf.client_get_default()
		for element in desktop_icon:
			button = GConfCheckButton(element["label"], element["visible"], icon_dir)
			button.connect("toggled", self.__button_toggled, element["visible"])
			main_button.vbox.pack_start(button, False, False, 0)

			button.box = gtk.HBox(False, 10)
			main_button.vbox.pack_start(button.box, False, False, 0)

			if not button.get_active():
				button.box.set_sensitive(False)

			icon = gtk.image_new_from_icon_name(element["icon"], gtk.ICON_SIZE_DIALOG)
			button.box.pack_start(icon, False, False, 0)

			button_rename = GConfCheckButton(element["rename"], element["name"], extra = self.__button_toggled_to_entry)
			vbox= gtk.VBox(False, 5)
			button.box.pack_start(vbox, False, False, 0)
			vbox.pack_start(button_rename, False, False, 0)

			button_rename.entry = GConfEntry(element["name"])
			if not button_rename.get_active():
				button_rename.entry.set_sensitive(False)
			vbox.pack_start(button_rename.entry, False, False, 0)


		#other
		button = GConfCheckButton(_("Use Home Directory as Desktop"), "/apps/nautilus/preferences/desktop_is_home_dir","/apps/nautilus/preferences")
		main_button.vbox.pack_start(button, False, False, 0)

		button = GConfCheckButton(_("Show \"Network\" icon on desktop"), "/apps/nautilus/desktop/network_icon_visible", icon_dir)
		main_button.vbox.pack_start(button, False, False, 0)

		button = GConfCheckButton(_("Show Mounted Volumes on desktop"), "/apps/nautilus/desktop/volumes_visible", icon_dir)
		main_button.vbox.pack_start(button, False, False, 0)