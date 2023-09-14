# Projet_B

## Introduction

### Contexte du Projet

Ce projet s'inscrit dans la continuité de notre formation et a pour but bien défini la mise en place d'un pipeline CI/CD
pour la conception du projet suivant: Transformer une application monolithique en micro-services et l’intégrer de manière 
automatisée via pipeline CI/CD en veillant à intégrer des principes DevSecOps.

Les participants sont: Amine R., Giovani M., Yousri B.


Dans ce contexte, plusieurs enjeux se sont posés et notamment l'introduction des concepts d'application monolithique et de micro-service. Explicitement, l'application monolithique correspond à un ensemble applicatif réuni en un seul bloc, un seul programme exécutable. 

L'avantage principal étant que le déploiement ne se compose que d'un exécutable puisque toutes les fonctions sont intégrées dans l'application. La mise en place pose moins de difficultés vu que les modules communiquent entre eux au sein du monolithe. Mais au fur et à mesure du développement, l'application peut gagner en complexité, du fait des fonctionnalités qui s'ajoutent, ce qui peut mettre à mal le fonctionnement de cet ensemble lorsqu'un de ces éléments pose problème. Par ailleurs, c'est l'une des raisons principales de la transition monolithe à micro-services, le problème de la scalabilité se pose. Dès lors qu'il devient nécessaire de mettre en place une instance supplémentaire pour faire face à la demande utilisateur, c'est tout l'application qui doit être déployée à nouveau, avec la charge que cela nécessite.

C'est dans ce contexte qu'intervient le passage aux micro-services. Il s'agit du découpage de fonctionnalités majeures du monolithe en micro-service dédié à un module précis. Prenons par exemple le cas de Netflix, qui est passé par cette transition: Lorsque l'application fait face à une demande plus forte qu'à l'accoutumée, il était nécessaire de déployer des instances entière de l'application en supplément. Or, il n'était pas pertinent d'augmenter l'accès à certaines parties du service, faisant peser une charge supplémentaire inutile, alors que la demande ne concernait que la partie transcodage vidéo par exemple. C'est en cela que les micro-services trouvent un intérêt. La contre-partie étant que leur mise en place est plus complexe, étant donné que tous ces éléments peuvent être amenés à fonctionner de concert sur un même réseau et cette intégration peut poser un nombre de difficultés certain.

C'est donc sur ce postulat que s'amorce ce projet avec les objectifs suivants:
- Partir d'une application monolithique (WordPress en l'espèce).
- Découper ce monolithe en plusieurs micro-services pour son exploitation.
- Déployer en continue ces micro-services à la suite de l'intégration de correctifs ou mise à jour.
- Sécuriser l'ensemble afin que ces micro-services ne soient pas accessibles et qu'ils soient eux-même sécurisés au cours de l'exploitation.

Tout en gardant à l'esprit les principes DevSecOps à intégrer dans ce projet.

### Stack Technologique

Afin de mettre en oeuvre ce projet, les éléments suivants ont été mis en oeuvre:
- WordPress : L'application monolithique déployée servant de base à nos micro-services).
- Python et Flask API : Pour le développement de nos micro-services.
- Nginx : Pour la sécurité de nos micro-services.
- Prometheus/Grafana : Pour le monitoring et la gestion des logs de nos micro-services.
- Docker : Pour le déploiement de nos applications.
- Jenkins : Pour la mise en place de notre Pipeline CI/CD.


## Développement

### Conception

Phase initiale de ce projet, nous avons dans un premier temps réfléchi au choix de l'application monolithique sur lequel nous travaillerions. Ayant eu un contact initial avec WordPress, c'est sur cette application que notre première réflexion s'est portée. Nous avons dès lors consulté la documentation de WordPress Rest API qui nous permettrait d'intéragir avec l'application afin d'exploiter nos micro-services. Si d'autres choix ont fait l'objet d'une réflexion collective (Jellyfin notamment) c'est finalement sur WordPress que notre choix s'est porté, compte tenu de la durée du projet et de la simplicité du déploiement de l'environnement (Jellyfin aurait par exemple nécessité la mise en place de contenu multimédia à traiter ou du matériel pour le transcoding vidéo) tandis que WordPress pouvait être exploité en quelques minutes suite à son déploiement (ou redéploiement) initial.

