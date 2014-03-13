# -*- coding: utf-8 -*-
# torrentview_data_funcs.py
#
# Copyright (C) 2007, 2008 Andrew Resch <andrewresch@gmail.com>
#
# Deluge is free software.
#
# You may redistribute it and/or modify it under the terms of the
# GNU General Public License, as published by the Free Software
# Foundation; either version 3 of the License, or (at your option)
# any later version.
#
# deluge is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with deluge.    If not, write to:
#     The Free Software Foundation, Inc.,
#     51 Franklin Street, Fifth Floor
#     Boston, MA  02110-1301, USA.
#
#    In addition, as a special exception, the copyright holders give
#    permission to link the code of portions of this program with the OpenSSL
#    library.
#    You must obey the GNU General Public License in all respects for all of
#    the code used other than OpenSSL. If you modify file(s) with this
#    exception, you may extend this exception to your version of the file(s),
#    but you are not obligated to do so. If you do not wish to do so, delete
#    this exception statement from your version. If you delete this exception
#    statement from all source files in the program, then also delete it here.
#
#

import deluge.common as common
import gtk
import warnings
import gobject
import deluge.component as component

# Status icons.. Create them from file only once to avoid constantly
# re-creating them.
icon_downloading = gtk.gdk.pixbuf_new_from_file(common.get_pixmap("downloading16.png"))
icon_seeding = gtk.gdk.pixbuf_new_from_file(common.get_pixmap("seeding16.png"))
icon_inactive = gtk.gdk.pixbuf_new_from_file(common.get_pixmap("inactive16.png"))
icon_alert = gtk.gdk.pixbuf_new_from_file(common.get_pixmap("alert16.png"))
icon_queued = gtk.gdk.pixbuf_new_from_file(common.get_pixmap("queued16.png"))
icon_checking = gtk.gdk.pixbuf_new_from_file(common.get_pixmap("checking16.png"))

# Holds the info for which status icon to display based on state
ICON_STATE = {
    "Allocating": icon_checking,
    "Checking": icon_checking,
    "Downloading": icon_downloading,
    "Seeding": icon_seeding,
    "Paused": icon_inactive,
    "Error": icon_alert,
    "Queued": icon_queued,
    "Checking Resume Data": icon_checking
}

def _(message): return message

TRANSLATE = {
    "Downloading": _("Downloading"),
    "Seeding": _("Seeding"),
    "Paused": _("Paused"),
    "Checking": _("Checking"),
    "Queued": _("Queued"),
    "Error": _("Error"),
}

del _

def _t(text):
    if text in TRANSLATE:
        text = TRANSLATE[text]
    return _(text)

def cell_data_statusicon(column, cell, model, row, data):
    """Display text with an icon"""
    try:
        state = model.get_value(row, data)

        if column.cached_cell_renderer_value == state:
            return
        column.cached_cell_renderer_value = state

        icon = ICON_STATE[state]

        #Supress Warning: g_object_set_qdata: assertion `G_IS_OBJECT (object)' failed
        original_filters = warnings.filters[:]
        warnings.simplefilter("ignore")
        try:
            cell.set_property("pixbuf", icon)
        finally:
            warnings.filters = original_filters

    except KeyError:
        pass

def create_blank_pixbuf():
    i = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, True, 8, 16, 16)
    i.fill(0x00000000)
    return i

def set_icon(icon, cell):
    if icon:
        pixbuf = icon.get_cached_icon()
        if pixbuf is None:
            try:
                pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(icon.get_filename(), 16, 16)
            except gobject.GError, e:
                # Failed to load the pixbuf (Bad image file), so set a blank pixbuf
                pixbuf = create_blank_pixbuf()
            finally:
                icon.set_cached_icon(pixbuf)
    else:
        pixbuf = create_blank_pixbuf()

    #Suppress Warning: g_object_set_qdata: assertion `G_IS_OBJECT (object)' failed
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        cell.set_property("pixbuf", pixbuf)

