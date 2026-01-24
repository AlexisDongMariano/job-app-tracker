variable "resource_group_name" {
    type = string
    default = "adm-rg" 
}

variable "location" {
    description = "Azure region"
    type = string
    default = "canadacentral"
}

variable "vm_size" {
    type = string
    default = "Standard_B1s"
}

variable "admin_username" {
    type = string
    default = "localadmin"
}

variable "vm_name" {
    type = string
    default = "adm-1-vm"
}

variable "owner_email" {
    description = "Owner of the resource"
    type = string
}