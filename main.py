import requests

# Stylish logo for BINof
def binof_logo():
    return '''
    
    $$\   $$\           $$\           $$\                           
    $$ | $$  |          \__|          $$ |                          
    $$ |$$  /  $$$$$$\  $$\  $$$$$$$\ $$$$$$$\  $$$$$$$\   $$$$$$\  
    $$$$$  /  $$  __$$\ $$ |$$  _____|$$  __$$\ $$  __$$\  \____$$\ 
    $$  $$<   $$ |  \__|$$ |\$$$$$$\  $$ |  $$ |$$ |  $$ | $$$$$$$ |
    $$ |\$$\  $$ |      $$ | \____$$\ $$ |  $$ |$$ |  $$ |$$  __$$ |
    $$ | \$$\ $$ |      $$ |$$$$$$$  |$$ |  $$ |$$ |  $$ |\$$$$$$$ |
    \__|  \__|\__|      \__|\_______/ \__|  \__|\__|  \__| \_______|
    '''

def is_vbv(card_number):
    vbv_indicator = card_number[0:6]
    vbv_bins = [
    "400115", "400117", "400118", "400119", "400135", "400136", "400137", "400138",
    "400139", "400175", "400344", "400345", "400346", "400347", "400348", "400349",
    "400350", "400351", "400352", "400353", "400354", "400355", "400356", "400357",
    "400358", "400359", "400360", "400361", "400362", "400363", "400364", "400365",
    "400366", "400367", "400368", "400369", "400370", "400371", "400372", "400373",
    "400374", "400375", "400376", "400377", "400378", "400379", "400380", "400381",
    # Add more VBV BINs here
]

    
    return vbv_indicator in vbv_bins

def get_bin_info(bin_number):
    url = f"https://lookup.binlist.net/{bin_number}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            bin_info = response.json()
            if bin_info:
                print(f"+++++++++++++++++BIN: {bin_number}")
                print(f"+++++++++++++++++Length: {bin_info.get('number', {}).get('length', 'N/A')}")
                print(f"+++++++++++++++++Card Type: {bin_info.get('type', 'N/A')}")
                print(f"+++++++++++++++++Brand: {bin_info.get('brand', 'N/A')}")
                print(f"+++++++++++++++++Country: {bin_info.get('country', {}).get('name', 'N/A')} {bin_info.get('country', {}).get('emoji', 'N/A')}")
                print(f"+++++++++++++++++Bank Name: {bin_info.get('bank', {}).get('name', 'N/A')}")
                print(f"+++++++++++++++++Bank URL: {bin_info.get('bank', {}).get('url', 'N/A')}")
                print(f"+++++++++++++++++Bank Phone: {bin_info.get('bank', {}).get('phone', 'N/A')}")
                print(f"+++++++++++++++++Bank City: {bin_info.get('bank', {}).get('city', 'N/A')}")
                print()
            else:
                print("Invalid BIN Input !!")
        else:
            print("Invalid BIN Input !!")
    except requests.exceptions.RequestException:
        print("Error: Unable to retrieve BIN information. Please check your internet connection.")
    except ValueError:
        print("Error: Invalid response from the BIN information service.")

def mass_bin_info(file_path):
    try:
        with open(file_path, 'r') as file:
            for line in file:
                bin_number = line.strip()
                get_bin_info(bin_number)
                if is_vbv(bin_number):
                    print("+++++++++++++++++ This card is VBV.")
                else:
                    print("$$$$$$$$$$$$$$$--- This card is non-VBV.")
    except FileNotFoundError:
        print("Error: The specified file does not exist.")
    except IOError:
        print("Error: Unable to read the file. Please check the file path.")

def main():
    try:
        while True:
            print(binof_logo())
            print("""
1. Mass BIN Check Mode
2. Single Bin Check Mode
3. Exit
            """)
            opt = input("$ Enter Your Mode : ")
            if opt == '1':
                path = input("$ Enter The Bin file's Path : ")
                mass_bin_info(path)
            elif opt == '2':
                bin_number = input("$ Enter the BIN to Check : ")
                get_bin_info(bin_number)
                if is_vbv(bin_number):
                    print("+++++++++++++++++ This card is VBV.")
                else:
                    print("$$$$$$$$$$$$$$$---This card is non-VBV.")
            elif opt == '3':
                break
            else:
                print("Invalid choice. Please enter a valid option.")
    except KeyboardInterrupt:
        print("\nExiting ....")

if __name__ == "__main__":
    main()
