package dev.aicivilization.plugin.listener;

import dev.aicivilization.plugin.AICivilizationPlugin;
import dev.aicivilization.plugin.api.ControllerApi;
import org.bukkit.entity.Player;
import org.bukkit.event.EventHandler;
import org.bukkit.event.Listener;
import org.bukkit.event.block.BlockBreakEvent;
import org.bukkit.event.block.BlockPlaceEvent;
import org.bukkit.event.player.PlayerInteractEvent;
import org.bukkit.event.player.PlayerItemConsumeEvent;
import org.bukkit.event.player.PlayerItemPickupEvent;
import org.bukkit.event.entity.EntityDamageEvent;
import org.bukkit.event.entity.EntityDeathEvent;
import org.bukkit.event.inventory.CraftItemEvent;
import org.bukkit.event.inventory.FurnaceSmeltEvent;
import org.bukkit.event.entity.EntityPickupItemEvent;
import org.bukkit.event.entity.EntityDropItemEvent;
import org.bukkit.event.player.AsyncPlayerChatEvent;

public class WorldListener implements Listener {
    private final AICivilizationPlugin plugin;
    private final ControllerApi controllerApi;

    public WorldListener(AICivilizationPlugin plugin, ControllerApi controllerApi) {
        this.plugin = plugin;
        this.controllerApi = controllerApi;
    }

    @EventHandler
    public void onBlockBreak(BlockBreakEvent event) {
        // In production: send event to AI Controller.
    }

    @EventHandler
    public void onBlockPlace(BlockPlaceEvent event) {
        // In production: send event to AI Controller.
    }

    @EventHandler
    public void onItemCraft(CraftItemEvent event) {
        // In production: send event to AI Controller.
    }

    @EventHandler
    public void onFurnaceSmelt(FurnaceSmeltEvent event) {
        // In production: send event to AI Controller.
    }

    @EventHandler
    public void onEntityDeath(EntityDeathEvent event) {
        // In production: send event to AI Controller.
    }

    @EventHandler
    public void onEntityDamage(EntityDamageEvent event) {
        // In production: send event to AI Controller.
    }

    @EventHandler
    public void onPlayerChat(AsyncPlayerChatEvent event) {
        // In production: send event to AI Controller.
    }

    @EventHandler
    public void onPlayerInteract(PlayerInteractEvent event) {
        // In production: send event to AI Controller.
    }

    @EventHandler
    public void onItemConsume(PlayerItemConsumeEvent event) {
        // In production: send event to AI Controller.
    }

    @EventHandler
    public void onItemPickup(PlayerItemPickupEvent event) {
        // In production: send event to AI Controller.
    }
}
