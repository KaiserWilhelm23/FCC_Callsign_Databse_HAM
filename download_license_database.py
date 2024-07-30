import os
import zipfile
import urllib.request
import shutil

# Define URLs and paths
url = 'ftp://wirelessftp.fcc.gov/pub/uls/complete/l_amat.zip'
zip_file_name = 'l_amat.zip'
extract_dir = 'l_amat_unzipped'
en_dat_file_name = 'EN.dat'

# Function to download the file
def download_file(url, local_filename):
    with urllib.request.urlopen(url) as response:
        with open(local_filename, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)

# Function to unzip the file
def unzip_file(zip_file, extract_to):
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

# Function to move the EN.dat file
def move_en_dat_file(source_dir, destination):
    source_path = os.path.join(source_dir, en_dat_file_name)
    destination_path = os.path.join(destination, en_dat_file_name)
    if os.path.exists(source_path):
        shutil.copy(source_path, destination_path)
    else:
        print(f"{en_dat_file_name} not found in {source_dir}")

# Function to clean up
def cleanup(files_and_dirs):
    for path in files_and_dirs:
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)

# Main script logic
if __name__ == "__main__":
    # Download the ZIP file
    print("This will download the database in the same directory that this app is run in. ")
    input("Welcome the FCC database downloader for HAMS. Press ENTER to start download:")
    print("Downloading the ZIP file...")
    download_file(url, zip_file_name)

    # Unzip the file
    print("Unzipping the file...")
    os.makedirs(extract_dir, exist_ok=True)
    unzip_file(zip_file_name, extract_dir)

    # Move the EN.dat file
    print("Moving EN.dat file...")
    move_en_dat_file(extract_dir, '.')

    # Clean up
    print("Cleaning up...")
    cleanup([zip_file_name, extract_dir])

    print("Done.")

    input("Press enter to EXIT... ")
