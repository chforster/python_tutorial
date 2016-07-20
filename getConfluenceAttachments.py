#!/usr/bin/python
import sys, string, xmlrpclib, re, getpass

server = xmlrpclib.ServerProxy('https://confluence.netconomy.net/rpc/xmlrpc')
token = server.confluence2.login(raw_input("User: "), getpass.getpass("Password: "))
space = 'SNSLEXT'
pagetree = server.confluence2.getPages(token, space) # Creates a list of dicts
allattachments = []
for pagedict in pagetree:
    pageid = pagedict['id'] # Pulls the ID from the current dict from the pagetree list
    pagetitle = pagedict['title']
    attachments = server.confluence2.getAttachments(token, pageid) # Creates another list of dicts
    d = {'title': pagetitle, 'id': pageid,'attachments': attachments} # Adds attachment list to a temp dict
    allattachments.append(d) # Appends each new dict to the allattachments list
# print the page title and all attachments and their file types from the first dict in the allattachments list
for each in allattachments:
    print each['title']+' '+each['id']
    for attachmentss in each['attachments']:
        print '...'+attachmentss['title'], attachmentss['url'],attachmentss['contentType']
exit('Done!')
