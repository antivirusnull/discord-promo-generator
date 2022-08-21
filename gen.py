import random, requests, json, string, threading, time
from urllib.parse import urlparse, parse_qs

def ran(a): return "".join(random.choices((string.ascii_lowercase), k=a))

agent = f"Medal-Electron/4.1674.0 (string_id_v2; no_upscale) win32/10.{random.randint(0,3)}.19042 (x64) Electron/8.5.5 Recorder/1.0.0 Node/12.13.0 Chrome/{random.randint(70,85)}.0.3987.163 Environment/production"

def generate(disc_token, proxy):
    while True:
        try:
            while True:
                email = ran(10) + random.choice(["@gmail.com", "@seksownyczlowiek.fun", "@yahoo.com", "@discordsupport.space", "@velipsemail.fun", "@asshole.fun", "@voicerecorder.fun"])
                username = ran(8); password = ran(10)

                r = requests.post("https://medal.tv/api/users", json={"email":email,  "userName":username,  "password":password}, headers={"Accept":"application/json",  "Content-Type":"application/json",  "User-Agent":agent,  "Medal-User-Agent":agent}, proxies=proxy)
                if not r.ok: continue

                authenticate = requests.post("https://medal.tv/api/authentication", json={"email":email,"password":password},headers={"Accept":"application/json","Content-Type":"application/json",  "User-Agent":agent,  "Medal-User-Agent":agent}, proxies=proxy)
                if not authenticate.ok: continue

                authResp = json.loads(authenticate.text)
                token = authResp["userId"] + "," + authResp["key"]
                discordOauth = requests.post("https://medal.tv/social-api/connections", json={"provider": "discord"}, headers={"Accept":"application/json",  "Content-Type":"application/json",  "User-Agent":agent,  "Medal-User-Agent":agent,  "X-Authentication":token}, proxies=proxy)
                if not discordOauth.ok: continue

                doOauth = requests.post(discordOauth.json()["loginUrl"], headers={"Authorization":str(disc_token), "Content-Type":"application/json"}, json={"permissions":"0",  "authorize":"true"}, proxies=proxy)
                if not doOauth.ok: continue

                medalLink = json.loads(doOauth.text)["location"]
                oauthDone = requests.get(medalLink)
                oauthResponse = parse_qs(urlparse(oauthDone.url).query)
                if oauthResponse["status"][0] == "error":
                    print(oauthResponse["message"][0])

                nitroLink = requests.get("https://medal.tv/api/social/discord/nitroCode", headers={"Accept":"application/json",  "Content-Type":"application/json",  "User-Agent":agent,  "Medal-User-Agent":agent,  "X-Authentication":token}, proxies=proxy)
                if not nitroLink.ok: continue
                
                nitro = json.loads(nitroLink.text)
                try:
                    print(nitro["url"])
                    with open("nitro.txt", "a+") as b: b.write(str(nitro["url"])+"\n")
                    break

                except Exception as e:
                    print(str(e))
                    print(str(nitro))
                    break

        except Exception as e:
            print(e)
        break

for disc_token in open("tokens.txt","r").read().splitlines():
    proxy = random.choice(open("proxies.txt","r").read().splitlines()); proxyDict = {"http": f"http://{proxy}","https": f"http://{proxy}"}
    threading.Thread(target=generate, args=(disc_token.strip(), proxyDict)).start()