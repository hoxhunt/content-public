import os
import glob
import yaml
import re

# Define the base directory
base_dir = '/Users/iapt/dev/demisto/content/Packs'

# def get_marketplace_name(yaml_data):
#     if "marketplaces" not in yaml_data or not yaml_data["marketplaces"]:
#         return ""

#     xsoar_keys = {"xsoar", "xsoar_saas", "xsoar_on_prem"}
#     if any(key in yaml_data.get("marketplaces", []) for key in xsoar_keys):
#         return "" if "marketplacev2" in yaml_data.get("marketplaces", []) else "XSOAR"

#     return "XSIAM" if "marketplacev2" in yaml_data.get("marketplaces", []) else "XSOAR"

def update_readme(integration_name, readme_content):
    conf_xsoar = r"Configure (.+?) on Cortex (.+?)"
    match = re.search(conf_xsoar, readme_content)
    replacements = {}
    if match:
        wildcard_value = match.group(1)
        cortex_variant = match.group(2)
        conf_xsoar = f"Configure {wildcard_value} on Cortex {cortex_variant}"
    navigation1 = "1. Navigate to **Settings** > **Integrations** > **Servers & Services**."
    navigation2_pattern = "2. Search for (.+?)"
    match1 = re.search(navigation2_pattern, readme_content)
    if match1:
        name_of_integration = match1.group(1)
        navigation2 = f"2. Search for {name_of_integration}"
        if navigation2 in readme_content:
            replacements[navigation2] = ""
    navigation3 = "3. Click Add instance to create and configure a new integration instance."
    navigation4 = "4. Click Test to validate the URLs, token, and connection."
    cortex_cli_pattern = "You can execute these commands from the Cortex (.+?) CLI"
    match2 = re.search(cortex_cli_pattern, readme_content)
    if match2:
        cortex_variant = match2.group(1)
        cortex_cli = f"You can execute these commands from the Cortex {cortex_variant} CLI"
        if cortex_cli in readme_content:
            replacements[cortex_cli] = "You can execute these commands from the CLI"
    if conf_xsoar in readme_content:
        replacements[conf_xsoar] = f"Configure {wildcard_value if wildcard_value else integration_name} in Cortex"
    if navigation1 in readme_content:
        replacements[navigation1] = ""
    if navigation3 in readme_content:
        replacements[navigation3] = ""
    if navigation4 in readme_content:
        replacements[navigation4] = ""
   
    return replacements
        

def process_files(readme_path, yml_content):
    try:
        yaml_data = yaml.safe_load(yml_content)
        with open(readme_path, 'r+') as readme_file:
            readme_content = readme_file.read()
            
            replacements = update_readme(yaml_data.get('display'), readme_content)
            
            # Perform replacements
            updated_content = readme_content
            for old_sentence, new_sentence in replacements.items():
                updated_content = updated_content.replace(old_sentence, new_sentence)
            
            # Write the updated content back to README.md
            readme_file.seek(0)
            readme_file.write(updated_content)
            readme_file.truncate()
    except yaml.YAMLError as exc:
        print(f"Error parsing YAML: {exc}")


# Iterate through each pack in the packs directory
for pack_path in glob.glob(os.path.join(base_dir, 'A*')):
    if os.path.isdir(pack_path):  # Ensure it's a directory
        integrations_path = os.path.join(pack_path, 'integrations')
        
        if os.path.isdir(integrations_path):
            # Iterate through each integration in the integrations directory
            for integration_path in glob.glob(os.path.join(integrations_path, '*')):
                if os.path.isdir(integration_path):  # Ensure it's a directory
                    integration_name = os.path.basename(integration_path)
                    readme_path = os.path.join(integration_path, 'README.md')
                    yml_file = os.path.join(integration_path, f'{integration_name}.yml')
                    if os.path.isfile(readme_path) and os.path.isfile(yml_file):
                        with open(yml_file, 'r') as yml_file_content:
                            yml_content = yml_file_content.read()
                        
                        process_files(readme_path, yml_content)
        