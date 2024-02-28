A small bash script for checking if your password has appeared in any pastes known to haveibeenpwned.com

You should of course not trust it and look at its code before you give it any of your passwords.  What it does is:
1) Hash your password.
2) Send the first 5 characters of the hash to an online API.
3) The API returns a list of full hashes that begin as such.
4) The script then looks for the remainder of the hash amongst those and shows you.

See also: https://haveibeenpwned.com/API/v2#PwnedPasswords
