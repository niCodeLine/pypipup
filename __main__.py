import subprocess
import os
import json

def update_pips():
    try:
        print('> Updating pip...')
        subprocess.call('pip3 install --upgrade pip', shell=True)
        print('Pip updated!')

        print('> Checking for outdated packages...')
        result = subprocess.run(
            ['pip3', 'list', '--outdated', '--format=json'],
            capture_output=True, text=True
        )

        outdated = json.loads(result.stdout)

        if not outdated:
            print('All packages are already up to date.')
            return

        print('- Updating packages...')
        for pkg in outdated:
            name = pkg['name']
            print(f'> Updating {name}...')
            subprocess.call(f'pip3 install --upgrade {name}', shell=True)

        print('Packages updated.')

        print('> Checking un-updated packages...')
        result = subprocess.run(
            ['pip3', 'list', '--outdated', '--format=json'],
            capture_output=True, text=True
        )
        remaining = json.loads(result.stdout)

        if not remaining:
            print('All packages updated successfully!')
        else:
            print('The following packages could not be updated:')
            for pkg in remaining:
                print(f" - {pkg['name']} ({pkg['version']} -> {pkg['latest_version']})")

        print('> Cleaning cache...')
        subprocess.call('pip3 cache purge', shell=True)

        print('Ready! Enjoy your updated features.')

    except Exception as e:
        print(f'Failed to update packages. Error:\n\n{e}')


if __name__ == '__main__':
    update_pips()
