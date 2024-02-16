module "vpc" {
    source  = "terraform-google-modules/network/google"
    version = "~> 9.0"

    project_id   = var.project_id
    network_name = "genai-vpc"
    routing_mode = "GLOBAL"

    subnets = [
        {
            subnet_name           = "genai-uc1-subnet"
            subnet_ip             = "10.0.1.0/24"
            subnet_region         = var.region
        },
        
    ]
}