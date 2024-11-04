#!/bin/bash

echo "Montagem"
sshfs -v utxu188:/srv/www/htdocs/cip/cip /tmp/cip
read -p "Gerar arquivos: pressione qualquer tecla"
./irp_cip.py cip
read -p "Copiar .htpasswd: pressione qualquer tecla"
scp ../IrP_CIP_dados/.htpasswd utxu188:/home/irpirmandadeprog1/.
read -p "Desmontar: pressione qualquer tecla"
umount -v /tmp/cip

