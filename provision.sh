export DEBIAN_FRONTEND=noninteractive

sudo apt-get -y update

# Install Basics: Utilities and some Python dev tools
sudo apt-get -y install build-essential git vim curl wget unzip 

# Install MySQL
sudo debconf-set-selections <<< 'mysql-server-5.7 mysql-server/root_password password password'
sudo debconf-set-selections <<< 'mysql-server-5.7 mysql-server/root_password_again password password'
sudo apt-get -y install mysql-server-5.7

# Set Timezone (Server/MySQL)
sudo ln -sf /usr/share/zoneinfo/UTC /etc/localtime
sudo mysql_tzinfo_to_sql /usr/share/zoneinfo | mysql --user=root --password=password mysql

# Allow connections from outside the vagrant box
sudo sed -i "s/.*bind-address.*/bind-address = 0.0.0.0/" /etc/mysql/mysql.conf.d/mysqld.cnf
echo "Updated bind address to accept connections from all hosts"

mysql -uroot -ppassword -e "GRANT ALL ON *.* to 'root'@'%' identified by 'password';"
mysql -uroot -ppassword -e "FLUSH PRIVILEGES;"
sudo /etc/init.d/mysql restart

# Add 1GB swap for memory overflow
sudo fallocate -l 1024M /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo "/swapfile   none    swap    sw    0   0" | sudo tee -a /etc/fstab
printf "vm.swappiness=10\nvm.vfs_cache_pressure=50" | sudo tee -a /etc/sysctl.conf && sudo sysctl -p

# Allow caching of NFS file share
sudo apt-get install -y cachefilesd
echo "RUN=yes" | sudo tee /etc/default/cachefilesd