provider "azurerm" {
    features {}
}


data "azurerm_resource_group" "rg" {
    name                             = "fluffbot"
}

data "azurerm_container_registry" "registry" {
    name                             = "myacr"
    resource_group_name              = "myacr"
}

data "azurerm_key_vault" "myKeyVault" {
    name                             = "myKeyVault"
    resource_group_name              = "keyvault"
}

data "azurerm_key_vault_secret" "app" {
    name                             = "SLACKAPPTOKEN"
    key_vault_id                     = data.azurerm_key_vault.myKeyVault.id
}

data "azurerm_key_vault_secret" "bot" {
    name                             = "SLACKBOTTOKEN"
    key_vault_id                     = data.azurerm_key_vault.myKeyVault.id
}


resource "azurerm_container_group" "container" {
    name                             = "fluffbot"
    location                         = data.azurerm_resource_group.rg.location
    resource_group_name              = data.azurerm_resource_group.rg.name
    ip_address_type                  = "None"
    dns_name_label                   = "fluffbot"
    os_type                          = "Linux"
    restart_policy                   = "Always"

    container {
        name                         = "fluffbot"
        image                        = "${data.azurerm_container_registry.registry.login_server}/fluffbot"
        cpu                          = "1"
        memory                       = "1.5"

        secure_environment_variables = {
            SLACK_APP_TOKEN          = data.azurerm_key_vault_secret.app.value
            SLACK_BOT_TOKEN          = data.azurerm_key_vault_secret.bot.value
        }
    }

    image_registry_credential {
        password                     = data.azurerm_container_registry.registry.admin_password
        server                       = data.azurerm_container_registry.registry.login_server
        username                     = data.azurerm_container_registry.registry.admin_username
    }
}