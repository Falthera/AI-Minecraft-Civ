package dev.aicivilization.plugin.listener;

import dev.aicivilization.plugin.AICivilizationPlugin;
import dev.aicivilization.plugin.api.ControllerApi;
import org.bukkit.entity.Player;
import org.bukkit.event.EventHandler;
import org.bukkit.event.Listener;
import org.bukkit.event.player.PlayerJoinEvent;
import org.bukkit.event.player.PlayerQuitEvent;
import org.bukkit.event.entity.PlayerDeathEvent;

public class AgentListener implements Listener {
    private final AICivilizationPlugin plugin;
    private final ControllerApi controllerApi;

    public AgentListener(AICivilizationPlugin plugin, ControllerApi controllerApi) {
        this.plugin = plugin;
        this.controllerApi = controllerApi;
    }

    @EventHandler
    public void onPlayerJoin(PlayerJoinEvent event) {
        Player player = event.getPlayer();
        controllerApi.notifyAgentJoined(player);
    }

    @EventHandler
    public void onPlayerQuit(PlayerQuitEvent event) {
        Player player = event.getPlayer();
        controllerApi.notifyAgentLeft(player);
    }

    @EventHandler
    public void onPlayerDeath(PlayerDeathEvent event) {
        controllerApi.notifyAgentDied(event);
    }
}
