# -*- coding: utf-8 -*-
from flask import Flask, jsonify
from bs4 import BeautifulSoup
import requests
import json
import os

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route('/api/fofocas', methods=['GET'])
def getfofocas():
	html_doc = requests.get('https://tvefamosos.uol.com.br/')
	soup = BeautifulSoup(html_doc.text, 'html.parser')
    

	##    Blocos    ##
	destaques = soup.find('section', class_='highlights-with-photo').find('div', class_='row')
	padroes = soup.find_all('section', class_='highlights-headline')
	ultimas = soup.find('section', class_='latest-news')
	data = []
	fofocas = []
	ultimas_noticias = []

	#print(ultimas)

	for dataBox_destaques in destaques.find_all('div', class_='thumbnail-standard'):
		title = dataBox_destaques.find('span', class_='thumb-kicker')
		content = dataBox_destaques.find('h3', class_='thumb-title').text
		content = content.replace('\"', '')
		data.append({ 'titulo' : title.text.strip(),'conteudo' : content.strip()})

	for dataBox_padroes in padroes:
		if dataBox_padroes.find('div', class_='section-title'):
			padrao_titulo = dataBox_padroes.find('div', class_='section-title').find('span').text
		else:
			padrao_titulo = ''

		print(padrao_titulo)
		itens = []
		c = 0
		for getcontent in dataBox_padroes.find_all('div', class_='thumbnail-standard'):
			item = getcontent.find('a').find('h3').text.strip()
			itens.append(item)

		itens[0] = itens[0].replace('\"', '')
		itens[1] = itens[1].replace('\"', '')
		itens[2] = itens[2].replace('\"', '')
		itens[3] = itens[3].replace('\"', '')



		fofocas.append({'titulo' : padrao_titulo.strip(), 'primeiro' : itens[0], 'segundo' : itens[1], 'terceiro' : itens[2], 'quarto' : itens[3]})
			

	for dataBox_ultimas in ultimas.find_all('div', class_='thumbnail-standard'):
		if dataBox_ultimas.find('h3', class_='thumb-title'):
			content = dataBox_ultimas.find('h3', class_='thumb-title').text
			content = content.replace('\"', '')
			data_ultimas = dataBox_ultimas.find('time', class_='thumb-time')
			ultimas_noticias.append({'conteudo' : content.strip(),'data' : data_ultimas.text.strip()})


	return jsonify({'destaques' : data, 'fofocas' : fofocas, 'ultimas' : ultimas_noticias})
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='127.0.0.1', port=port)

