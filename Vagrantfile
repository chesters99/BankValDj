# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.define :localvm do |local|
    local.vm.box = "puppetlabs/centos-7.2-64-nocm"
    local.vm.network "forwarded_port", guest: 8000, host: 8000 # django runserver
    local.vm.network "forwarded_port", guest: 5555, host: 5555 # celery flower task monitor
    local.vm.network "forwarded_port", guest: 443, host: 8443   # nginx https
    local.vm.network "forwarded_port", guest: 80, host: 8080   # nginx http
    local.vm.network "forwarded_port", guest: 5432, host: 5432 # postgresql from pycharm
#    local.vm.network "public_network", ip: "192.168.0.5", bridge: "en0: Wi-Fi (AirPort)"
    local.vm.synced_folder '.', '/vagrant', disabled: true
    local.vm.synced_folder "/Users/graham/Documents/Projects/BankValDj", "/home/vagrant/BankValDj"
    local.vm.provider "virtualbox" do |vb|
      vb.gui = false
      vb.memory = "2048"
      vb.cpus = "3"
      vb.customize ["modifyvm", :id, "--ioapic", "on"]
    end
    config.vm.provision :ansible do |ansible|
#      ansible.verbose = "vvvv"
      ansible.playbook = "ansible/site.yml"
      ansible.inventory_path = "ansible/hosts"
      ansible.limit="localvm"
    end
  end

  config.vm.define :production do |prod|
    prod.vm.box_url = "https://github.com/mitchellh/vagrant-aws/raw/master/dummy.box"
    prod.vm.box = "dummy"
    prod.vm.synced_folder '.', '/vagrant', disabled: true
    prod.vm.provider :aws do |aws, override|
      aws.access_key_id = ENV['AWS_KEY']
      aws.secret_access_key = ENV['AWS_SECRET']
      aws.keypair_name = ENV['AWS_KEYNAME']
      aws.ami = "ami-6d1c2007"  # centos 7.2 in us-east-1 zone
      # "ami-2051294a" # redhat 7.2 in us-east-1 zone - too expensive and doesnt match dev environment
      aws.region = "us-east-1"
      aws.availability_zone = "us-east-1b" # should database replicate to diff zone
      aws.instance_type = "t2.micro"
      aws.security_groups = ['default']
      aws.elastic_ip = "52.86.44.119"
      config.ssh.insert_key = 'true'
      config.ssh.username="centos"
      override.ssh.username = "centos"
      override.ssh.private_key_path = ENV['AWS_KEYPATH']
    end
    config.vm.provision :ansible do |ansible|
#      ansible.verbose = "vvvv"
      ansible.playbook = "ansible/site.yml"
      ansible.inventory_path = "ansible/hosts"
      ansible.limit="production"
      ansible_user="centos"
      ansible_ssh_private_key_file="/Users/graham/Documents/Projects/BankValDj/BankValDj/settings/secret/USEast21Aug_secret.pem"
    end
  end
end
