## Install

```bash
git clone https://github.com/rcaloras/dotfiles.git
ln -s "$PWD/dotfiles/.global_bash_profile" ~/.global_bash_profile
```

Add to your bash profile.

```bash
if [ -f ~/.global_bash_profile ]; then
    source ~/.global_bash_profile
fi
```

