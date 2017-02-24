==================================
ModularesEinsatzInformationsSystem
==================================
:Autor: Matti Borchers <matti.borchers@feuerwehrflotwedel.de>
:Version: 1.0
:Datum: 24.02.2017

Inhaltsverzeichnis
==================
1. Systemüberblick_
2. Modulbeschreibungen
3. Konfiguration des Systems

.. _Systemüberblick:

1. Systemüberblick
==================

2. Modulbeschreibungen
======================
Im folgenden werden die zur Verfügung stehenden Module beschrieben. Aktiviert bzw. deaktiviert
werden diese über die Konfiguration des MEIS.

Einsätze über die serielle Schnittstelle empfangen
--------------------------------------------------
Die Grundlage des Modularen Einsatzinformationssytems ist das Empfangen von Daten eines Digitalen
Meldeempfängers über eine serielle Schittstelle.

3. Konfiguation des Systems
===========================
Die oben beschriebenen Module des Systems können mit Hilfe einer Konfiguration
aktiviert/deaktiviert und verändert werden. Die Konfiguration hat folgenden Aufbau:

============  =======================================================
Element       Beschreibung
============  =======================================================
wehr          Enthält Informationen über die zugehörige Ortsfeuerwehr
hardware      Informationen über die angeschlossene Hardware
============  =======================================================