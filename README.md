# Final-Project-Augment-Augu
Final Project for HCDE 310, uses Discord API to create a bot that performs calculations for the game Teamfight Tactics
This Project is a helping tool for the autobattler game Teamfight Tactics.

It covers two main functionalities: Finding the amount of rolls remaining, and Finding Unit (also called Champions) specific odds:

Finding Rolls Remaining:
The game centers around refreshing a shop that offers 5 different units, in order to buy units that synergise with each other. It is really important to know how much you can refresh the shop because while it is easy to see without any modifiers, Augments are modifiers that heavily change the way the shop refreshes occur. Finding rolls remaing can be done by using the $roll X command, where X is any integer representation of the gold you have. It will automatically check if you have declared youself to have any augments, and take those into account.

Finding Champion Odds:
This helps users find the likelihood of seeing a champion when they roll, it also calculates the amount of rolls you should expect to do to find that Champion, and how much gold it will correlate to (which is not linear due to the Augment modifiers). You use this command by inputting $find X, where X is the name of a champion. This will then prompt you to enter two integers separate by a space, in an X Y format, where X is the number of that champion currently in play (not in the pool to roll for) and Y is the other champions of that tier in play (the more in play, the higher your odds of getting your desired champion). Only existing champions can be found, and not every champion can be found at all levels, so you might have to level up a bit before you can find a champion! If you are not familiar with TFT Champions, a list can be found here https://tftactics.gg/champions, but I like to use Jinx (tier 5- hard to find) and Lulu (Tier 2- easy to find) in testing because they cover a pretty wide spread.

Other commands:
$New or $Augur- The bot creates a fresh start
$Help- Very useful command, gives info about all the commands
$Add Golden Ticket and $Add High End Shopping- Adds Augment Modifiers, can be reversed by replacing "Add" with "Remove" (This can also be used on levels!)
$Set level X- Sets the level to the desired level
$Profile- Shows your profile info (Here profile means current modeled game statistics, not your personal info)


To Get Started: Run the program after completing the set-up and inviting the bot to your server, then type $New if you want to start from the beginning of the user flow, or try using other commands if you want.

The bot doesn't react to messages that aren't commands or requested user input, I intended for it to be used by fairly high level players so it makes some allowances for different syntaxes (like lvl instead of level and gt instead of Golden Ticket, as well as the occaisional extra space), but generally the bot is pretty clear about syntax and ignores stuff that doesn't match it. Likewise, it is intended to be used as more of a quick and easy tool for players using it more as a tool than as a toy, so while I coded around the standard mishaps (like trying to find the odds of a champion that can't be found, or a champion that doesn't exist), it is assumed that users aren't trying to break it by spamming it with another discord bot to overload it, or restricting its permissions (which would be a set up issue). 

Either way, have fun testing it out, I certainly had fun making it!
