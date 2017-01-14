Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/trusty64"
  config.vm.synced_folder ".", "/var/webapps/mutual_funds/code",
    owner: "funds_user", group: "users"
  config.vm.network :private_network, ip: "172.16.0.19"
  config.vm.provider "virtualbox" do |v|
    v.memory = 1024
    v.cpus = 1
  end
end