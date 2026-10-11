package plus;

import client.Character;
import client.Client;
import client.inventory.Item;
import config.YamlConfig;
import constants.inventory.ItemConstants;
import net.server.Server;
import server.ItemInformationProvider;
import server.maps.PlayerShopItem;
import soloMapling.FreeMarket.HiredMerchantArtificial;
import tools.PacketCreator;

import java.awt.Point;
import java.io.File;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.TreeMap;

/**
 * MapleStoryPlus: set shops in the Free Market that always sell what a player needs.
 * <p>
 * The shops are listed in {@code Fixed-Shops.tsv}, next to the settings file (written by
 * {@code Settings/Scripts/Make-Fixed-Shops.py}). A Free Market room named in that file gets these shops
 * instead of random ones. Their stock never runs out and their prices do not move.
 */
public class FixedShops {
    private static final org.slf4j.Logger log = org.slf4j.LoggerFactory.getLogger(FixedShops.class);
    private static final int STOCK = 999;           // shown as the amount left; refilled after every purchase
    private static final int[] STORE_LOOKS = {5030000, 5030001, 5030002, 5030004, 5030008, 5030010};
    private static final int OWNER_ID_BASE = 19000; // below the ids the random shops use (20000 and up)

    private record Entry(int itemId, int price) {}

    // room -> spot -> shop title -> items
    private static Map<Integer, Map<Integer, Map.Entry<String, List<Entry>>>> rooms;

    private static synchronized void load() {
        if (rooms != null) {
            return;
        }
        rooms = new LinkedHashMap<>();
        File settings = new File(YamlConfig.CONFIG_FILE_NAME).getAbsoluteFile().getParentFile();
        File file = new File(settings, "Fixed-Shops.tsv");
        if (!file.exists()) {
            return;
        }
        try {
            List<String> lines = Files.readAllLines(file.toPath(), StandardCharsets.UTF_8);
            for (String line : lines.subList(1, lines.size())) {
                String[] cell = line.split("\t");
                if (cell.length < 6) {
                    continue;
                }
                int room = Integer.parseInt(cell[0]);
                int spot = Integer.parseInt(cell[1]);
                rooms.computeIfAbsent(room, r -> new TreeMap<>())
                        .computeIfAbsent(spot, s -> Map.entry(cell[2], new ArrayList<>()))
                        .getValue().add(new Entry(Integer.parseInt(cell[3]), Integer.parseInt(cell[5])));
            }
        } catch (Exception e) {
            System.err.println("Fixed-Shops.tsv could not be read: " + e);
            rooms.clear();
        }
    }

    /** Fills the room with its set shops. Returns false if the room has none, so the caller fills it at random. */
    public static boolean fill(int mapId, List<Point> positions) {
        load();
        Map<Integer, Map.Entry<String, List<Entry>>> shops = rooms.get(mapId);
        if (shops == null) {
            return false;
        }
        int opened = 0;
        for (Map.Entry<Integer, Map.Entry<String, List<Entry>>> shop : shops.entrySet()) {
            int spot = shop.getKey();
            if (spot >= positions.size()) {
                System.err.println("Fixed shop '" + shop.getValue().getKey() + "' has no spot in room " + mapId);
                continue;
            }
            try {
                open(mapId, positions.get(spot), spot, shop.getValue().getKey(), shop.getValue().getValue());
                opened++;
            } catch (Exception e) {
                log.error("Fixed shop '{}' could not be opened", shop.getValue().getKey(), e);
            }
        }
        log.info("Fixed shops: opened {} of {} in Free Market room {}", opened, shops.size(), mapId % 100);
        return true;
    }

    private static void open(int mapId, Point position, int spot, String title, List<Entry> entries) {
        Client client = Client.createMock();
        Character owner = Character.getDefault(client);
        client.setPlayer(owner);     // the item data asks the client's character about stack sizes
        owner.setPosition(position);
        owner.setMap(Server.getInstance().getChannel(0, 1).getMapFactory().getMap(mapId));

        int look = STORE_LOOKS[spot % STORE_LOOKS.length];
        Merchant merchant = new Merchant(owner, title, look, OWNER_ID_BASE + (mapId % 100) * 100 + spot, "MaplePlus");
        merchant.setTier("A");
        merchant.setMapId(mapId);
        owner.setHiredMerchant(merchant);
        owner.getWorldServer().registerHiredMerchant(merchant);
        owner.getWorldServer().getChannel(1).addHiredMerchant(owner.getId(), merchant);

        ItemInformationProvider ii = ItemInformationProvider.getInstance();
        for (Entry entry : entries) {
            Item item;
            if (entry.itemId() < 2000000) {
                item = ii.getEquipById(entry.itemId());
            } else {
                // Throwing stars and bullets are sold as one full set
                short amount = ItemConstants.isRechargeable(entry.itemId()) ? ii.getSlotMax(client, entry.itemId()) : 1;
                item = new Item(entry.itemId(), (short) 0, amount);
            }
            merchant.addItem(new PlayerShopItem(item, (short) STOCK, entry.price()));
        }

        owner.setHasMerchant(true);
        merchant.setOpen(true);
        merchant.getMap().addMapObject(merchant);
        owner.setHiredMerchant(null);
        merchant.getMap().broadcastMessage(PacketCreator.spawnHiredMerchantBox(merchant));
    }

    /** A shop whose shelves are full again after every purchase. */
    private static class Merchant extends HiredMerchantArtificial {
        Merchant(Character owner, String title, int look, int ownerId, String ownerName) {
            super(owner, title, look, ownerId, ownerName);
        }

        @Override
        public void buy(Client c, int item, short quantity) {
            super.buy(c, item, quantity);
            for (PlayerShopItem shelf : getItems()) {
                shelf.setBundles((short) STOCK);
                shelf.setDoesExist(true);
            }
        }

        @Override
        public void saveItems(boolean shutdown) {
            // Nothing to save: the stock comes from Fixed-Shops.tsv at every start.
        }
    }
}