L'application étant choisie, nous avons donc procédé au découpage de l'application en se basant sur la documentation afin d'identifier les micro-services à mettre en place. Nous avons donc décidé de partir sur le développement de trois micro-services:
- Un micro-service dédié à la gestion des posts (Listing, création, édition, suppression)
- Un micro-service dédié à la gestion des pages (Listing, création, édition, suppression)
- Un micro-service dédié à la gestion des médias (Listing, édition, suppression)

Le postulat de départ étant le suivant, nous avons imaginé la situation où un client souhaiterait exploiter un site web de taille moyenne qui requiert l'intervention de plusieurs auteurs, en déployant des micro-services dédiés à une fonctionnalité spécifique et ce afin de sécuriser l'accès à l'exploitation du site, tout en apportant un élément de scalabilité dans le cas où il serait nécessaire de déployer un module uniquement pour faire face à une charge spécifique.

Il était donc nécessaire mettre en place une interface pour exploiter le micro-service, ainsi que d'un accès sécurisé, à la fois pour exploiter le service mais aussi permettre une flexibilité dans la gestion des utilisateurs, par le biais d'une authentification.

Nous avons donc établi un schéma initial de ce à quoi ressemblerait notre architecture:
(INSERER SCHEMA INITIAL)

Une fois le schéma établi, nous nous sommes réparti le développement des micro-services, un chacun, sur la base établie plus haut. La documentation WordPress Rest API étant bien définie, le code serait donc similaire dans son fonctionnement, puisqu'il s'agissait d'envoyer une requête HTTP spécifique à une adresse afin d'obtenir un résultat.

### Présentation des micro-services

Etablis sur la base de WordPress Rest API, nos micro-services sont écrit en Python et utilisent le micro-framework Flask qui permet de déployer des applications web. En définissant des routes spécifiques appelant l'API WordPress par le biais d'une requête HTTP GET/POST/PUT/DELETE, il nous est possible d'exploiter un site WordPress par le biais de ces micro-services. Chaque micro-service est dédié à un type de contenu mais ils sont globalement identiques dans leur fonctionnement et intègre une authentification sécurisée par une session côté serveur, un limiteur de requête par IP et un module de monitoring, le tout exploité par une page web.

#### Micro-service A: Posts

Le micro-service Posts est dédié à la gestion des Posts du site WordPress du client. En utilisant WordPress Rest API, l'utilisateur peut, une fois authentifier, accéder à l'exploitation des posts du site, soit en ajoutant du nouveau contenu, soit en éditant ou supprimant un contenu existant.

#### Micro-service B: Pages

Le micro-service Pages est dédié à la gestion des Pages du site WordPress du client. En utilisant WordPress Rest API, l'utilisateur peut, une fois authentifier, accéder à l'exploitation des pages du site, soit en ajoutant du nouveau contenu, soit en éditant ou supprimant un contenu existant.

#### Micro-service B: Médias

Le micro-service Médias est dédié à la gestion des médias du site WordPress du client. En utilisant WordPress Rest API, l'utilisateur peut, une fois authentifier, accéder à l'exploitation des médias du site en éditant ou supprimant un contenu existant.

### Difficultés

La première difficulté était de comprendre le fonctionnement de l'API de Wordpress. Ce projet étant une première à ce sujet, il a fallu comprendre l'intéraction entre le service et l'application par l'envoi de requête HTTP. Nous avons dans un premier temps expérimenté avec Postman, afin de tester l'utilisation de l'API. Une fois que nous avions compris son fonctionnement, il était désormais temps d'implémenter les premières routes sur notre application Python utilisées conjointement avec Flask API. La question de l'authentification s'est posée très tôt. A ce niveau, Wordpress ne propose pas de solution officielle adéquate, en dehors de l'utilisation de cookies. Nous avons donc dans un premier temps uilisé le seul plugin officiel de WordPress pour l'authentification qui est une authentification JSON Basic Authentication. 

### Premier jet

