import eg
import httplib
import xml.etree.ElementTree as ET
import urllib

eg.RegisterPlugin(
    name = "HTTP Relay",
    author = "klemensl",
    version = "0.0.1",
    kind = "other",
    description = "..."
)

class HTTPRelay(eg.PluginBase):

    def __init__(self):
        self.AddAction(sendYowsupMessage)
        self.AddAction(sendRequest)
        self.AddAction(sendPOSTRequestWithBody)
		
    def __start__(self):
        #self.host = host
        #self.port = port
        #print "HTTPRelay Plugin is started with parameter: {0}:{1}".format(self.host, self.port)
        print "HTTPRelay Plugin started"
				
    def Configure(self):
        panel = eg.ConfigPanel(self)
        while panel.Affirmed():
            panel.SetResult()

    def SendGETRequest(self, protocol, host, port, request):
        print "sending request to: {0}:{1}{2}".format(host, port, request)
        conn = httplib.HTTPConnection(host, port)
        conn.request("GET", request)
        response = conn.getresponse()
        data = response.read()
        conn.close()
        if '?>' in data:
            dataBody = data.partition('?>')[2]
        else:
            dataBody = data
        print "DEBUG", response.status, response.reason, dataBody
        return dataBody

    def SendPOSTRequest(self, protocol, host, port, request, body=None, headers=None):
        print "sending request to: {0}:{1}{2}".format(host, port, request)
        conn = httplib.HTTPConnection(host, port)
        conn.request("POST", request, body, headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
        if '?>' in data:
            dataBody = data.partition('?>')[2]
        else:
            dataBody = data
        print "DEBUG", response.status, response.reason, dataBody
        return dataBody
			
	
class sendYowsupMessage(eg.ActionBase):
    name = "Send a message using Yowsup"

    def __call__(self, protocol, host, port, message):
        message = message.encode('utf-8')
        print "Sending message '{0}'".format(message)
        parameter = urllib.urlencode({'message' : message})
        dataBody = self.plugin.SendGETRequest(protocol, host, port, "/cgi-bin/yowsup.py?{0}".format(parameter))
        

    def Configure(self, protocol="http", host="192.168.1.103", port=80, message=""):
        panel = eg.ConfigPanel(self)
        protocolCtrl = panel.TextCtrl(protocol)
        hostCtrl = panel.TextCtrl(host)
        portCtrl = panel.SpinIntCtrl(port, min=1, max=65535)
        messageCtrl = panel.TextCtrl(message)
        panel.sizer.AddMany([
            panel.StaticText("Protocol:"),
            protocolCtrl,
            panel.StaticText("Host:"),
            hostCtrl,
            panel.StaticText("Port:"),
            portCtrl,
            panel.StaticText("Message:"),
            messageCtrl,
        ])
        while panel.Affirmed():
            panel.SetResult(
                protocolCtrl.GetValue(),
                hostCtrl.GetValue(),
                portCtrl.GetValue(),
                messageCtrl.GetValue(),
            )

class sendRequest(eg.ActionBase):
    name = "Send a GET request"

    def __call__(self, protocol, host, port, request):
        #request = request.encode('utf-8')
        eg.globals.httprelayresponse = self.plugin.SendGETRequest(protocol, host, port, request)
        
				
    def Configure(self, protocol="http", host="192.168.1.101", port=8000, request=""):
        panel = eg.ConfigPanel(self)
        protocolCtrl = panel.TextCtrl(protocol)
        hostCtrl = panel.TextCtrl(host)
        portCtrl = panel.SpinIntCtrl(port, min=1, max=65535)
        requestCtrl = panel.TextCtrl(request)
        panel.sizer.AddMany([
            panel.StaticText("Protocol:"),
            protocolCtrl,
            panel.StaticText("Host:"),
            hostCtrl,
            panel.StaticText("Port:"),
            portCtrl,
            panel.StaticText("Request:"),
            requestCtrl,
        ])
        while panel.Affirmed():
            panel.SetResult(
                protocolCtrl.GetValue(),
                hostCtrl.GetValue(),
                portCtrl.GetValue(),
                requestCtrl.GetValue(),
            )

class sendPOSTRequestWithBody(eg.ActionBase):
    name = "Send a POST request"

    def __call__(self, protocol, host, port, request, body):
        #request = request.encode('utf-8')
        headers = {"Content-type": "text/xml"}
        eg.globals.httprelayresponse = self.plugin.SendPOSTRequest(protocol, host, port, request, body, headers)
        
				
    def Configure(self, protocol="http", host="192.168.1.101", port=8000, request="", body=""):
        panel = eg.ConfigPanel(self)
        protocolCtrl = panel.TextCtrl(protocol)
        hostCtrl = panel.TextCtrl(host)
        portCtrl = panel.SpinIntCtrl(port, min=1, max=65535)
        requestCtrl = panel.TextCtrl(request)
        bodyCtrl = panel.TextCtrl(body, style=wx.TE_MULTILINE)
        panel.sizer.AddMany([
            panel.StaticText("Protocol:"),
            protocolCtrl,
            panel.StaticText("Host:"),
            hostCtrl,
            panel.StaticText("Port:"),
            portCtrl,
            panel.StaticText("Request:"),
            requestCtrl,
            panel.StaticText("Body:"),
            bodyCtrl,
        ])
        while panel.Affirmed():
            panel.SetResult(
                protocolCtrl.GetValue(),
                hostCtrl.GetValue(),
                portCtrl.GetValue(),
                requestCtrl.GetValue(),
                bodyCtrl.GetValue(),
            )