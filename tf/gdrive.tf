


/*resource "null_resource" "gdrice_folder" {
  triggers = {
    bq_dataset = var.dataset_name
  }

  provisioner "local-exec" {
    command = "cp -rf ../installation_scripts/Create_GDrive_folder.py aux_data/; source venv/bin/activate; python3 aux_data/Create_GDrive_folder.py --folder_name=\"${var.gdrive_folder_name}\" --service_account_email=\"${module.genai_service_account.email}\"}"
  }
  depends_on=[null_resource.py_venv, module.genai_service_account]
}*/