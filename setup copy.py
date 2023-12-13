
import subprocess

def update_pips(verbose=False):
    try:
        print('Updating pip...')
        subprocess.call('pip install --upgrade pip', shell=True)
        print('Pip updated!')

        print('Checking for outdated packages...')
        subprocess.call('pip list -o > outdated_pips.txt', shell=True)

        out_pips_file = 'outdated_pips.txt'
        print('Updating packages...')
        with open(out_pips_file, 'r') as f:
            lines = f.readlines()
            for index, line in enumerate(lines):
                package_name = line.strip().split(' ')[0]
                if index > 1:
                    print(f'Updating {package_name}...')
                    subprocess.call(f'pip install {package_name} --upgrade', shell=True)

        print('Packages updated')

        print('Checking un-updated pips...')
        subprocess.call('pip list -o > outdated_pips.txt', shell=True)
        with open(out_pips_file, 'r') as f:
            content = f.read()
            if not content:
                print('All packages updated successfully')
            else:
                print(f'Failed to update the following packages:\n\n{content}')
    except Exception as e:
        print(f'Failed to update packages. Error:\n\n{e}')

# Ejemplos de uso
# guardar_pips()
# actualizar_pips(verbose=True)
