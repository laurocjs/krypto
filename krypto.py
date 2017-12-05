from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import random
import string
import subprocess as sub

# Initialize the bot
myToken = ""
for line in open('myToken.token'): # Read your token file
    myToken += line
updater = Updater(token=myToken[0:-1]) # mine ends with an \n, so I cut it off
dispatcher = updater.dispatcher
print 'Krypto is running...'

# Initialize the words list
articles = [line.strip() for line in open('dict/articles')]
adjectives = [line.strip() for line in open('dict/adjectives')]
nouns = [line.strip() for line in open('dict/nouns')]
verbs = [line.strip() for line in open('dict/verbs')]
words = [line.strip() for line in open('dict/words')]

# Define each command method
# Start method is just a welcome message
def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Hi! I'm *Krypto*! I'm here to keep you safe!\nTip /help to see all my powers! _Woof_!\n", parse_mode='Markdown')

# Help method is a message explaining all the other commands
def helpmethod(bot, update):
    message= "Always here to help you!\n\n"
    message += "-- Passwords generators --\n"
    message += "/newshortpass 4 words (not safe)\n"
    message += "/newlongpass 6 words (safe *recommended*)\n"
    message += "/newsafepass random sentence (safe)\n"
    message += "/randomshortpass 8-character-long string (not safe)\n"
    message += "/randomlongpass 16-character-long string (safe)\n"
    message += "\n-- Keys Tools --\n"
    message += "\n/keygen 2048 bits RSA key\n"
    message += "\nMore methods _coming soon_! _Woof Woof_!\n"
    bot.send_message(chat_id=update.message.chat_id, text=message, parse_mode='Markdown')


# Generate a new password using 4 words. This password are no longer considered safe.
def newShortMemorablePassword(bot, update):
    password = ""
    passwordwithspace = ""
    for i in xrange(4): # change to _ instead of i, join instead of +=
        word = random.SystemRandom().choice(words + adjectives + nouns + verbs)
        password += word
        passwordwithspace += word + ' '
    message= "_Izzy_! Your new password is:\n" + password + '\n'
    message += "Remember it as:" + passwordwithspace + '\n'
    bot.send_message(chat_id=update.message.chat_id, text=message, parse_mode='Markdown')

# Generate a new password using memorable words. This password was recommended by Diceware.
def newLongMemorablePassword(bot, update):
    password = ""
    passwordwithspace = ""
    for i in xrange(6): # change to _ instead of i, join instead of +=
        word = random.SystemRandom().choice(words + adjectives + nouns + verbs)
        password += word
        passwordwithspace += word + ' '
    message = "_Shhowwow_! Your new password is:\n" + password + '\n'
    message += "Remember it as:" + passwordwithspace + '\n'
    bot.send_message(chat_id=update.message.chat_id, text=message, parse_mode='Markdown')

# Generate a random sentence to be used as a password.
def newSafePass(bot, update):
    word1 = random.SystemRandom().choice(articles)
    word2 = random.SystemRandom().choice(adjectives)
    word3 = random.SystemRandom().choice(nouns)
    word4 = random.SystemRandom().choice(verbs)
    word5 = random.SystemRandom().choice(articles)
    word6 = random.SystemRandom().choice(adjectives)
    word7 = random.SystemRandom().choice(nouns)
    password = word1 + word2 + word3 + word4.replace(" ", "") + word5 + word6 + word7
    passwordwithspace = word1 + ' ' + word2 + ' ' + word3 + ' ' + word4 + ' ' + word5 + ' ' + word6 + ' ' + word7
    message = "_Shaaaaazamm_! Your new password is:\n" + password + '\n'
    message += "Read it as: " + passwordwithspace + '\n'
    bot.send_message(chat_id=update.message.chat_id, text=message, parse_mode='Markdown')

# Random weak string, no one should use it nowadays.
def randomPass1(bot, update):
    password = ""
    for i in xrange(8):
        password += random.SystemRandom().choice(string.lowercase + string.digits)
    message = "_Wo wo_! Your new password is:\n" + password + '\n'
    bot.send_message(chat_id=update.message.chat_id, text=message, parse_mode='Markdown')

# A stronger string.
def randomPass2(bot, update):
    password = ""
    for i in xrange(14):
        password += random.SystemRandom().choice(string.letters + string.digits + string.punctuation)
    message = "_Hashaaashu_! Your new password is:\n" + password + '\n'
    bot.send_message(chat_id=update.message.chat_id, text=message, parse_mode='Markdown')

# Generate a 2048 bits RSA key
def generateKey(bot, update):
    message = "_Woooooooooooooof_!\nThis is your private key, *do not* share it!\n"
    # Generate key
    command = "openssl genrsa -out private.pem 2048".split()
    p = sub.Popen(command,stdout=sub.PIPE,stderr=sub.PIPE)
    output, errors = p.communicate()
    # Export private key
    command = "openssl rsa -in private.pem -outform PEM -pubout -out public.pem".split()
    p = sub.Popen(command,stdout=sub.PIPE,stderr=sub.PIPE)
    output, errors = p.communicate()
    # Export public key
    command = "openssl rsa -in private.pem -out private_unencrypted.pem -outform PEM".split()
    p = sub.Popen(command,stdout=sub.PIPE,stderr=sub.PIPE)
    output, errors = p.communicate()
    # Read keys files
    privKey = ""
    for line in open('private_unencrypted.pem'):
        privKey += line
    pubKey = ""
    for line in open('public.pem'):
        pubKey += line

    message += privKey + '\n'
    message += '\nAnd here your public key is! You *can* share it!\n'
    message += pubKey + '\n'

    # Send message and the files .pem
    bot.send_message(chat_id=update.message.chat_id, text=message, parse_mode='Markdown')
    f = open('private_unencrypted.pem')
    bot.send_document(chat_id=update.message.chat_id, document=f, str='ChavePrivada.pem')
    f = open('public.pem')
    bot.send_document(chat_id=update.message.chat_id, document=f, str='ChavePublica.pem')

    # Remove the key files, we cannot keep them
    command = "rm -f private.pem private_unencrypted.pem public.pem".split()
    p = sub.Popen(command,stdout=sub.PIPE,stderr=sub.PIPE)
    output, errors = p.communicate()


# Create handlers for each method
start_handler = CommandHandler('start', start)
help_handler = CommandHandler('help', helpmethod)
# Password handlers
newshortpass_handler = CommandHandler('newshortpass', newShortMemorablePassword)
newlongpass_handler = CommandHandler('newlongpass', newLongMemorablePassword)
newsafepass_handler = CommandHandler('newsafepass', newSafePass)
newpass_handler = CommandHandler('randomshortpass', randomPass1)
newpass2_handler = CommandHandler('randomlongpass', randomPass2)
# Keys handlers
keygen_handler = CommandHandler('keygen', generateKey)

# Add the handlers to the dispatcher
dispatcher.add_handler(start_handler)
dispatcher.add_handler(help_handler)
dispatcher.add_handler(newshortpass_handler)
dispatcher.add_handler(newlongpass_handler)
dispatcher.add_handler(newsafepass_handler)
dispatcher.add_handler(newpass_handler)
dispatcher.add_handler(newpass2_handler)
dispatcher.add_handler(keygen_handler)

# Start polling
updater.start_polling()
