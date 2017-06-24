#!/bin/sh

/var/www/snowmap/reset/countreset.pl
cp /var/www/snowmap/log/counter/reset.dat /var/www/snowmap/log/counter/scounter.dat
cp /var/www/snowmap/log/counter/reset.dat /var/www/snowmap/log/counter/gcounter.dat
cp /var/www/snowmap/log/counter/reset.dat /var/www/snowmap/log/counter/gcounter30.dat

chmod 777 /var/www/snowmap/log/counter/scounter.dat
chmod 777 /var/www/snowmap/log/counter/gcounter.dat
chmod 777 /var/www/snowmap/log/counter/gcounter30.dat

/var/www/snowmap/reset/replace.pl
