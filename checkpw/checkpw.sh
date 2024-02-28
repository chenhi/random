#! /bin/bash

if [ $# -eq 0 ]; then
    >&2 printf "Usage: \n checkpw 'yourpassword' \nEnclose in single quotes 'password' to handle special characters. To avoid saving the password to your bash history, begin the line with a space.\n"
    exit 1
fi

hash=`echo -n "$1" | sha1sum | cut -f 1 -d " "`
head=`echo $hash | cut -b -5`
tail=`echo $hash | rev | cut -b -35 | rev`

curl -s "https://api.pwnedpasswords.com/range/$head" | grep -i $tail

