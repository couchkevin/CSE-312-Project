import socketserver

import globe
import myparser
import auth

import replies
import webs


class server(socketserver.BaseRequestHandler):
    def handle(self):
        dataraw = self.request.recv(2048)


        #check what sort of data we've received
        datatype = ''
        if (dataraw.find(b'POST') == 0) :
            datatype = 'Post'
        elif (dataraw.find(b'GET') == 0) :
            datatype = 'Get'

        #### GET FUNCTIONS ####
        if datatype == 'Get':
            data = dataraw.decode("utf-8") #since it's a get request we know it's just headers

            split1  = data.split("\r") #divide up
            split2  = split1[0].split(" ")
            path    = split2[1]
            print(path)
            if(path == "/"):#send them the homepage
                replies.sendmsg("200 OK", "Base", self)

            elif(path == "/auth"):#check if they're logged in first
                    if (auth.checkvalid(data,self) == True) :  # if its a real token
                        replies.sendmsg("200 OK", "Base2", self)
                        return
                    else:
                        replies.sendmsg('403 Forbidden', "Not allowed, wrong token. User must log in to view page",self)

            elif (path == '/websocket'):
                print("Web!")
                if (auth.checkvalid(data, self) == True) :  # if its a real token
                    print("Pass!")
                    webs.hands(data, self)
                      # add the client to the list
                    #sloppy
                    token3 = myparser.findbufferend(data, "Cookie:", "\r\n")
                    token3 += ';'  # add ; at the end to normalize the cookie format in case of misorder
                    token = myparser.findbufferend(token3, "token=", ";")
                    #
                    username = auth.GetUsername(token)
                    globe.clients.append([self,username]) #add self to list of connected users along with user name

                    webs.readsock(self,username)  # keep socket open
                else :
                    replies.sendmsg('403 Forbidden', "Not allowed, wrong token. User must log in to view page", self)
            elif (path == '/functions.js') :
                replies.sendmsg("Base3", "Base3", self)

        ### POST FUNCTIONS #####
        elif datatype == 'Post':
            pathindex = dataraw.find(b'/')  # find first / for the path
            postpath = myparser.findtill(dataraw, "/", 32)  # custom function to find / after pathindex up until 32

            if (postpath == 'create-account') :
                username = myparser.findbufferend(dataraw, b'name="Username"\r\n\r\n', b'\r\n-').decode('utf-8')
                password = myparser.findbufferend(dataraw, b'name="Password"\r\n\r\n', b'\r\n-').decode('utf-8')
                auth.create_account(username, password, self)

            if (postpath == 'login') :
                username = myparser.findbufferend(dataraw, b'name="Username"\r\n\r\n', b'\r\n-').decode('utf-8')
                password = myparser.findbufferend(dataraw, b'name="Password"\r\n\r\n', b'\r\n-').decode('utf-8')
                auth.login(username, password, self)


if __name__ == "__main__":
    host = "0.0.0.0"
    port = 8000
    token2 = 0


    server = socketserver.ThreadingTCPServer((host,port), server)
    server.serve_forever()
