/**
 MapleStoryPlus: King Slime as an area boss.

 In the original game King Slime only lives at the end of the Kerning party quest, which one player
 cannot enter. He is one of the two trials for 2nd job, so he also appears in the swamp next to
 Kerning City. Modelled on the Mano spawner.
 **/

var KING_SLIME = 9300003;
var SWAMP_OF_DESPAIR_1 = 107000000;
var CHECK_EVERY = 15 * 60 * 1000;

function init() {
    scheduleNew();
}

function scheduleNew() {
    setupTask = em.schedule("start", 0);
}

function cancelSchedule() {
    if (setupTask != null) {
        setupTask.cancel(true);
    }
}

function start() {
    var swamp = em.getChannelServer().getMapFactory().getMap(SWAMP_OF_DESPAIR_1);
    if (swamp.getMonsterById(KING_SLIME) != null) {
        em.schedule("start", CHECK_EVERY);
        return;
    }
    const LifeFactory = Java.type('server.life.LifeFactory');
    const Point = Java.type('java.awt.Point');
    const PacketCreator = Java.type('tools.PacketCreator');
    swamp.spawnMonsterOnGroundBelow(LifeFactory.getMonster(KING_SLIME), new Point(-225, -449));
    swamp.broadcastMessage(PacketCreator.serverNotice(6, "The swamp bubbles as King Slime rises from the mud."));
    em.schedule("start", CHECK_EVERY);
}

// ---------- FILLER FUNCTIONS ----------

function dispose() {}

function setup(eim, leaderid) {}

function monsterValue(eim, mobid) {return 0;}

function disbandParty(eim, player) {}

function playerDisconnected(eim, player) {}

function playerEntry(eim, player) {}

function monsterKilled(mob, eim) {}

function scheduledTimeout(eim) {}

function afterSetup(eim) {}

function changedMap(eim, chr, mapid) {}

function changedLeader(eim, leader) {}

function playerExit(eim, player) {}

function leftParty(eim, player) {}

function clearPQ(eim) {}

function allMonstersDead(eim) {}

function playerUnregistered(eim, player) {}
