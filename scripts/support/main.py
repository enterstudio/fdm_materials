import os
import sys

from gitHubConnector import GitHubConnector
from materialFileReader import MaterialFileReader
from materialsOutputFormatter import MaterialsOutputFormatter


def main():

    working_fld = "/var/tmp/fdm_material_overview"
    github_url = "git@github.com:Ultimaker/fdm_materials.git"
    generated_file = "mat_overview.html"
    additional_devices = set(sys.argv[1:])

    nozzle_lookup = {
        "Ultimaker 2 Extended+": ["0.25 mm", "0.4 mm", "0.6 mm", "0.8 mm"],
        "Ultimaker 2+": ["0.25 mm", "0.4 mm", "0.6 mm", "0.8 mm"],
        "Ultimaker 3": ["AA 0.25", "AA 0.4", "AA 0.8", "BB 0.4", "BB 0.8"],
        "Ultimaker 3 Extended": ["AA 0.25", "AA 0.4", "AA 0.8", "BB 0.4", "BB 0.8"]
    }

    try:
        os.mkdir(working_fld)
    except OSError:
        pass

    github_connector = GitHubConnector(working_fld, github_url)
    github_connector.getSourceFiles()

    material_reader = MaterialFileReader(working_fld)
    materials = material_reader.read()

    materials_output_formatter = MaterialsOutputFormatter()

    filtered_devices = material_reader.all_devices
    filtered_devices.remove("IMADE3D JellyBOX")
    filtered_devices.remove("cartesio")
    filtered_devices.remove("Ultimaker 2")
    filtered_devices.remove("Ultimaker 2 Extended")
    filtered_devices.remove("Ultimaker 2 Go")
    filtered_devices.remove("Ultimaker Original")

    html = materials_output_formatter.toHtml(
        materials,
        filtered_devices | additional_devices,
        material_reader.all_nozzles,
        nozzle_lookup
    )

    file = open(os.path.join(working_fld, generated_file), "w")
    file.write(html)
    sys.exit(0)

if __name__ == "__main__":
    main()