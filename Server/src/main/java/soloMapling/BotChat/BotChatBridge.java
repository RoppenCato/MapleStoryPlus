package soloMapling.BotChat;

import client.Character;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import tools.PacketCreator;

import java.net.URI;
import java.net.URLEncoder;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.charset.StandardCharsets;
import java.time.Duration;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.stream.Collectors;

// MapleStoryPlus: hands a player's whisper to a bot over to the external chat bridge
// (Settings/Scripts/Bot-Chat-Bridge.py), which asks an LLM for the bot's reply. The reply comes back as
// plain text, one chat line per row, and the bot whispers each line to the player.
// If the bridge is not running the bot simply stays silent, as it did before.
public class BotChatBridge {
    private static final Logger log = LoggerFactory.getLogger(BotChatBridge.class);

    private static final String BRIDGE_URL = System.getProperty("bot-chat-url", "http://127.0.0.1:8585/chat");
    private static final Duration CONNECT_TIMEOUT = Duration.ofSeconds(2);
    private static final Duration REPLY_TIMEOUT = Duration.ofSeconds(90);
    // Pause before each line so it reads like typing rather than an instant answer.
    private static final long TYPING_MS_PER_CHAR = 45;
    private static final long TYPING_MS_MAX = 3500;
    private static final int MAX_LINE_LENGTH = 100;   // whispers longer than a signed byte are rejected

    private static final HttpClient HTTP = HttpClient.newBuilder().connectTimeout(CONNECT_TIMEOUT).build();

    public static void whisper(Character player, Character bot, String message) {
        Map<String, String> form = new LinkedHashMap<>();
        form.put("player", player.getName());
        form.put("bot", bot.getName());
        form.put("level", String.valueOf(bot.getLevel()));
        form.put("job", bot.getJob().name());
        form.put("map", String.valueOf(bot.getMapId()));
        form.put("text", message);
        String body = form.entrySet().stream()
                .map(e -> e.getKey() + "=" + URLEncoder.encode(e.getValue(), StandardCharsets.UTF_8))
                .collect(Collectors.joining("&"));
        int channel = player.getClient().getChannel() - 1;
        String botName = bot.getName();

        Thread.startVirtualThread(() -> {
            try {
                HttpRequest request = HttpRequest.newBuilder(URI.create(BRIDGE_URL))
                        .timeout(REPLY_TIMEOUT)
                        .header("Content-Type", "application/x-www-form-urlencoded")
                        .POST(HttpRequest.BodyPublishers.ofString(body))
                        .build();
                HttpResponse<String> response = HTTP.send(request, HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
                if (response.statusCode() != 200) {
                    return;
                }
                for (String line : response.body().split("\n")) {
                    line = line.strip();
                    if (line.isEmpty()) {
                        continue;
                    }
                    if (line.length() > MAX_LINE_LENGTH) {
                        line = line.substring(0, MAX_LINE_LENGTH);
                    }
                    Thread.sleep(Math.min(TYPING_MS_MAX, line.length() * TYPING_MS_PER_CHAR));
                    if (!player.isLoggedinWorld()) {
                        return;
                    }
                    player.sendPacket(PacketCreator.getWhisperReceive(botName, channel, false, line));
                }
            } catch (java.net.ConnectException | java.net.http.HttpConnectTimeoutException e) {
                // bridge not running - the bot stays silent
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            } catch (Exception e) {
                log.warn("Bot chat bridge call failed for {} -> {}", player.getName(), botName, e);
            }
        });
    }
}
