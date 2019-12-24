import subprocess


def run_clients(client_qty):
    for _ in range(client_qty):
        subprocess.run(['python', 'client'], shell=True, cwd='../messenger')


if __name__ == '__main__':
    run_clients(1)
