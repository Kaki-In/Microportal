#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#  micropylist.py
#
#  Copyright 2023 Kaki In <kaki@mifamofi.net>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

import verbosePolicy as _vpol
import sys as _sys
import os as _os

if "LANG" in _os.environ:
    DEFAULT_LANGAGE  = _os.environ['LANG'].split(".")[0].split("_")[0]
else:
    DEFAULT_LANGAGE = "en"

class i18nTranslator():
    def __init__(self, lang = DEFAULT_LANGAGE, vpol = _vpol.VerbosePolicy(True, True, True, True, True)):
        self._langage = lang.lower()
        self._vpol = vpol  
    
    def setLangage(self, lang):
        """
        Changes the langage of the translator
        """
        self._langage = lang
    
    def getLangage(self):
        """
        Returns the actual langage
        """
        return self._langage 
    
    def getMessage(self, message, lang = None, **insertions):
        text = message

        lang = lang or self._langage
        
        if   lang == "en":
            # nothing to do, translation not necessary. Voluntary added because of the error management.
            pass

        elif lang == "fr":
            ### Exceptions ###
            if   message == "invalid request":
                text = "requête invalide"
            elif message == "no such request":
                text = "requête introuvable"

            elif message == "micropy actually not connected":
                text = "le micropy n'est pas connecté"
            elif message == "micropy already connected":
                text = "le micropy est déjà connecté"
            elif message == "invalid micropy response ; is it really a micropy?":
                text = "réponse invalide du micropy ; est-ce vraiment un micropy?"

            elif message == "user actually not connected":
                text = "l'utlisateur n'est pas connecté"
            elif message == "user already connected":
                text = "l'utilisateur est déjà connecté"
            elif message == "invalid user response ; is it really an user?":
                text = "réponse invalide de l'utilisateur ; est-ce vraiment un utilisateur?"

            elif message == "the protocol manager has not been started yet":
                text = "le gestionnaire de protocol n'est pas démarré"
            elif message == "the protocol manager isn't stopping":
                text = "le gestionnaire de protocol n'a pas été arrêté"
            elif message == "invalid request struct":
                text = "structure de requête invalide"

            elif message == "no such micropy":
                text = "micropy inconnu"

            elif message == "no such user":
                text = "utilisateur inconnu"

            elif message == "not connected client":
                text = "le client n'est pas connecté"
            elif message == "client not stopping":
                text = "le client n'est pas en état d'arrêt"
            
            ### Server logs ###

            elif message == "Connected a client at address {address}":
                text = "Connexion d'un client à l'adresse {address}"
            elif message == "Connected micropy {name}":
                text = "Connexion du micropy {name}"
            elif message == "Connected a micropy at address {address}":
                text = "Connexion d'un micropy à l'adresse {address}"

            elif message == "Connected user {username}":
                text = "L'utilisateur {username} s'est connecté"

            elif message == "A client sent an invalid connection response : {info}":
                text = "Un client a envoyé une réponse de connection invalide : {info}"
            
            elif message == "an exception occured while closing connections":
                text = "une erreur est intervenue pendant la fermeture des connexions"

            elif message == "an error occured...":
                text = "une erreur est intervenue..."
            
            ### Protocol Manager Logs ###

            elif message == "Got an unexpected syntax error when parsing a request":
                text = "Une erreur de syntax inattendue est parvenue lors de la lecture d'une requête"
            elif message == "Got an unexpected value error when parsing a request":
                text = "Une erreur de valeur inattendue est parvenue lors de la lecture d'une requête"
                
            ### Action execution errors ###
            
            elif message == "invalid argument {argname} ":
                text = "argument {argname} invalide"
            elif message == "missing argument {argname}":
                text = "argument {argname} manquant"
            elif message == "invalid answer":
                text = "réponse invalide"

            else:
                self._vpol.log("Warning : untranslated message {} to langage {}".format(repr(message), repr(lang)), _vpol.LEVEL_WARNING)
                
        else:
            self._vpol.log("Warning : unknown langage {}".format(repr(lang)), _vpol.LEVEL_WARNING)

        try : 
            text = text.format(**insertions)
        except:
            self._vpol.log("Warning : couldn't translate extracted informations {} for message {}".format(repr(insertions), repr(message)), _vpol.LEVEL_WARNING)

        return text

