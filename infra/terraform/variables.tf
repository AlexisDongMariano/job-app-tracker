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
    default = "Standard_B1ms"
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

variable "ssh_public_key" {
    description = "SSH public key for VM access"
    type = string
    sensitive = true
}

variable "my_public_ip" {
    description = "Your public IP address for NSG rules (use '*' for any IP, or specific IP like '1.2.3.4/32')"
    type = string
    default = "*"
}