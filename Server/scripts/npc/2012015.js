/*
	This file is part of the OdinMS Maple Story Server
    Copyright (C) 2008 Patrick Huy <patrick.huy@frz.cc> 
                       Matthias Butz <matze@odinms.de>
                       Jan Christian Meyer <vimes@odinms.de>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License version 3
    as published by the Free Software Foundation. You may not use, modify
    or distribute this program under any other version of the
    GNU Affero General Public License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

/**
 -- Odin JavaScript --------------------------------------------------------------------------------
 El Nath Magic Spot - Orbis Tower <20th Floor>(200080200)
 -- By ---------------------------------------------------------------------------------------------
 Unknown
 -- Version Info -----------------------------------------------------------------------------------
 1.2 - Now official version (action(1,0,0) is stupid) by Moogra
 1.1 - Official Text and Method [Information]
 1.0 - First Version by Unknown
 ---------------------------------------------------------------------------------------------------
 **/

var teleportCost = 5000;    // MapleStoryPlus: the tower stones cost mesos instead of a rock scroll

function start() {
    if (cm.getMeso() >= teleportCost) {
        cm.sendYesNo("For #b" + teleportCost + " mesos#k you can activate #b#p2012014##k. Will you teleport to where #b#p2012015##k is?");
    } else {
        cm.sendOk("There's a #b#p2012015##k that'll enable you to teleport to where #b#p2012014##k is, but it costs #b" + teleportCost + " mesos#k to activate.");
        cm.dispose();
    }
}

function action(mode, type, selection) {
    if (mode > 0) {
        if (cm.getMeso() < teleportCost) {
            cm.dispose();
            return;
        }
        cm.gainMeso(-teleportCost);
        cm.warp(200080200, 0);
    }
    cm.dispose();
}