Nous avions pour chacun des services une page d'accueil accessible avec un champ d'authentification un listing des éléments, mais nous n'avions pas encore complétés nos micro-services. Un premier jet, certes rudimentaire, mais fonctionnel.
(INSERER CAPTURE D'ECRAN)

Cependant, cela s'inscrivait dans notre démarche DevOps et l'application de la méthodologie Agile puisqu'il était désormais tant de mettre en place notre pipeline CI/CD afin de passer d'un prototype à un produit compétent, en appliquant un développement incrémental et itératif tout en déployant et testant ces intégrations.

## Le pipeline CI/CD

En déployant Jenkins via WSL2, nous avons initié notre pipeline sur notre machine locale, faisant ainsi office à la fois de "Controller" et de "Built-in Node". Néanmoins dans un environnement plus robuste, il nous aurait été possible pour des raisons de sécurité de dissocier le processus en initiant une machine Jenkins "Controller" et une ou plusieurs machines "agents" s'occupant d'exécuter les pipelines et le déploiement.

Nous avons mis en place un pipeline initial assez rudimentaire afin de pouvoir lancer un build une fois un commit exécuté, pour que le build soit testé puis déployé. Néanmoins à ce stade, il s'agissait de tests bouchon. Il s'agissait de s'assurer que les apports au code n'empêchaient pas de déployer l'application. Nous avons pour cela conteneuriser nos micro-services avec Docker, afin de constater le bon déploiement de ces derniers via notre pipeline. 

Au fur et à mesure du développement et du fait que nos applications approchaient de leur stade final, nous avons ajouté des tests supplémentaires. Tout d'abord, de vrais tests s'assurant que les routes étaient correctement mappées dans l'application et renvoyait le bon code retour, puis des tests sécurité suite à la mise en place d'éléments de sécurité dans notre architecture (ce point sera abordé plus tard).

En combinant GitHub et Docker, nous arrivions donc à un pipeline CI/CD complet:
- Une intégration continue: Le déploiement de code dans notre gestionnaire de code source (GitHub) permet la construction d'une nouvelle image, qui sera testée afin de s'assurer que le code reste cohérent et ne produit pas d'erreur.
- Un déploiement continue: Une fois le build construit et validé, la nouvelle image est déployée sur Docker et ce sans interrompre les autres services. Tout changement est donc déployé via Docker tout en garantissant un service continu.

(INSERER CAPTURE D'ECRAN PIPELINE CI/CD)

Autre élément à prendre en compte, la sécurité de Jenkins. Idéalement, nous aurions pu mettre en place comme nous l'avions dit un Node Jenkins détaché du Jenkins Controller, mais les ressources hardware étant limitées et la nature du projet étant en local, cela ne s'est pas présenté comme une nécessité. Néanmoins, il s'agit d'un élément à prendre en compte pour un projet à plus grande échelle.

Il a aussi été nécessaire de mettre en place dès cette étape des bonnes pratiques relatives à l'utilisation de Jenkins:
- Mettre une politique de mot de passe efficace et ce même en environnement de développement (pas de admin/admin par exemple).
- Définir des rôles afin de limiter les accès des utilisateurs sur la machine et faire en sorte qu'ils ne puissent pas sortir de leurs prérogatives sur Jenkins.
- Définir un utilisateur non-root pour exécuter les tâches Jenkins, dans le cas où un acteur mal-intentionné interne voudrait exécuter des commandes malveillantes depuis Jenkins (ou même un acteur externe).

En prenant en compte tous ces éléments, nous avons pu aboutir au développement et au déploiement de notre application dans les temps, par l'intégration de tests permettant à la fois de valider la cohésion du code mais aussi de la sécurisation de notre architecture.

En effet, du fait des limitations de notre environnement de développement et de l'échelle de ce projet, nous aurions pu implémenter d'avantages d'éléments à notre pipeline:
- Comme vu précédemment, la mise en place de node pour exécuter les pipelines.
- L'utilisation du webhook de notre SCM, GitHub, afin de lancer automatiquement un Build lorsqu'un commit est poussé vers le SCM.


## Sécurité

### Politique de sécurité

Il était primordial dès le départ de définir une politique de sécurité claire, aussi bien externe, s'agissant de potentiels failles de sécurité ou d'attaques, mais aussi en interne, dans le cas où un acteur mal-intentionné aurait accès à nos machines sur site. Ainsi, nous avons établi cette politique en deux parties:
- Une politique de sécurité DevSec.
- Une politique de sécurité SecOps.

### DevSec

La première difficultée s'agissant de la sécurité était que les informations d'authentification apparaissaient clairement dans l'URL de nos micro-services, ce qui pose un problème majeur. Une première solution avait été d'encoder puis décoder ces éléments au sein même de l'application, en passant par un encodage/décodage avec base64. Mais la problématique demeurait étant donné qu'il suffisait de copier la partie en base64 et la décoder, faisant ainsi apparaitre les données sensibles.

Les solutions étaient donc les suivantes:
- Utiliser la solution Basic Auth de WordPress
- Utiliser un plugin tiers basé sur JWT mais dont la provenance ne permettait pas de s'assurer d'une implémentation sûre

La solution Basic Auth étant celle supportée officiellement, nous sommes donc restés sur ce choix, étant donné que nous l'avions déjà implémenté avec succès et qu'il nous permettait aussi de proposer une authentification utilisateur sur la base d'un nom d'utilisateur et mot de passe. Mais cette solution ne saurait être satisfaisante en l'état et ce même pour un proof-of-concept ou un environnement de développement. Ainsi, nos investigations nous ont mené à une solution double: La première, passer ces requêtes en POST et non en GET, afin que les identifiants n'apparaissent plus dans l'URL et deuxièmement, l'utilisation de Flask Session afin de gérer la session utilisateur en conservant les identifiants dans la session côté serveur et non plus en les passant dans l'URL. Ce faisant, nous nous pouvions conserver cette méthode en mitigeant les soucis inhérents à celle-ci.

Nous avons donc appliqué un principe DevSec dès cette étape afin d'implémenter des mesures de sécurité dès le départ et non pas sur le tard. Néanmoins, il conviendra de passer à une solution plus robuste.

Par ailleurs, un limiteur de requête par adresse IP a aussi été mis en place, afin d'éviter des attaques type DDoS ou de type Bruteforce, évitant ainsi qu'une IP puisse requérir notre service au-delà des limites du raisonnable.

Quant à l'accès à nos micro-services, il nous semblait primordial de passer par un reverse-proxy afin de cacher ces derniers mais aussi d'établir des connexions par un protocole HTTPS (HTTP + TLS) afin de chiffrer les échanges entre le client et le serveur. Notre choix s'est porté sur Nginx pour le reverse proxy, auquel nous avons couplé ModSecurity en tant que WAF (Web Application Firewall) afin de protéger notre backend des attaques communes en appliquant l'OWASP CRS. (Notre pipeline intégrant d'ailleurs des tests dans ce sens afin de nous assurer du bon déploiement de notre système de sécurité).

### SecOps

S'agissant du principe SecOps, cela s'est manifesté de plusieurs façons. Tout d'abord en établissant des bonnes pratiques internes notamment sur les droits utilisateurs et sur les mots de passes.

En segmentant l'accès aux pipelines aux utilisateurs définis, le risque qu'un utilisateur lance un job qu'il n'aurait pas dû est ainsi mitigé. Le fait de définir un utilisateur non-root dans notre Built-in Node permet aussi d'éviter une utilisation malveillante de Jenkins par un acteur présent dans les locaux ou ayant accès à la session de manière malveillante.

Enfin, le fait d'avoir passé nos conteneurs Docker en rootless permet aussi d'éviter une utilisation malveillante de ces derniers lors de l'exploitation du service.


## Conclusion

Au final, notre projet a abouti à la mise en place de l'infrastructure suivante:
- Une machine avec WSL2 pour opérer Jenkins et Docker,
- Trois micro-services conteneurisés sous Docker afin d'exploiter WordPress, lui aussi conteneurisé avec sa base de données
- Prometheus et Grafana, eux aussi conteneurisés afin de monitorer nos services,
- Nginx avec ModSecurity, agissant comme reverse proxy et WAF afin de protéger notre infrastructure.

(SCHEMA D'INFRASTRUCTURE)

Bien entendu, il y a des axes d'améliorations à apporter:
- Une solution d'authentification plus robuste,
- Un pipeline CI/CD reposant sur plusieurs machines,
- La mise en place d'un webhook pour automatiser les builds,
- Mise en place d'une whitelist sur Nginx,
- Mise en place de fail2ban pour bannir les tentatives répétées.
