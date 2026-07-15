sudo apt update
sudo apt install kali-linux-large -y
sudo apt update
sudo apt install zsh git curl wget -y
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
echo $SHELL
chsh -s /bin/zsh
nano ~/.zshrc
source ~/.zshrc
chsh -s /bin/zsh
