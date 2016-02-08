# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.box = "puppetlabs/centos-7.2-64-nocm"
  config.vm.network "forwarded_port", guest: 8000, host: 8000 # django runserver
  config.vm.network "forwarded_port", guest: 443, host: 443   # nginx https
  config.vm.network "forwarded_port", guest: 80, host: 8080   # nginx http
  config.vm.network "forwarded_port", guest: 5432, host: 5432 # postgresql from pycharm
  config.vm.network "public_network", ip: "192.168.0.5", bridge: "en0: Wi-Fi (AirPort)"
  config.vm.synced_folder '.', '/vagrant', disabled: true
  config.vm.synced_folder "/Users/graham/Documents/Projects/BankValDj", "/home/vagrant/BankValDj"
  config.vm.provider "virtualbox" do |vb|
    vb.gui = false
    vb.memory = "1024"
    vb.cpus = "2"
    vb.customize ["modifyvm", :id, "--ioapic", "on"]
  end
  config.vm.provision :ansible do |ansible|
#    ansible.verbose = "vvv"
    ansible.playbook = "ansible/localvm.yml"
  end
end
