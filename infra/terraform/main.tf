terraform {
    required_version = ">= 1.0"

    required_providers {
        azurerm = {
            source = "hashicorp/azurerm"
            version = "~> 3.0"
        }
    }
}

# Optional: Store state remotely
# backend "azurerm" {
#    resource_group_name = "tfstate-rg"
#    storage_account_name = "tfstatestorage"
#    container_name = "tfstate"
#    key = "test.terraform.tfstate"
# }

provider "azurerm" {
    features {}
}

resource "azurerm_resource_group" "main" {
    name = var.resource_group_name
    location = var.location

    tags = {
        Owner = var.owner_email
    }
}