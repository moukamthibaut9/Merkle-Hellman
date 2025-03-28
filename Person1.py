import socket
import merkle_hellmann as mh


P1Hostname='localhost'
P1CommunicationPort=4555
P2Answer=''
P1Request=''
BlackList=['end','kill','stop','finish']
Connected=True


# Partie relative a la definition des clés
P1Username = str(input("Pour commencer, entrer un nom d'utilisateur: ")) # Definition d'un nom d'utilisateur pour P1
print("Definissez votre clé privée avant communication\n")
A = int(input("Entrer A: "))
N = int(input("Entrer N: "))
P1_Knapshak = []
P1_Key_lenght = int(input("Combien d'éléments pour votre sac? "))
print("Entrer les elements de votre sac.\n")
for i in range(1,P1_Key_lenght+1):
    P1_Knapshak.append(int(input(f"Element {i}: ")))
P1_PvK = (A,N,P1_Knapshak) # Enregistrement de votre clé privée
P2_PuK = []
P2_Key_lenght = int(input("Combien d'éléments pour le sac de votre interlocuteur: "))
print("Entrer ces éléments.\n")
for i in range(1,P2_Key_lenght+1):
    P2_PuK.append(int(input(f"Element {i}: ")))  # Enregistrement de la clé publique de votre interlocuteur


# Partie relative a la connexion proprement dite
P1MainConnexion=socket.socket(socket.AF_INET,socket.SOCK_STREAM) # Creation d'une connexion
if Connected:
    P1MainConnexion.connect((P1Hostname,P1CommunicationPort)) # Connexion
    P1Username=P1Username.encode().capitalize()
    P1MainConnexion.send(P1Username) # Envoi du nom de P1 a P2
    P2Username=P1MainConnexion.recv(1024).decode().capitalize() # Reception  du nom de P2
    print("Une communication sécurisée a été établie avec {}.".format(P2Username))
    while Connected:
        P1Request=str(input("{}, entrez votre message : ".format(P1Username.decode())))
        P1Request = mh.merkle_hellmann_encrypt(P2_PuK,P1Request) # Chiffrement du message avant envoi
        P1MainConnexion.send(P1Request.encode())
        P2Answer=P1MainConnexion.recv(1024)
        P2Answer = mh.merkle_hellmann_decrypt(P1_PvK,P2Answer.decode())  # Dechiffrement du message recu avant affichage
        print("Réponse de {} : {}".format(P2Username,P2Answer))
        if ( P2Answer.lower() in BlackList ):
            Connected=False
    P1MainConnexion.close()
    print("La communication a été coupée. Une personne s'est déconnectée.")



