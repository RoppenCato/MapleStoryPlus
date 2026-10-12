package client.command.commands.gm0;

import client.Client;
import client.command.Command;

// MapleStoryPlus: a quick look at what stands between you and your next job
public class GoalsCommand extends Command {
    {
        setDescription("Show what you need for your next job advancement.");
    }

    @Override
    public void execute(Client client, String[] params) {
        for (String line : plus.Trials.goals(client.getPlayer())) {
            client.getPlayer().yellowMessage(line);
        }
    }
}
