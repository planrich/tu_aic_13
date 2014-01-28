# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "precise64"
  config.vm.box_url = "http://files.vagrantup.com/precise64.box"

  config.hostmanager.enabled = true
  config.hostmanager.manage_host = true
  config.hostmanager.ignore_private_ip = false
  config.hostmanager.include_offline = true

  config.vm.provider :virtualbox do |v|
    v.customize ["modifyvm", :id, "--memory", 1024]
  end
  
  config.vm.define 'g2t2-apps' do |node|
    node.vm.hostname = "g2t2-apps.vm"
    node.vm.network :private_network, ip: '10.17.42.11'
    node.vm.provision :hostmanager
    node.vm.provision :shell, :path => 'provision/g2t2-apps.sh'
  end

end
