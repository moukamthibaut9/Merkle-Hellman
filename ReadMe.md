# Procédure d'execution des fichiers


1. Génération des clés pour les deux personnes qui vont communiquer
    Dans le fihier _merkle\_hellmann.py_, décommentez la section '# Génération des clés' et executer le fichier afin d'obtenir les différentes clés que les deux personnes vont utiliser ( vous pouvez modifier les valeurs des variables **P1_Key_lenght** et **P2_Key_lenght** pour agir sur la longueur des clés qui seront générées ). Une fois les clés obtenues, recommentez cette section pour éviter l'affichage des clés dans la console pendant la communication

2. Execution des fichiers _Person2.py_ et _Person1.py_ pour lancer une communication entre deux personnes
    Une fois les clés obtenues, executez dans cet ordre les fichiers _Person2.py_ et _Person1.py_ ( nous avons utilisé le module **socket** pour simuler cette communication, ce module permet de simuler un serveur et un ou plusieurs clients qui vont s'échanger des informations sur le même réseau; _Person2.py_ ici est associé au serveur, il est donc important qu'il soit le premier à démarrer )
    N.B : Les éléments de votre sac contituent les éléments de votre clé privée tandis que les éléments du sac de votre interlocuteur constituent les éléments de sa clé publique.