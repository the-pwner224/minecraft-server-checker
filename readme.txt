This script will check a Minecraft server's status and report the number of
  connected players. Additionally, it can run in the background and send you
  notifications when other players are playing (Linux and Mac only).

================================================================================

Usage:

You must have Python 3 installed. At the top of the file, put in your server's
  hostname and port (you can use the domain name instead of IP address if the
  server has one).

In a terminal:

$ python3 minecraft.py check
Server Name: 2/20    (2 players are currently on, out of 20 maximum)

$ python3 minecraft.py
(this will run in background and send notifications when player count changes)

================================================================================

This uses code from Nope's answer at https://gaming.stackexchange.com/a/166587,
  licensed CC BY-SA 3.0 (https://creativecommons.org/licenses/by-sa/3.0/).
Changes made to format of code, and extra features added as described above.
This code is also licensed CC BY-SA 3.0.
