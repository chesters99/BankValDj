# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.box = "puppetlabs/centos-7.2-64-nocm"
  config.vm.network "forwarded_port", guest: 8000, host: 8000
  config.vm.network "public_network", ip: "192.168.0.5", bridge: "en0: Wi-Fi (AirPort)"
  # config.vm.synced_folder "../data", "/vagrant_data"
  config.vm.provider "virtualbox" do |vb|
    vb.gui = false
    vb.memory = "1024"
  end
  config.vm.provision :ansible do |ansible|
#    ansible.verbose = "vvv"
    ansible.playbook = "ansible/vagrant.yml"
  end
end
