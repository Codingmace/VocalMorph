import requests
import os
import shutil
import subprocess
import sys

def vocal_seperator(input_file):
    filepath = "vocal-remover-v6.0.0.4.zip"
    if not os.path.exists("./vocal-remover/"):
        # Download latest zip
        url = "https://github.com/tsurumeso/vocal-remover/releases/download/v6.0.0b4/vocal-remover-v6.0.0b4.zip"

        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(filepath, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

        # Decompress folder
        shutil.unpack_archive(filepath, ".")

        # Delete old zip
        os.remove(filepath)

        requirements_file = '.\\vocal-remover\\requirements.txt'
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_file])
            print(f"Successfully installed packages from {requirements_file}")
        except subprocess.CalledProcessError as e:
            print(f"Error occurred while installing packages: {e}")
        except FileNotFoundError:
            print(f"Requirements file not found: {requirements_file}")

    subprocess.run(["python",".\\vocal-remover\\inference.py", "-i", input_file])

#vocal_seperator()
