package dev.aicivilization.plugin.api;

import org.bukkit.entity.Player;
import org.bukkit.Location;
import org.bukkit.block.Block;
import java.util.List;
import java.util.concurrent.CompletableFuture;

public class ControllerApi {
    private final String baseUrl;
    private final String apiKey;

    public ControllerApi(String baseUrl, String apiKey) {
        this.baseUrl = baseUrl;
        this.apiKey = apiKey;
    }

    public CompletableFuture<Void> notifyAgentJoined(Player player) {
        return CompletableFuture.runAsync(() -> {
            // In production: POST to AI Controller /agents endpoint.
        });
    }

    public CompletableFuture<Void> notifyAgentLeft(Player player) {
        return CompletableFuture.runAsync(() -> {
            // In production: POST to AI Controller.
        });
    }

    public CompletableFuture<Void> notifyAgentDied(org.bukkit.event.entity.PlayerDeathEvent event) {
        return CompletableFuture.runAsync(() -> {
            // In production: POST death event to AI Controller.
        });
    }

    public CompletableFuture<Void> sendObservation(Player player, Observation obs) {
        return CompletableFuture.runAsync(() -> {
            // In production: POST observation to AI Controller.
        });
    }

    public CompletableFuture<Action> requestAction(String agentId) {
        return CompletableFuture.supplyAsync(() -> {
            // In production: GET action from AI Controller.
            return null;
        });
    }

    public static class Observation {
        public String agentId;
        public Location location;
        public double health;
        public int hunger;
        public List<Block> nearbyBlocks;
        public List<Player> nearbyPlayers;
        public long timestamp;
    }

    public static class Action {
        public String type;
        public String target;
        public java.util.Map<String, Object> params;
    }
}
