# -*- coding: utf-8 -*-
#
# Copyright (C) 2009 Andrew Resch <andrewresch@gmail.com>
#
# This file is part of Deluge and is licensed under GNU General Public License 3.0, or later, with
# the additional special exception to link portions of this program with the OpenSSL library.
# See LICENSE for more details.
#

"""
Event module.

This module describes the types of events that can be generated by the daemon
and subsequently emitted to the clients.

"""

known_events = {}


class DelugeEventMetaClass(type):
    """
    This metaclass simply keeps a list of all events classes created.
    """
    def __init__(self, name, bases, dct):  # pylint: disable=bad-mcs-method-argument
        super(DelugeEventMetaClass, self).__init__(name, bases, dct)
        if name != "DelugeEvent":
            known_events[name] = self


class DelugeEvent(object):
    """
    The base class for all events.

    :prop name: this is the name of the class which is in-turn the event name
    :type name: string
    :prop args: a list of the attribute values
    :type args: list

    """
    __metaclass__ = DelugeEventMetaClass

    def _get_name(self):
        return self.__class__.__name__

    def _get_args(self):
        if not hasattr(self, "_args"):
            return []
        return self._args

    name = property(fget=_get_name)
    args = property(fget=_get_args)


class TorrentAddedEvent(DelugeEvent):
    """
    Emitted when a new torrent is successfully added to the session.
    """
    def __init__(self, torrent_id, from_state):
        """
        :param torrent_id: the torrent_id of the torrent that was added
        :type torrent_id: string
        :param from_state: was the torrent loaded from state? Or is it a new torrent.
        :type from_state: bool
        """
        self._args = [torrent_id, from_state]


class TorrentRemovedEvent(DelugeEvent):
    """
    Emitted when a torrent has been removed from the session.
    """
    def __init__(self, torrent_id):
        """
        :param torrent_id: the torrent_id
        :type torrent_id: string
        """
        self._args = [torrent_id]


class PreTorrentRemovedEvent(DelugeEvent):
    """
    Emitted when a torrent is about to be removed from the session.
    """
    def __init__(self, torrent_id):
        """
        :param torrent_id: the torrent_id
        :type torrent_id: string
        """
        self._args = [torrent_id]


class TorrentStateChangedEvent(DelugeEvent):
    """
    Emitted when a torrent changes state.
    """
    def __init__(self, torrent_id, state):
        """
        :param torrent_id: the torrent_id
        :type torrent_id: string
        :param state: the new state
        :type state: string
        """
        self._args = [torrent_id, state]


class TorrentTrackerStatusEvent(DelugeEvent):
    """
    Emitted when a torrents tracker status changes.
    """
    def __init__(self, torrent_id, status):
        """
        Args:
            torrent_id (str): the torrent_id
            status (str): the new status
        """
        self._args = [torrent_id, status]


class TorrentQueueChangedEvent(DelugeEvent):
    """
    Emitted when the queue order has changed.
    """
    pass


class TorrentFolderRenamedEvent(DelugeEvent):
    """
    Emitted when a folder within a torrent has been renamed.
    """
    def __init__(self, torrent_id, old, new):
        """
        :param torrent_id: the torrent_id
        :type torrent_id: string
        :param old: the old folder name
        :type old: string
        :param new: the new folder name
        :type new: string
        """
        self._args = [torrent_id, old, new]


class TorrentFileRenamedEvent(DelugeEvent):
    """
    Emitted when a file within a torrent has been renamed.
    """
    def __init__(self, torrent_id, index, name):
        """
        :param torrent_id: the torrent_id
        :type torrent_id: string
        :param index: the index of the file
        :type index: int
        :param name: the new filename
        :type name: string
        """
        self._args = [torrent_id, index, name]


class TorrentFinishedEvent(DelugeEvent):
    """
    Emitted when a torrent finishes downloading.
    """
    def __init__(self, torrent_id):
        """
        :param torrent_id: the torrent_id
        :type torrent_id: string
        """
        self._args = [torrent_id]


class TorrentResumedEvent(DelugeEvent):
    """
    Emitted when a torrent resumes from a paused state.
    """
    def __init__(self, torrent_id):
        """
        :param torrent_id: the torrent_id
        :type torrent_id: string
        """
        self._args = [torrent_id]


class TorrentFileCompletedEvent(DelugeEvent):
    """
    Emitted when a file completes.
    """
    def __init__(self, torrent_id, index):
        """
        :param torrent_id: the torrent_id
        :type torrent_id: string
        :param index: the file index
        :type index: int
        """
        self._args = [torrent_id, index]


class TorrentStorageMovedEvent(DelugeEvent):
    """
    Emitted when the storage location for a torrent has been moved.
    """
    def __init__(self, torrent_id, path):
        """
        :param torrent_id: the torrent_id
        :type torrent_id: string
        :param path: the new location
        :type path: string
        """
        self._args = [torrent_id, path]


class CreateTorrentProgressEvent(DelugeEvent):
    """
    Emitted when creating a torrent file remotely.
    """
    def __init__(self, piece_count, num_pieces):
        self._args = [piece_count, num_pieces]


class NewVersionAvailableEvent(DelugeEvent):
    """
    Emitted when a more recent version of Deluge is available.
    """
    def __init__(self, new_release):
        """
        :param new_release: the new version that is available
        :type new_release: string
        """
        self._args = [new_release]


class SessionStartedEvent(DelugeEvent):
    """
    Emitted when a session has started.  This typically only happens once when
    the daemon is initially started.
    """
    pass


class SessionPausedEvent(DelugeEvent):
    """
    Emitted when the session has been paused.
    """
    pass


class SessionResumedEvent(DelugeEvent):
    """
    Emitted when the session has been resumed.
    """
    pass


class SessionProxyUpdateEvent(DelugeEvent):
    """
    Emitted when an event has made changes to the torrent cache in the session proxy.
    """
    def __init__(self, torrent_id, **kw):
        self._args = [torrent_id, kw]


class ConfigValueChangedEvent(DelugeEvent):
    """
    Emitted when a config value changes in the Core.
    """
    def __init__(self, key, value):
        """
        :param key: the key that changed
        :type key: string
        :param value: the new value of the `:param:key`
        """
        self._args = [key, value]


class PluginEnabledEvent(DelugeEvent):
    """
    Emitted when a plugin is enabled in the Core.
    """
    def __init__(self, plugin_name):
        self._args = [plugin_name]


class PluginDisabledEvent(DelugeEvent):
    """
    Emitted when a plugin is disabled in the Core.
    """
    def __init__(self, plugin_name):
        self._args = [plugin_name]


class ClientDisconnectedEvent(DelugeEvent):
    """
    Emitted when a client disconnects.
    """
    def __init__(self, session_id):
        self._args = [session_id]


class ExternalIPEvent(DelugeEvent):
    """
    Emitted when the external ip address is received from libtorrent.
    """
    def __init__(self, external_ip):
        """
        Args:
            external_ip (str): The IP address.
        """
        self._args = [external_ip]
