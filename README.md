tvkaista-wmc
============

Tvkaista windows media center client

Note: Author has no relations to the tvkaista service, he is just a customer of the service.

Documentation only in Finnish. Sorry.

Tämä on Windows 7:n Media Centerille tekemäni tvkaista-sovellus. Se oli käytössä julkisesti käytössä 2012 joulukuuhun
asti, jolloin lopetin sen ylläpitämisen vähäisen käytön takia. Päätin kuitenkin julkaista nyt sovelluksen koodin.
Huomio: Tämä perustuu kaukaisesti tvkaista-xbmc -sovellukselle, mutta kaikki siitä otetut osat ovat minun kirjoittamiani,
ja tämä on julkaistu eri lisenssillä (Affero GPL v3) kuin xbmc-sovellus (jonka lisenssi on GPLv2 tai myöhempi,
ja se sisältää myös muiden kuin minun kirjoittamaani koodia).

Asennus
-------

Ohjetta kirjoittaessa tekijällä oli käytössä Rackspace.co.uk:n Centos 6.4 -virtuaalikone. Komennot on testattu
toimiviksi sillä.

Asenna apache

    yum -y install httpd

Konfiguroi apache ymmärtämään .cgi -päätteiset tiedostot ohjelmiksi ja salli niiden ajo documentrootista.

    sed -i -e "s/#AddHandler cgi-script .cgi/AddHandler cgi-script .cgi/" \
    -e "s/Options Indexes FollowSymLinks/Options ExecCGI Indexes FollowSymLinks/" \
    /etc/httpd/conf/httpd.conf

Laita tvkaistawmc.cgi ja static/Controls2.xml apachen dokumenttijuureen

    cd /var/www/html
    wget https://raw.github.com/viljoviitanen/tvkaista-wmc/master/tvkaistawmc.cgi
    chmod a+rx tvkaistawmc.cgi
    mkdir static
    cd static
    wget https://raw.github.com/viljoviitanen/tvkaista-wmc/master/static/Controls2.xml

Laita apache käynnistymään bootissa ja (uudelleen)käynnistä se

    chkconfig httpd on
    service httpd restart

Valinnaisesti, "tehoa" sovellukseen saa lisää laittamalla memcached:n ja python-kirjastot käyttöön

    yum -y install memcached python-memcached
    chkconfig memcached on
    service memcached start

Jos koneessa/ympäristössä on palomuuri, pitää tietenkin sallia sisääntulevat portin 80 yhteydet. Amazonin
EC2-ympäristössä portteja avataan hallintakonsolista, Rackspacen Centos-koneessa se menee esim. näin:

    sed -i '/dport 22/i-A INPUT -m state --state NEW -m tcp -p tcp --dport 80 -j ACCEPT' /etc/sysconfig/iptables
    service iptables restart
    
Tämän jälkeen linkin, joka käynnistää media centerin, saa osoitteesta `http://<palvelimesi>/tvkaistawmc.cgi/link`

*Huomio: Tämän enempää ohjeita ohjelman asennuksesta tai käytöstä tekijältä ei kannata pyytää.
Tekijää ei myöskään kiinnosta ohjelman mahdolliset bugit tai parannusehdotukset. Jos tarjoat ohjelman ajoon
julkisesti, huomioi lisenssi.*
