# -*- coding: utf-8 -*-

import csv
import json
import tweepy
import time

from credentials import *


#Añadimos las credenciales

access_token = "862175095-wrIaQfiy9kdEeubwS6LeC6BKOfq0jp59xNh5z3Jg"
access_token_secret = "A5U15GCR6yQbtfe6nKapXLKbL0or0L6aN7Rel4U0AakDW"
consumer_key = "EtrFBSWeQRGJWUeDES9nnf0E5"
consumer_secret = "jFpBjOTI4WxY0QQexSmtQn1UNXt9vv9LXFDrZm5tMfMgvMWefT"

if __name__ == '__main__':

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    now = time.strftime("%d-%m-%y-%H-%M-%S")

    #Creamos los ficheros CSV que usaremos para cargar en gephi

    csvFileTweets = open('tweets.csv', 'a')
    csvFileUsers = open('users.csv', 'a')
    csvFileEdges = open('edges.csv', 'a')


    csvWriterTweets = csv.writer(csvFileTweets)
    csvWriterUsers = csv.writer(csvFileUsers)
    csvWriterEdges = csv.writer(csvFileEdges)

    #Creamos un set para comprobar que no metamos usuarios repetidos

    users = set()

    csvWriterTweets.writerow(['ID', 'Usuario', 'Texto', 'Seguidores', 'Siguiendo', 'Favoritos Cuenta', 'RTs','Favoritos Tweet','Fecha', 'Localizacion'])
    csvWriterUsers.writerow(['ID', 'Seguidores', 'Siguiendo', 'Favoritos Cuenta'])
    csvWriterEdges.writerow(['Source', 'Target'])
    #Con un cursor vamos a crear el primer csv de tweets y a llenar una estructura de tweets

    for tweet in tweepy.Cursor(api.search,
        q="#AOVE OR #AceiteDeOliva",
        count=10000,
        #since="2012-09-01",
        #until="2017-04-01",
        lang="es").items(18000):
                #Escribimos filas en los ficheros CSV
                csvWriterTweets.writerow([tweet.user.id,tweet.user.screen_name, tweet.text.encode('utf-8'), tweet.user.followers_count,
                tweet.user.friends_count, tweet.user.favourites_count, tweet.retweet_count, tweet.favorite_count, tweet.created_at, tweet.user.location.encode('utf-8')])
                completo = tweet.text.encode('utf-8')
                troceado = completo.split()
                if(tweet.user.screen_name not in users):
                    users.add(tweet.user.screen_name)
                    csvWriterUsers.writerow([tweet.user.screen_name, tweet.user.followers_count,tweet.user.friends_count, tweet.user.favourites_count])
                #Obtenemos los RT
                if( troceado[0] == 'RT'):
                    csvWriterEdges.writerow([tweet.user.screen_name, troceado[1]])
                #Obtenemos las menciones
                elif('@' in completo):
                    i=0
                    while i < len(troceado):
                        palabra=troceado[i]
                        if (palabra[0]=='@' and troceado[i] in users):
                            csvWriterEdges.writerow([tweet.user.screen_name, troceado[i]])
                            break
                        else:
                            i+=1

    csvFileTweets.close()
    csvFileUsers.close()
    csvFileEdges.close()
