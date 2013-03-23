IRC-Bot
=======

IRC-Bot uses the "jargon text" file, with a markov-chain algorithm for the text-generated, to 
create auto-responses.

#### set-up

The IRC-Client repo uses the sockets and threading modules, which are both in pythons 
standard library.  For the IRC-Bot I've used twisted to construct the client.  You will need to 
have twisted installed first. 

If you don't have twisted already, you can:

    pip install twisted
    

#### usage

`cd` to IRC-Bot's directory and run:

    python main.py

Give input for the fields prompted for:

    Name your bot: chatbot38
    Enter your name: tijko
    Host: irc.freenode.net
    Port: 6667
    Channel: somechannel

    Connected!
    Signed ON!
    Joined #somechannel

Once on the channel, if a user directs a question towards IRC-Bot, it will respond:

    tijko | whats going on today chatbot38?

    chatbot38 | know changed the generation how a lock up and sail stanford hackers may be mouse pointing device

