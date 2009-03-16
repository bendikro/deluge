/*
Script: deluge-menus.js
    Contains all the menus contained within the UI for easy access and editing.

Copyright:
	(C) Damien Churchill 2009 <damoxc@gmail.com>
	This program is free software; you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation; either version 3, or (at your option)
	any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program.  If not, write to:
		The Free Software Foundation, Inc.,
		51 Franklin Street, Fifth Floor
		Boston, MA  02110-1301, USA.
*/

Deluge.Menus = {
	onTorrentAction: function(item, e) {
		var selection = Deluge.Torrents.getSelections();
		var ids = new Array();
		$each(selection, function(record) {
			ids.include(record.id);
		});
		
		switch (item.id) {
			case 'pause':
			case 'resume':
				Deluge.Client.core[item.id + '_torrent'](ids, {
					onSuccess: function() {
						Deluge.Ui.update();
					}
				});
				break;
			case 'top':
			case 'up':
			case 'down':
			case 'bottom':
				Deluge.Client.core['queue_' + item.id](ids, {
					onSuccess: function() {
						Deluge.Ui.update();
					}
				});
				break;
			case 'update':
				Deluge.Client.core.force_reannounce(ids, {
					onSuccess: function() {
						Deluge.Ui.update();
					}
				});
				break;
			case 'remove':
				Deluge.Client.core.remove_torrent(ids, null, {
					onSuccess: function() {
						Deluge.Ui.update();
					}
				});
				break;
			case 'recheck':
				Deluge.Client.core.force_recheck(ids, {
					onSuccess: function() {	
						Deluge.Ui.update();
					}
				});
				break;
		}
	}
}

Deluge.Menus.Torrent = new Ext.menu.Menu({
	id: 'torrentMenu',
	items: [{
		id: 'pause',
		text: _('Pause'),
		icon: '/icons/16/pause.png',
		handler: Deluge.Menus.onTorrentAction,
		scope: Deluge.Menus
	}, {
		id: 'resume',
		text: _('Resume'),
		icon: '/icons/16/start.png',
		handler: Deluge.Menus.onTorrentAction,
		scope: Deluge.Menus
	}, '-', {
		id: 'options',
		text: _('Options'),
		icon: '/icons/16/preferences.png',
		menu: new Ext.menu.Menu({
			items: [{
				text: _('D/L Speed Limit'),
				iconCls: 'x-deluge-downloading',
				menu: new Ext.menu.Menu({
					items: [{
						text: _('5 KiB/s'),
					}, {
						text: _('10 KiB/s'),
					}, {
						text: _('30 KiB/s'),
					}, {
						text: _('80 KiB/s'),
					}, {
						text: _('300 KiB/s'),
					},{
						text: _('Unlimited')
					}]
				})
			}, {
				text: _('U/L Speed Limit'),
				iconCls: 'x-deluge-seeding',
				menu: new Ext.menu.Menu({
					items: [{
						text: _('5 KiB/s'),
					}, {
						text: _('10 KiB/s'),
					}, {
						text: _('30 KiB/s'),
					}, {
						text: _('80 KiB/s'),
					}, {
						text: _('300 KiB/s'),
					},{
						text: _('Unlimited')
					}]
				})
			}, {
				text: _('Connection Limit'),
				icon: '/icons/16/connections.png',
				menu: new Ext.menu.Menu({
					items: [{
						text: _('50'),
					}, {
						text: _('100'),
					}, {
						text: _('200'),
					}, {
						text: _('300'),
					}, {
						text: _('500'),
					},{
						text: _('Unlimited')
					}]
				})
			}, {
				text: _('Upload Slot Limit'),
				icon: '/icons/16/upload_slots.png',
				menu: new Ext.menu.Menu({
					items: [{
						text: _('0'),
					}, {
						text: _('1'),
					}, {
						text: _('2'),
					}, {
						text: _('3'),
					}, {
						text: _('5'),
					},{
						text: _('Unlimited')
					}]
				})
			}, {
				id: 'auto_managed',
				text: _('Auto Managed'),
				checked: false
			}]
		})
	}, '-', {
		text: _('Queue'),
		icon: '/icons/16/queue.png',
		menu: new Ext.menu.Menu({
			items: [{
				id: 'top',
				text: _('Top'),
				icon: '/icons/16/top.png',
				handler: Deluge.Menus.onTorrentAction,
				scope: Deluge.Menus
			},{
				id: 'up',
				text: _('Up'),
				icon: '/icons/16/up.png',
				handler: Deluge.Menus.onTorrentAction,
				scope: Deluge.Menus
			},{
				id: 'down',
				text: _('Down'),
				icon: '/icons/16/down.png',
				handler: Deluge.Menus.onTorrentAction,
				scope: Deluge.Menus
			},{
				id: 'bottom',
				text: _('Bottom'),
				icon: '/icons/16/bottom.png',
				handler: Deluge.Menus.onTorrentAction,
				scope: Deluge.Menus
			}]
		})
	}, '-', {
		id: 'update',
		text: _('Update Tracker'),
		icon: '/icons/16/update.png',
		handler: Deluge.Menus.onTorrentAction,
		scope: Deluge.Menus
	}, {
		edit: 'edit_trackers',
		text: _('Edit Trackers'),
		icon: '/icons/16/edit_trackers.png',
		handler: Deluge.Menus.onTorrentAction,
		scope: Deluge.Menus
	}, '-', {
		id: 'remove',
		text: _('Remove Torrent'),
		icon: '/icons/16/remove.png',
		handler: Deluge.Menus.onTorrentAction,
		scope: Deluge.Menus
	}, '-', {
		id: 'recheck',
		text: _('Force Recheck'),
		icon: '/icons/16/recheck.png',
		handler: Deluge.Menus.onTorrentAction,
		scope: Deluge.Menus
	}, {
		id: 'move',
		text: _('Move Storage'),
		icon: '/icons/16/move.png',
		handler: Deluge.Menus.onTorrentAction,
		scope: Deluge.Menus
	}]
});

