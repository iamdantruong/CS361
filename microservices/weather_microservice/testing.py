import send_zip



rpc = send_zip.SendZipClient('96817')
response = rpc.call()
#print(response)
print("city is  "+ response['name'])
print("temperature is "+str(response['main']['temp']))