def cell_data_trackericon(column, cell, model, row, data):
    host = model[row][data]

    if column.cached_cell_renderer_value == host:
        return
    if host:
        if not component.get("TrackerIcons").has(host):
            # Set blank icon while waiting for the icon to be loaded
            set_icon(None, cell)
            component.get("TrackerIcons").fetch(host)
            column.cached_cell_renderer_value = None
        else:
            set_icon(component.get("TrackerIcons").get(host), cell)
            # Only set the last value when we have found the icon
            column.cached_cell_renderer_value = host
    else:
        set_icon(None, cell)
        column.cached_cell_renderer_value = None

def cell_data_progress(column, cell, model, row, data):
    """Display progress bar with text"""
    (value, state_str) = model.get(row, *data)
    if column.cached_cell_renderer_value[0] != value:
        column.cached_cell_renderer_value[0] = value
        cell.set_property("value", value)

    textstr = _t(state_str)
    if state_str != "Seeding" and value < 100:
        textstr = textstr + " %.2f%%" % value

    if column.cached_cell_renderer_value[1] != textstr:
        column.cached_cell_renderer_value[1] = textstr
        cell.set_property("text", textstr)

def cell_data_queue(column, cell, model, row, data):
    value = model.get_value(row, data)

    if column.cached_cell_renderer_value == value:
        return
    column.cached_cell_renderer_value = value

    if value < 0:
        cell.set_property("text", "")
    else:
        cell.set_property("text", str(value + 1))

def cell_data_speed(column, cell, model, row, data):
    """Display value as a speed, eg. 2 KiB/s"""
    #print "cell_data_speed:", type(column)
    #print "cell_data_speed:", dir(column)
    try:
        speed = model.get_value(row, data)
    except AttributeError, e:
        print "AttributeError"
        import traceback
        traceback.print_exc()
    if column.cached_cell_renderer_value == speed:
        return
    column.cached_cell_renderer_value = speed

    speed_str = ""
    if speed > 0:
        speed_str = common.fspeed(speed)
    cell.set_property('text', speed_str)

def cell_data_speed_limit(column, cell, model, row, data):
    """Display value as a speed, eg. 2 KiB/s"""
    speed = model.get_value(row, data)

    if column.cached_cell_renderer_value == speed:
        return
    column.cached_cell_renderer_value = speed

    speed_str = ""
    if speed > 0:
        speed_str = common.fspeed(speed * 1024)
    cell.set_property('text', speed_str)

def cell_data_size(column, cell, model, row, data):
    """Display value in terms of size, eg. 2 MB"""
    size = model.get_value(row, data)
    cell.set_property('text', common.fsize(size))

def cell_data_peer(column, cell, model, row, data):
    """Display values as 'value1 (value2)'"""
    (first, second) = model.get(row, *data)
    # Only display a (total) if second is greater than -1
    if second > -1:
        cell.set_property('text', '%d (%d)' % (first, second))
    else:
        cell.set_property('text', '%d' % first)

def cell_data_time(column, cell, model, row, data):
    """Display value as time, eg 1m10s"""
    time = model.get_value(row, data)
    if column.cached_cell_renderer_value == time:
        return
    column.cached_cell_renderer_value = time

    if time <= 0:
        time_str = ""
    else:
        time_str = common.ftime(time)
    cell.set_property('text', time_str)

def cell_data_ratio(column, cell, model, row, data):
    """Display value as a ratio with a precision of 3."""
    ratio = model.get_value(row, data)
    # Previous value in cell is the same as for this value, so ignore
    if column.cached_cell_renderer_value == ratio:
        return
    column.cached_cell_renderer_value = ratio
    cell.set_property('text', "∞" if ratio < 0 else "%.3f" % ratio)

def cell_data_date(column, cell, model, row, data):
    """Display value as date, eg 05/05/08"""
    date = model.get_value(row, data)

    if column.cached_cell_renderer_value == date:
        return
    column.cached_cell_renderer_value = date

    date_str = common.fdate(date) if date > 0.0 else ""
    cell.set_property('text', date_str)

def cell_data_date_or_never(column, cell, model, row, data):
    """Display value as date, eg 05/05/08 or Never"""
    value = model.get_value(row, data)

    if column.cached_cell_renderer_value == value:
        return
    column.cached_cell_renderer_value = value

    date_str = common.fdate(value) if value > 0.0 else _("Never")
    cell.set_property('text', date_str)

