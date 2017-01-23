if [ -f app.pem ] ; then
	mv app.pem key.pem
fi

if [ -f app.zip ] ; then
	rm app.zip
fi

7z a app.zip key.pem
cd app
7z a ../app.zip *
cd ..
