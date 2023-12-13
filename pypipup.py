import subprocess

def update_pips():
    try:
        print('> Updating pip...')
        subprocess.call('pip install --upgrade pip', shell=True)
        print('Pip updated!')

        print('> Checking for outdated packages...')
        subprocess.call('pip list -o > outdated_pips.txt', shell=True)

        out_pips_file = 'outdated_pips.txt'
        print('- Updating packages...')
        with open(out_pips_file, 'r') as f:
            lines = f.readlines()
            for index, line in enumerate(lines):
                package_name = line.strip().split(' ')[0]
                if index > 1:
                    print(f'> Updating {package_name}...')
                    subprocess.call(f'pip install {package_name} --upgrade', shell=True)

        print('Packages updated')

        print('> Checking un-updated pips...')
        subprocess.call('pip list -o > outdated_pips.txt', shell=True)
        with open(out_pips_file, 'r') as f:
            content = f.read()
            if not content:
                print('All packages updated successfully!')
            else:
                print(f'The following packages could not be updated:\n\n{content}')
        print('> Cleaning caché...')
        import os
        os.remove('outdated_pips.txt')
        print('Ready! Enjoy your updated features.')
    except Exception as e:
        print(f'Failed to update packages. Error:\n\n{e}')

if __name__ == '__main__':
    update_pips()