/*
    MapleStoryPlus: the Guide. Opened with the Trade button anywhere, and by the job instructors.

    Shows where you stand, lets you advance your job when you are ready, and lists the trials (the bosses
    to beat). Everything it says and decides is in the server code, plus/Trials.java; this script only
    shows the pages. The bosses are listed in Settings/Trials.tsv.
*/
var status = -1;
var chosenJob = 0;
var onJobPage = false;
var onSkillShop = false;
var chosenSkill = 0;

function start() {
    status = -1;
    action(1, 0, 0);
}

function action(mode, type, selection) {
    if (mode != 1) {
        cm.dispose();
        return;
    }
    const Trials = Java.type('plus.Trials');
    var chr = cm.getPlayer();
    status++;

    if (status == 0) {
        cm.sendSimple(Trials.menu(chr));
    } else if (status == 1) {
        if (selection == 0) {
            if (Trials.canAdvance(chr)) {
                onJobPage = true;
                cm.sendSimple(Trials.jobPage(chr));
            } else {
                cm.sendOk(Trials.jobPage(chr));
                cm.dispose();
            }
        } else if (selection == 1) {
            cm.sendOk(Trials.trialsPage(chr));
            cm.dispose();
        } else if (Trials.hasSkillShop(chr)) {
            onSkillShop = true;
            cm.sendSimple(Trials.fourthJobPage(chr));
        } else {
            cm.sendOk(Trials.fourthJobPage(chr));
            cm.dispose();
        }
    } else if (status == 2 && onSkillShop) {
        chosenSkill = selection;
        var question = Trials.confirmSkill(chr, chosenSkill);
        if (question == "") {
            cm.sendOk("That skill's limit is already as high as it goes.");
            cm.dispose();
        } else {
            cm.sendYesNo(question);
        }
    } else if (status == 3 && onSkillShop) {
        cm.sendOk(Trials.buySkill(chr, chosenSkill));
        cm.dispose();
    } else if (status == 2 && onJobPage) {
        chosenJob = selection;
        cm.sendYesNo("Become a #e" + cm.getJobName(chosenJob) + "#n? This cannot be undone.");
    } else if (status == 3 && onJobPage) {
        cm.sendOk(Trials.advance(chr, chosenJob));
        cm.dispose();
    } else {
        cm.dispose();
    }
}
