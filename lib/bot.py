#!/usr/bin/env python

from twisted.internet import reactor
from twisted.internet.protocol import ClientFactory
from twisted.words.protocols import irc
import re
import psycopg2
import urllib2
import json
import passwords

ticker_type = ["ETF", "Equity"]
exchanges = ["NASDAQ", "NYSE"]
one_letter_words = ["A", "I"]

# our connection
conn = psycopg2.connect(database=passwords.Live.database, user=passwords.Live.user, password=passwords.Live.password, host=passwords.Live.host, port=passwords.Live.port)
cur = conn.cursor()
print "Opened database successfully"

def is_valid_stock(ticker):
	url = "http://d.yimg.com/autoc.finance.yahoo.com/autoc?query="+str(ticker)+"&callback=YAHOO.Finance.SymbolSuggest.ssCallback"
	response = urllib2.urlopen(url)
	html = response.read().lstrip("YAHOO.Finance.SymbolSuggest.ssCallback(").rstrip(")")
	data = json.loads(html)
	try:
		if data["ResultSet"]["Result"][0]["typeDisp"] in ticker_type and data["ResultSet"]["Result"][0]["exchDisp"] in exchanges:
			return True
		else:
			return False
	except Exception as e:
		pass

class Bot(irc.IRCClient):
    nickname = raw_input('Name your bot: ')
    realname = raw_input('Enter your name: ')

    def connectionMade(self):
        irc.IRCClient.connectionMade(self)     
        print '\nConnected!'

    def connectionLost(self, reason):
        irc.IRCClient.connectionLost(self, reason)
        #print 'Lost connection %s' % reason

    def signedOn(self):
        self.join(self.factory.channel)
        #print 'Signed On!'

    def joined(self, channel):
        self.channel = channel
        #print 'Joined %s' % channel

    def register(self, nickname, hostname='foo', servername='bar'):
        self.nickname = nickname
        if self.password is not None:
            self.sendLine("PASS %s" % self.password)
        self.setNick(nickname)
        if self.username is None:
            self.username = nickname
        self.sendLine("USER %s %s %s :%s" % 
                      (self.username, hostname, servername, self.realname))

    def irc_PING(self, prefix, params):
        #print 'Ping --> %s' % params
        self.sendLine("PONG %s" % params[-1])

    def privmsg(self, user, channel, msg):
        user = user.split('!')[0]
        #print '%s | %s' % (user, msg)
	regex = re.compile("[A-Z]+\s\(")
	#regex = re.compile("[A-Z]+\s")
	tickers = regex.findall(msg)
	for t in tickers:
		t = t.strip('(')
		if is_valid_stock(t.replace(" ", "")) and not t.replace(" ", "") in one_letter_words:
			cur.execute("SELECT count(*) from STOCKS where stock=\'"+str(t)+"\'")
			rows = cur.fetchall()
			for row in rows:
				if int(row[0]) > 0:
					cur.execute("UPDATE STOCKS SET count = count + 1 WHERE stock =\'"+str(t)+"\'")
					conn.commit()
					cur.execute("UPDATE STOCKS SET last_modified = current_timestamp WHERE stock =\'"+str(t)+"\'")
					conn.commit()
				else:
					cur.execute("INSERT INTO STOCKS (STOCK,COUNT,LAST_MODIFIED) VALUES (\'"+str(t)+"\',1,current_timestamp)");
					conn.commit()
				#print "Records created successfully";
	#conn.close()

class Proto4Bot(ClientFactory):

    def __init__(self):
        self.channel = '#' + raw_input('Channel: ')
        self.protocol = Bot

    def clientConnectionLost(self, connector, reason):
        connector.connect()

