package dev.aicivilization.plugin;

import dev.aicivilization.plugin.api.ControllerApi;
import dev.aicivilization.plugin.listener.AgentListener;
import dev.aicivilization.plugin.listener.WorldListener;
import org.bukkit.plugin.java.JavaPlugin;

public class AICivilizationPlugin extends JavaPlugin {
    private static AICivilizationPlugin instance;
    private ControllerApi controllerApi;

    @Override
    public void onEnable() {
        instance = this;
        saveDefaultConfig();

        String apiUrl = getConfig().getString("controller.api-url", "http://localhost:8000");
        String apiKey = getConfig().getString("controller.api-key", "changeme");
        this.controllerApi = new ControllerApi(apiUrl, apiKey);

        getServer().getPluginManager().registerEvents(new AgentListener(this, controllerApi), this);
        getServer().getPluginManager().registerEvents(new WorldListener(this, controllerApi), this);

        getLogger().info("AI Civilization Plugin enabled.");
    }

    @Override
    public void onDisable() {
        getLogger().info("AI Civilization Plugin disabled.");
    }

    public static AICivilizationPlugin getInstance() {
        return instance;
    }

    public ControllerApi getControllerApi() {
        return controllerApi;
    }
}
