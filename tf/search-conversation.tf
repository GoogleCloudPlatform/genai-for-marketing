

resource "null_resource" "genai_marketing_search_app_creation" {
  triggers = {
    bq_dataset = var.dataset_name
  }

  provisioner "local-exec" {
    command = "cp -rf ../installation_scripts/genai_marketing_search_app_creation.py aux_data/; source venv/bin/activate; cd aux_data/; python3 genai_marketing_search_app_creation.py --project=\"${var.project_id}\" --app-name=\"${var.search_app_name}\" --company-name=\"${var.company_name}\" --uris=\"${var.datastore_uris}\""
  }
  depends_on = [null_resource.py_venv]
}


resource "null_resource" "genai_marketing_conversation_app_creation" {
  triggers = {
    bq_dataset = var.dataset_name
  }

  provisioner "local-exec" {
    command = "cp -rf ../installation_scripts/genai_marketing_conversation_app_creation.py aux_data/; source venv/bin/activate; cd aux_data/; python3 genai_marketing_conversation_app_creation.py --project=\"${var.project_id}\" --location=\"global\" --app-name=\"${var.chat_bot_name}\" --company-name=\"${var.company_name}\" --uris=\"${var.datastore_uris}\" --datastore-storage-folder=\"${var.datastore_storage_folder}\""
  }
  depends_on = [null_resource.py_venv]
}
