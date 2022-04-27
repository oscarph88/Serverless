import json as j
import xml.etree.cElementTree as et

print('lambda function')

def lambda_handler(event, context):
    print(event['body'])
    data = j.loads(event['body'])
    
    root = et.Element("Reservation")
    header = et.SubElement(root, "header")
    et.SubElement(header,"echoToken").text = data["header"]["echoToken"]
    et.SubElement(header,"timestamp").text = data["header"]["timestamp"]

    reservation = et.SubElement(root, "body")
    hotel = et.SubElement(reservation, "hotel")
    et.SubElement(hotel,"uuid").text = data["reservation"]["hotel"]["uuid"]
    et.SubElement(hotel,"code").text = data["reservation"]["hotel"]["code"]
    et.SubElement(hotel,"offset").text = data["reservation"]["hotel"]["offset"]
    et.SubElement(reservation,"reservationId").text = str(data["reservation"]["reservationId"])

    confirmation = et.SubElement(reservation,"reservations")

    for z in data["reservation"]["confirmationNumbers"]:
        reservationSource = et.SubElement(confirmation,"reservation")
        reservationSource.set("source", z["source"])
        info = et.SubElement(reservationSource,"info")
        info.set("confirmationNumber", z["confirmationNumber"])
        et.SubElement(info,"firstName").text = z["guest"].split(' ')[0]
        et.SubElement(info,"lastName").text = z["guest"].split(' ')[1]

    et.SubElement(reservation,"lastUpdateTimestamp").text = str(data["reservation"]["lastUpdateTimestamp"])
    et.SubElement(reservation,"lastUpdateOperatorId").text = str(data["reservation"]["lastUpdateOperatorId"])

    tree = et.ElementTree(root)
    #tree.write("output.xml")

    print(et.tostring(root, encoding='utf8').decode('utf8'))

    #2 Contstruct the body of the response object
    transactionResponse = {}
    transactionResponse['XML'] = et.tostring(root, encoding='utf8').decode('utf8')
    transactionResponse['message'] = 'XML created correctly'

    #3 Construct http response object
    responseObject = {}
    responseObject['statusCode'] = 200
    responseObject['headers'] = {}
    responseObject['headers']['Content Type'] = 'application/json'
    responseObject['body'] = j.dumps(transactionResponse)

    #return the response object
    return responseObject