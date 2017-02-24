#!/usr/bin/python
# coding=utf-8
"""Modul beinhaltet Klassen, die einen fuerwehrtechnischen
Aspekt abbilden.
"""
import logging
import re

import datetime


#                 Aufbau Alarmmeldungen
#                      1,2,3,...,n
#
#
#              v1            |         v2
#     -----------------------|------------------------
#                            |
#  1    Stichwort            |   -
#  2    BMA                  |   Stichwort
#  3    Objekt               |   Objekt
#  4    Str./Hausnummer      |   -
#  5    Ortsteil             |   Str./Hausnummer
#  6    Gemeinde             |   -
#  7    Meldender            |   -
#  8    sonst. Ortsangabe    |   Ortsteil
#  9    Bemerkung            |   Gemeinde
# 10                         |   sonst. Ortsangabe
# 11                         |   Bemerkung


class Einsatz:
    def __init__(self, einsatz_bytes):
        """
        Klasse repräsentiert einen empfangenen Einsatz des Digitalen Meldeempfängers.
        :type einsatz_bytes: str
        :param einsatz_bytes: Text-String der die gesamten Einsatzmeldung enthält.
        """
        self._logger = logging.getLogger(self.__class__.__name__)

        self._format_version = 1

        self._hexdata = einsatz_bytes.encode('hex')
        self._einsatz_text = einsatz_bytes.decode('latin-1')

        self._ric_str = u""
        self._ric = 0
        self._ric_sub = u""
        self._datum = u""
        self._uhrzeit = u""
        self._stichwort = u""
        self._bma = u""
        self._objekt = u""
        self._gemeinde = u""
        self._ortsteil = u""
        self._str_hnr = u""
        self._meldender = u""
        self._son_ort = u""
        self._bemerkung = u""
        self._v2_str4 = u""
        self._v2_str6 = u""
        self._v2_str7 = u""
        self._short_einsatz_info_text = u""
        self._einsatz_haupttext = u""
        self._ts_dme = None
        self._ts_system = datetime.datetime.now()
        self._is_menschengefahr = False
        self._is_probealarm = False
        self._is_valid = False
        self._parse(self._einsatz_text)

    def _parse(self, einsatz_text):
        # Wandelt Dezimalzahlen mit dem Format {Zahl1},{Zahl2} in {Zahl1}.{Zahl2} um.
        self._einsatz_text = re.sub(r"(\d+),(\d+)", "\g<1>.\g<2>", einsatz_text)

        meldender = False

        zeilen = self._einsatz_text.split(u"\r\n")
        if len(zeilen) >= 2:
            timestamp = zeilen[1]
            self._datum = re.findall(r'\d{2}\.\d{2}\.\d{2}', timestamp)[0]
            self._uhrzeit = re.findall(r'\d{2}:\d{2}', timestamp)[0]
            self._ts_dme = datetime.datetime.strptime(self._datum + ' ' + self._uhrzeit, '%d.%m.%y %H:%M')
        if len(zeilen) >= 3:
            self._ric_str = zeilen[2]
            self._ric = int(self._ric_str[:2])
            self._ric_sub = self._ric_str[2]
        if len(zeilen) >= 4:
            text = zeilen[3]
            self._einsatz_haupttext = text
            if u"Probealarm" in text:
                self._is_valid = True
                self._is_probealarm = True  # Es handelt sich um ein Probealarm
                self._short_einsatz_info_text = u"Probealarm"
                self._stichwort = u'P'
                self._bemerkung = u'Probealarm'
            elif u'Info:' in text:
                self._is_valid = True
                self._stichwort = u'I'
                self._bemerkung = u'Info'
                self._short_einsatz_info_text = u"Info"
                self._bemerkung = text[5:].strip()
            else:
                split_text = text.split(u',')
                split_text_length = len(split_text)

                if split_text_length >= 1:
                    if split_text[0].startswith('#'):
                        self._format_version = 2
                        self._bma = split_text[0].strip()
                    else:
                        self._format_version = 1
                        self._stichwort = split_text[0].strip()
                        self._set_einsatz_info_text()

                if split_text_length >= 2:
                    # Ab diesem Punkt gilt ein Einsatz als ausgewertet
                    self._is_valid = True
                    if self._format_version == 1:
                        self._bma = split_text[1].strip()
                    elif self._format_version == 2:
                        self._stichwort = split_text[1].strip()
                        self._set_einsatz_info_text()

                if split_text_length >= 3:
                    if self._format_version == 1:
                        self._objekt = split_text[2].strip()
                    elif self._format_version == 2:
                        self._objekt = split_text[2].strip()

                if split_text_length >= 4:
                    if self._format_version == 1:
                        self._str_hnr = split_text[3].strip()
                    elif self._format_version == 2:
                        self._v2_str4 = split_text[3].strip()


                if split_text_length >= 5:
                    if self._format_version == 1:
                        self._ortsteil = split_text[4].strip()
                    elif self._format_version == 2:
                        self._str_hnr = split_text[4].strip()

                if split_text_length >= 6:
                    if self._format_version == 1:
                        self._gemeinde = split_text[5].strip()
                    elif self._format_version == 2:
                        self._v2_str6 = split_text[5].strip()

                if self._format_version == 1:
                    if split_text_length >= 7:
                        pass

                    if split_text_length >= 8:
                        meldender = False
                        if u"herr" in split_text[7].lower() or u"frau" in split_text[7].lower():
                            meldender = True
                            self._meldender = split_text[7] + split_text[6]

                        if meldender:
                            if split_text_length >= 9:
                                self._son_ort = split_text[8].strip()
                        else:
                            self._son_ort = split_text[7].strip()

                    if split_text_length >= 9 and not meldender:
                        for x in range(8, split_text_length):
                            self._bemerkung += " "
                            self._bemerkung += split_text[x].strip()

                    if split_text_length >= 10 and meldender:
                        for x in range(9, split_text_length):
                            self._bemerkung += " "
                            self._bemerkung += split_text[x].strip()

                    self._bemerkung = self._bemerkung.strip()

                elif self._format_version == 2:
                    if split_text_length >= 7:
                        self._v2_str7 = split_text[6].strip()

                    if split_text_length >= 8:
                        self._ortsteil = split_text[7].strip()

                    if split_text_length >= 9:
                        self._gemeinde = split_text[8].strip()

                    if split_text_length >= 10:
                        self._son_ort = split_text[9].strip()

                    if split_text_length >= 11:
                        for i in range(10, split_text_length):
                            self._bemerkung += " "
                            self._bemerkung += split_text[i].strip()
                        self._bemerkung = self._bemerkung.strip()

                # Leerzeichen aus dem Einsatztext entfernen
                self._einsatz_haupttext = ' '.join(self._einsatz_haupttext.split())



    def _set_einsatz_info_text(self):
        if self._stichwort == u'B1':
            self._short_einsatz_info_text = u'Brandeinsatz (klein)'
        elif self._stichwort == u'B1Y':
            self._short_einsatz_info_text = u'Brandeinsatz (klein) mit Menschengefährdung'
        elif self._stichwort == u'B2':
            self._short_einsatz_info_text = u'Brandeinsatz (mittel)'
        elif self._stichwort == u'B2Y':
            self._short_einsatz_info_text = u'Brandeinsatz (mittel) mit Menschengefährdung'
        elif self._stichwort == u'B3':
            self._short_einsatz_info_text = u'Brandeinsatz (groß)'
        elif self._stichwort == u'B3Y':
            self._short_einsatz_info_text = u'Brandeinsatz (groß) mit Menschengefährdung'
        elif self._stichwort == u'B4':
            self._short_einsatz_info_text = u'Brandeinsatz (groß)'
        elif self._stichwort == u'B4Y':
            self._short_einsatz_info_text = u'Brandeinsatz (groß) mit Menschengefährdung'
        elif self._stichwort == u'BMA':
            self._short_einsatz_info_text = u'Brandmeldeanlage'
        elif self._stichwort == u'WB1':
            self._short_einsatz_info_text = u'Böschungsbrand'
        elif self._stichwort == u'WB2':
            self._short_einsatz_info_text = u'Waldbrand bis 1000qm'
        elif self._stichwort == u'WB3':
            self._short_einsatz_info_text = u'Waldbrand über 1000qm'
        elif self._stichwort == u'WB4':
            self._short_einsatz_info_text = u'Waldbrand über 1000qm'
        elif self._stichwort == u'WB_1':
            self._short_einsatz_info_text = u'Böschungsbrand'
        elif self._stichwort == u'WB_2':
            self._short_einsatz_info_text = u'Waldbrand bis 1000qm'
        elif self._stichwort == u'WB_3':
            self._short_einsatz_info_text = u'Waldbrand über 1000qm'
        elif self._stichwort == u'WB_4':
            self._short_einsatz_info_text = u'Waldbrand über 1000qm'
        elif self._stichwort == u'WBK':
            self._short_einsatz_info_text = u'Wärmebildkamera'
        elif self._stichwort == u'H1':
            self._short_einsatz_info_text = u'Technische Hilfeleistung (klein)'
        elif self._stichwort == u'H1Y':
            self._short_einsatz_info_text = u'Technische Hilfeleistung (klein) mit Menschengefährdung'
        elif self._stichwort == u'H2':
            self._short_einsatz_info_text = u'Technische Hilfeleistung (mittel)'
        elif self._stichwort == u'H2Y':
            self._short_einsatz_info_text = u'Technische Hilfeleistung (mittel) mit Menschengefährdung'
        elif self._stichwort == u'H3':
            self._short_einsatz_info_text = u'Technische Hilfeleistung (groß)'
        elif self._stichwort == u'H3Y':
            self._short_einsatz_info_text = u'Technische Hilfeleistung (groß) mit Menschengefährdung'
        elif self._stichwort == u'VUPK':
            self._short_einsatz_info_text = u'Verkehrsunfall mit eingeklemmter Person'
        elif self._stichwort == u'W':
            self._short_einsatz_info_text = u'Wasserrettung'
        elif self._stichwort == u'WY':
            self._short_einsatz_info_text = u'Wasserrettung mit Menschengefährdung'
        elif self._stichwort == u'ABC_1':
            self._short_einsatz_info_text = u'ABC-Einsatz (klein)'
        elif self._stichwort == u'ABC_2':
            self._short_einsatz_info_text = u'ABC-Einsatz (mittel)'
        elif self._stichwort == u'ABC_3':
            self._short_einsatz_info_text = u'ABC-Einsatz (groß)'
        elif self._stichwort == u'ABC_4':
            self._short_einsatz_info_text = u'ABC-Einsatz (groß)'
        elif self._stichwort == u'DLK':
            self._short_einsatz_info_text = u'Drehleiter'
        elif self._stichwort == u'UEB':
            self._short_einsatz_info_text = u'Übung'
        elif self._stichwort == u'KFB':
            self._short_einsatz_info_text = u'Kreisfeuerwehrbereitschaft'
        elif self._stichwort == u'KFB (CE)':
            self._short_einsatz_info_text = u'Kreisfeuerwehrbereitschaft'
        elif self._stichwort == u'KFB_1':
            self._short_einsatz_info_text = u'Kreisfeuerwehrbereitschaft 1. Zug'
        elif self._stichwort == u'KFB_2':
            self._short_einsatz_info_text = u'Kreisfeuerwehrbereitschaft 2. Zug'
        elif self._stichwort == u'KFB_3':
            self._short_einsatz_info_text = u'Kreisfeuerwehrbereitschaft 3. Zug'
        elif self._stichwort == u'KFB_4':
            self._short_einsatz_info_text = u'Kreisfeuerwehrbereitschaft 4. Zug'
        elif self._stichwort == u'KFB_5':
            self._short_einsatz_info_text = u'Kreisfeuerwehrbereitschaft 5. Zug'
        else:
            self._short_einsatz_info_text = u'Sonstiges'

    @property
    def ric_text(self):
        """Gibt den RIC als String zurück. Zum Beispiel: 03B"""
        return self._ric_str

    @property
    def ric_nummer(self):
        """Gibt die RIC-Nummer als String zurück. Zum Beispiel: 03"""
        return self._ric

    @property
    def ric_unteradresse(self):
        """Gibt die RIC-Unteradresse als String zurück. Zum Beispiel: B"""
        return self._ric_sub

    @property
    def stichwort(self):
        """Gibt das Alarmierungsstichwort als String zurück."""
        return self._stichwort

    @property
    def ortschaft(self):
        """Gibt den Namen der Ortschaft als String zurück."""
        return self._gemeinde

    @property
    def ortsteil(self):
        """Gibt den Namen des Ortsteils als String zurück."""
        return self._ortsteil

    @property
    def einsatzort(self):
        """Gibt den Einsatzort als String zurück."""
        return self._str_hnr

    @property
    def ortszusatz(self):
        """Gibt den Zusatz zum Einsatzort als String zurück."""
        return self._son_ort

    @property
    def freitext(self):
        """Gibt den Freitext als String zurück."""
        return self._bemerkung

    @property
    def menschengefahr(self):
        """Gibt zurück, ob es sich um einen Einsatz mit Menschengefährdung handelt."""
        return self._is_menschengefahr

    @property
    def datetime_dme(self):
        """Gibt den Zeitstempel des Einsatzes zurück (Datum und Uhrzeit von DME)"""
        return self._ts_dme

    @property
    def datetime_system(self):
        """Gibt den Zeitstempel des Einsatzes zurück (Linux Systemzeit)"""
        return self._ts_system

    @property
    def short_einsatz_info(self):
        """Gibt eine kurze Information über den Einsatz zurück. Bei Probealarm: "Probealarm",
        sonst Alarmierungsstichwort - Freitext
        """
        return self._short_einsatz_info_text

    @property
    def einsatz_haupttext(self):
        """"Gibt den Haupttext zurück. (Einsatzmeldung ohne Zeitstempel und RIC)"""
        return self._einsatz_haupttext

    @property
    def probealarm(self):
        """Gibt zurück, ob es sich bei dem Einsatz um einen Probealarm handelt"""
        return self._is_probealarm

    @property
    def valid(self):
        """Gibt zurück, ob ein Einsatz ausgewertet werden konnte (Einsatztext)"""
        return self._is_valid

    @property
    def alarmdict(self):
        """Gibt ein Dictionary zurück, welches verschiedene Informationen über den
        Einsatz enthält"""
        alarmdict = {
            "ric": self._ric,
            "ric_sub": self._ric_sub,
            "uhrzeit": None,
            "datum": None,
            "bma": self._bma,
            "ts_dme": self._ts_dme,
            "ts_system": self._ts_system,
            "stichwort": self._stichwort,
            "stichwort_lang": self._short_einsatz_info_text,
            "bemerkung": self._bemerkung,
            "gemeinde": self._gemeinde,
            "ortsteil": self._ortsteil,
            "meldender": self._meldender,
            "son_ort": self._son_ort,
            "str_hnr": self._str_hnr,
            "objekt": self._objekt,
            "einsatztext": self._einsatz_haupttext,
            "v2_str4": self._v2_str4,
            "v2_str6": self._v2_str6,
            "v2_str7": self._v2_str7,
            "raw_hex": self._hexdata
        }
        return alarmdict
