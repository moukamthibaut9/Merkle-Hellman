from math import trunc, sqrt,fabs
from random import randint


def dec_bin(dec_nbr):
    """ Fonction pour passer du decimal au binaire(prend en entree un entier et retourne une chaine) """
    bin_nbr = ''
    if dec_nbr == 0:
        bin_nbr = '0'
    while dec_nbr != 0:
        bin_nbr = str(dec_nbr % 2) + bin_nbr
        dec_nbr = dec_nbr // 2
    return bin_nbr # La forme binaire du nombre est retournee sous forme de chaine de caracteres

def bin_dec(bin_nbr):
    """ Fonction pour passer du binaire au decimal(prend en entree une chaine et retourne un entier) """
    dec_nbr = 0
    for i in range(len(bin_nbr)):
        if bin_nbr[i] not in ['0','1']:
           print("Votre chaine binaire n'est pas valide")
           dec_nbr = None
           break
        else:
           dec_nbr += int(bin_nbr[i]) * pow(2,len(bin_nbr) - (i + 1))
    return dec_nbr # La forme decimale du nombre est retournee sous forme d'un entier

def pgcd(nbr1,nbr2):
    temp = 0
    if type(nbr1) is int and type(nbr2) is int and nbr1 != 0 and nbr2 != 0:
        if nbr1 < 0:
            nbr1 = -nbr1
        if nbr2 < 0:
            nbr2 = -nbr2
        if nbr1 > nbr2:
            temp = nbr1
            nbr1 = nbr2
            nbr2 = temp
        while (nbr2 % nbr1) != 0:
            temp = nbr2
            nbr2 = nbr1
            nbr1 = temp % nbr1
        return nbr1 # Correspond au PDGC des deux nombres
    print("Seuls les entiers non nuls sont pris en compte")
    return None

def premier(nbr):
    i = 1
    premier = True
    while i <= sqrt(nbr):
        i += 1
        if nbr % i == 0 and not (nbr in [1,2]):
            premier = False
            break
    return premier

def premiers(nbr1,nbr2):
    if pgcd(nbr1,nbr2) == 1:
        return True
    return False

def modulo_reverse(nbr,mod):
    reverse_nbr = 1
    for i in range(1,mod):
        if (nbr*i) % mod == 1:
            reverse_nbr = i
            break
    return reverse_nbr
        

def merkle_hellmann_knapsack_generator(nbr):
    knapsack = []
    for i in range(nbr):
        knapsack.append(sum(knapsack)+randint(1,100))
    return knapsack

def merkle_hellmann_keys_generator(knapsack):
    W = sum(knapsack)
    N = W + randint(1,500)
    A = randint(1,N-1)
    while not premiers(A,N):
        A = randint(1,N-1)
    private_key = (A,N,knapsack)
    public_key = []
    for elt in knapsack:
        public_key.append((elt*A)%N)
    return (private_key,public_key)

def merkle_hellmann_encrypt(public_key,message):
    """
    La cle publique est b = [b1, b2, ..., bn]
    """
    encryped_message = "" # Variable qui va stocquer tout le message chiffré sous forme d'une chaine numerique
    message_ = "" # Variable qui va stocquer le message clair sous forme numerique(binaire)
    bloc_lenght = len(public_key) # Taille de la cle = Taille d'un bloc
    for char in message:
        ascii_bin_char = dec_bin(ord(char))  # Variable qui va stocquer chaque carctere du message en binaire sur 8 bits
        if len(dec_bin(ord(char))) < 8:
            for i in range(8 - len(dec_bin(ord(char)))):
                ascii_bin_char = '0' + ascii_bin_char
        message_ += ascii_bin_char
    message = message_ # On ecrase le contenu de 'message' en y transferant celui de 'message_'
    if len(message_) % bloc_lenght != 0:
        for i in range(bloc_lenght - (len(message_) % bloc_lenght)):
            message = '0' + message # On complete le premier bloc par des zeros si necessaires(a gauche)
    # message__ constitue une liste qui va stocquer les blocs de notre message sous forme de chaine binaire
    message__ = [message[i:i+bloc_lenght] for i in range(0,len(message),bloc_lenght)]
    for bloc in message__:
        encryped_bloc = 0 # Variable qui va stocquer un bloc chiffré sous forme numerique
        for i in range(bloc_lenght):
            encryped_bloc += public_key[i] * int(bloc[i])
        encryped_message += str(encryped_bloc) + '.'
    return encryped_message[:len(encryped_message)-1]


def merkle_hellmann_decrypt(private_key,message):
    """
    La cle privee est le couple (A,N,[a1, a2, ..., an])
    """
    decryped_message = "" # Variable qui va stocquer le message déchiffré final
    decryped_message_ = "" # Variable qui va stocquer tout le message déchiffré sous forme d'une chaine binaire
    bloc_lenght = len(private_key[2]) # Taille de la cle = Taille d'un bloc
    # On extrait les blocs du message chiffré d'une liste obtenue a partir de split, on les dechiffre 
    # en binaire, les concatenne et stoque le resultat dans la variable 'decryped_message_' 
    for c in message.split('.'):
        p = (modulo_reverse(private_key[0],private_key[1]) * int(c))%private_key[1]
        decrypted_bloc = '' # Variable qui va stocquer un bloc déchiffré sous forme numerique binaire
        for i in range(bloc_lenght-1,-1,-1):
            if private_key[2][i] <= p:
                decrypted_bloc = '1' + decrypted_bloc
                p -= private_key[2][i]
            else:
                decrypted_bloc = '0' + decrypted_bloc
        decryped_message_ += decrypted_bloc
    if len(decryped_message_)%8 != 0:
        decryped_message_ = decryped_message_[len(decryped_message_)%8 : ]
    # Definition d'une liste qui va stocquer les blocs de notre message sous forme de chaine de 8 bits
    decryped_message__ = [decryped_message_[i:i+8] for i in range(0,len(decryped_message_),8)]
    for bloc in decryped_message__:
        decryped_message += chr(bin_dec(bloc))
    return decryped_message


if __name__ == '__main__':
    # Génération des clés
    P1_Key_lenght = 3
    P1Knapshak = merkle_hellmann_knapsack_generator(P1_Key_lenght)
    (P1_PvK,P1_PuK) = merkle_hellmann_keys_generator(P1Knapshak)
    P2_Key_lenght = 4
    P2Knapshak = merkle_hellmann_knapsack_generator(P2_Key_lenght)
    (P2_PvK,P2_PuK) = merkle_hellmann_keys_generator(P2Knapshak)
    print(f"\nP1PrivateKey = {P1_PvK} | P1PublicKey = {P1_PuK}\nP2PrivateKey = {P2_PvK} | P2PublicKey = {P2_PuK}\n")

    # Test avec l'une des clés générée
    """
    message = 'VOICI son numero: 676080813'
    Ch = merkle_hellmann_encrypt(P1_PuK,message)
    Dc = merkle_hellmann_decrypt(P1_PvK,Ch)

    print(f"Message: {message}\nChiffrement: {Ch}\nDechiffrement: {Dc}")
    """

