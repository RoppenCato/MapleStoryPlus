/*
	This file is part of the OdinMS Maple Story Server
    Copyright (C) 2008 Patrick Huy <patrick.huy@frz.cc>
		       Matthias Butz <matze@odinms.de>
		       Jan Christian Meyer <vimes@odinms.de>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation version 3 as published by
    the Free Software Foundation. You may not use, modify or distribute
    this program under any other version of the GNU Affero General Public
    License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

/*      Author: Xterminator, Moogra
	NPC Name: 		First Eos Rock
	Map(s): 		Ludibrium : Eos Tower 100th Floor (221024400)
	Description: 		Brings you to 71st Floor
*/

var teleportCost = 5000;    // MapleStoryPlus: the tower stones cost mesos instead of a rock scroll

function start() {
    if (cm.getMeso() >= teleportCost) {
        cm.sendYesNo("For #b" + teleportCost + " mesos#k you can activate #bFirst Eos Rock#k. Will you teleport to #bSecond Eos Rock#k at the 71st floor?");
    } else {
        cm.sendOk("There's a rock that will enable you to teleport to #bSecond Eos Rock#k, but it costs #b" + teleportCost + " mesos#k to activate.");
        cm.dispose();
    }
}

function action(mode, type, selection) {
    if (mode < 1) {
    } else {
        if (cm.getMeso() < teleportCost) {
            cm.dispose();
            return;
        }
        cm.gainMeso(-teleportCost);
        cm.warp(221022900, 3);
    }
    cm.dispose();
}