Deluge.Menus.Connections = new Ext.menu.Menu({
	id: 'connectionsMenu',
	items: [{
		id: '50',
		text: '50',
		group: 'max_connections_global',
		checked: false,
		checkHandler: onLimitChanged
	},{
		id: '100',
		text: '100',
		group: 'max_connections_global',
		checked: false,
		checkHandler: onLimitChanged
	},{
		id: '200',
		text: '200',
		group: 'max_connections_global',
		checked: false,
		checkHandler: onLimitChanged
	},{
		id: '300',
		text: '300',
		group: 'max_connections_global',
		checked: false,
		checkHandler: onLimitChanged
	},{
		id: '500',
		text: '500',
		group: 'max_connections_global',
		checked: false,
		checkHandler: onLimitChanged
	},{
		id: '-1',
		text: 'Unlimited',
		group: 'max_connections_global',
		checked: false,
		checkHandler: onLimitChanged
	},'-',{
		id: 'other',
		text: 'Other',
		group: 'max_connections_global',
		checked: false,
		checkHandler: onLimitChanged
	}]
});

Deluge.Menus.Download = new Ext.menu.Menu({
	id: 'downspeedMenu',
	items: [{
		id: '5',
		text: '5 KiB/s',
		group: 'max_download_speed',
		checked: false,
		checkHandler: onLimitChanged
	},{
		id: '10',
		text: '10 KiB/s',
		group: 'max_download_speed',
		checked: false,
		checkHandler: onLimitChanged
	},{
		id: '30',
		text: '30 KiB/s',
		group: 'max_download_speed',
		checked: false,
		checkHandler: onLimitChanged
	},{
		id: '80',
		text: '80 KiB/s',
		group: 'max_download_speed',
		checked: false,
		checkHandler: onLimitChanged
	},{
		id: '300',
		text: '300 KiB/s',
		group: 'max_download_speed',
		checked: false,
		checkHandler: onLimitChanged
	},{
		id: '-1',
		text: 'Unlimited',
		group: 'max_download_speed',
		checked: false,
		checkHandler: onLimitChanged
	},'-',{
		id: 'other',
		text: 'Other',
		group: 'max_download_speed',
		checked: false,
		checkHandler: onLimitChanged
	}]
});

Deluge.Menus.Upload = new Ext.menu.Menu({
	id: 'upspeedMenu',
	items: [{
		id: '5',
		text: '5 KiB/s',
		group: 'max_upload_speed',
		checked: false,
		checkHandler: onLimitChanged
	},{
		id: '10',
		text: '10 KiB/s',
		group: 'max_upload_speed',
		checked: false,
		checkHandler: onLimitChanged
	},{
		id: '30',
		text: '30 KiB/s',
		group: 'max_upload_speed',
		checked: false,
		checkHandler: onLimitChanged
	},{
		id: '80',
		text: '80 KiB/s',
		group: 'max_upload_speed',
		checked: false,
		checkHandler: onLimitChanged
	},{
		id: '300',
		text: '300 KiB/s',
		group: 'max_upload_speed',
		checked: false,
		checkHandler: onLimitChanged
	},{
		id: '-1',
		text: 'Unlimited',
		group: 'max_upload_speed',
		checked: false,
		checkHandler: onLimitChanged
	},'-',{
		id: 'other',
		text: 'Other',
		group: 'max_upload_speed',
		checked: false,
		checkHandler: onLimitChanged
	}]
});

function onLimitChanged(item, checked) {
	if (item.id == "other") {
	} else {
		config = {}
		config[item.group] = item.id
		Deluge.Client.core.set_config(config, {
			onSuccess: function() {
				Deluge.Ui.update();
			}
		});
	}
}