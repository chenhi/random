# checkpw

A small bash script for checking if your password has appeared in any pastes known to haveibeenpwned.com

You should of course not trust it and look at its code before you give it any of your passwords.  What it does is:
1) Hash your password (without any trailing newline).
2) Send the head (first 5 characters) of the hash to an online API.
3) The API returns a list of tails (last 35 characters) of pwned passwords that begin with that head.
4) The script then looks for your hash tail amongst those and shows you if it appears.

See also: https://haveibeenpwned.com/API/v2#PwnedPasswords
