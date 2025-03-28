import socket
import merkle_hellmann as mh

P2Hostname='localhost'
P2CommunicationPort=4555
P1Answer=''
P2Request=''
BlackList=['end','kill','stop','finish']
Connected=True


# Partie relative a la definition des clés
P2Username = str(input("Pour commencer, entrer un nom d'utilisateur: ")) # Definition d'un nom d'utilisateur pour P2
print("Definissez votre clé privée avant communication\n")
A = int(input("Entrer A: "))
N = int(input("Entrer N: "))
P2_Knapshak = []
P2_Key_lenght = int(input("Combien d'éléments pour votre sac? "))
print("Entrer les elements de votre sac.\n")
for i in range(1,P2_Key_lenght+1):
    P2_Knapshak.append(int(input(f"Element {i}: ")))
P2_PvK = (A,N,P2_Knapshak) # Enregistrement de votre clé privée
P1_PuK = []
P1_Key_lenght = int(input("Combien d'éléments pour le sac de votre interlocuteur: "))
print("Entrer ces éléments.\n")
for i in range(1,P1_Key_lenght+1):
    P1_PuK.append(int(input(f"Element {i}: ")))  # Enregistrement de la clé publique de votre interlocuteur

# Partie relative a la connexion proprement dite
P2MainConnexion=socket.socket(socket.AF_INET,socket.SOCK_STREAM) # Creation d'une connexion
if Connected:
    P2MainConnexion.bind((P2Hostname,P2CommunicationPort)) # Connexion
    P2MainConnexion.listen(5)
    print("Prêt à la communication\n")
    P2ToP1Connexion,Connexion_Infos=P2MainConnexion.accept() # Ecoute jusqu'à acceptation d'une demande cliente
    P1Username=P2ToP1Connexion.recv(1024).decode().capitalize() # Reception  du nom de P1
    P2Username=P2Username.encode().capitalize()
    P2ToP1Connexion.send(P2Username) # Envoi du nom de P2 a P1
    print("Une communication sécurisée a été établie avec {}.".format(P1Username))
    while Connected:
        P1Answer=P2ToP1Connexion.recv(1024)
        P1Answer = mh.merkle_hellmann_decrypt(P2_PvK,P1Answer.decode())  # Dechiffrement du message recu avant affichage
        print("Réponse de {} : {}".format(P1Username,P1Answer))
        P2Request=str(input("{}, à vous de répondre : ".format(P2Username.decode())))
        P2Request = mh.merkle_hellmann_encrypt(P1_PuK,P2Request) # Chiffrement du message avant envoi
        P2ToP1Connexion.send(P2Request.encode())
        if ( P1Answer.lower() in BlackList ):
            Connected=False
    P2ToP1Connexion.close()
    P2MainConnexion.close()
    print("La communication a été coupée. Une Personne s'est déconnectée.")