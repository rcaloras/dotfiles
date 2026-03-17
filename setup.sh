#!/usr/bin/env bash 
# Setup File for Dotfiles
#
# Should be able to run with "bash setup.sh" or ./setup.sh


bash_profile_hook='
if [ -f ~/.global_bash_profile ]; then
    source ~/.global_bash_profile
fi
'

ln -sf "$PWD/.global_bash_profile" ~/.global_bash_profile

# Link Vim
ln -sf "$PWD/vimfiles/.vimrc" ~/.vimrc
ln -sf "$PWD/vimfiles/.vim" ~/.vim


# Add our file to our bashprofile if it doesn't exist yet
if grep -q "source ~/.global_bash_profile" "$HOME/.bashrc"
then
    :
else
    echo "$bash_profile_hook" >> "$HOME/.bashrc"
fi

# Add our file to our zsh profile if it doesn't exist yet
if grep -q "source ~/.global_bash_profile" "$HOME/.zshrc"
then
    :
else
    echo "$bash_profile_hook" >> "$HOME/.zshrc"
fi