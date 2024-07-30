import os
import zipfile
import urllib.request
import shutil
from colorama import init, Fore, Style

# Initialize Colorama
init(autoreset=True)

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

# Function to search for a call sign in the file
def search_call_sign_in_file(call_sign):
    results = []
    if os.path.exists(en_dat_file_name):
        with open(en_dat_file_name, 'r') as file:
            for line in file:
                parts = line.strip().split('|')
                if len(parts) > 20 and call_sign in parts[4]:
                    callsign = parts[4]
                    name = parts[7] if len(parts) > 7 else 'N/A'
                    first_name = parts[8] if len(parts) > 8 else ''
                    last_name = parts[10] if len(parts) > 10 else ''
                    address = f"{parts[14]}, {parts[15]}, {parts[16]}, {parts[17]}" if len(parts) > 17 else 'N/A'
                    license_number = parts[6] if len(parts) > 6 else 'N/A'
                    frn = parts[22] if len(parts) > 22 else ''
                    full_name = f"{first_name} {last_name}".strip() if first_name or last_name else name
                    results.append((callsign, full_name, address, license_number, frn))
    return results

# Function to display results with color
def display_results(results):
    formatted_results = []
    for result in results:
        formatted_result = f"""
{Fore.GREEN + Style.BRIGHT}Call Sign:         {Fore.RESET}{result[0]}
{Fore.BLUE + Style.BRIGHT}Name:              {Fore.RESET}{result[1]}
{Fore.CYAN + Style.BRIGHT}Address:          {Fore.RESET}{result[2]}
{Fore.MAGENTA + Style.BRIGHT}License Number:    {Fore.RESET}{result[3]}
{Fore.YELLOW + Style.BRIGHT}FRN:               {Fore.RESET}{result[4]}
        """
        formatted_results.append(formatted_result.strip())
    return '\n\n'.join(formatted_results)

# Function to clear the screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Main script logic
def main():
    clear_screen()
    if os.path.exists(en_dat_file_name):
        print(f"{Fore.GREEN}The {en_dat_file_name} file already exists.")
        download_choice = input(f"{Fore.CYAN}Do you want to download it again? (y/n): ")
        if download_choice.lower() == 'y':
            clear_screen()
            print(f"{Fore.YELLOW}Downloading the ZIP file...")
            download_file(url, zip_file_name)

            clear_screen()
            print(f"{Fore.YELLOW}Unzipping the file...")
            os.makedirs(extract_dir, exist_ok=True)
            unzip_file(zip_file_name, extract_dir)

            clear_screen()
            print(f"{Fore.YELLOW}Moving EN.dat file...")
            move_en_dat_file(extract_dir, '.')

            clear_screen()
            print(f"{Fore.YELLOW}Cleaning up...")
            cleanup([zip_file_name, extract_dir])
        else:
            clear_screen()
            print(f"{Fore.GREEN}Using the existing {en_dat_file_name} file.")
    else:
        clear_screen()
        print(f"{Fore.CYAN}This will download the database in the same directory that this app is run in.")
        input(f"{Fore.GREEN}Welcome to the FCC database downloader for HAMs. Press ENTER to start download:")
        clear_screen()
        print(f"{Fore.YELLOW}Downloading the ZIP file...")
        download_file(url, zip_file_name)

        clear_screen()
        print(f"{Fore.YELLOW}Unzipping the file...")
        os.makedirs(extract_dir, exist_ok=True)
        unzip_file(zip_file_name, extract_dir)

        clear_screen()
        print(f"{Fore.YELLOW}Moving EN.dat file...")
        move_en_dat_file(extract_dir, '.')

        clear_screen()
        print(f"{Fore.YELLOW}Cleaning up...")
        cleanup([zip_file_name, extract_dir])

    clear_screen()
    print(f"{Fore.GREEN}Setup complete.")

    while True:
        call_sign = input(f"{Fore.GREEN}Enter a call sign to search (or type 'exit' to quit): ")
        if call_sign.lower() == 'exit':
            break
        clear_screen()
        results = search_call_sign_in_file(call_sign)
        if results:
            print(display_results(results))
        else:
            print(f"{Fore.RED}No results found for call sign: {call_sign}")

if __name__ == "__main__":
    main()
