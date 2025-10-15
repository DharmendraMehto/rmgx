import mysql.connector
import pandas as pd
import os
import smtplib
from email.message import EmailMessage

mysqlConnection={
"host":"<mysqlid>",
"user":'<mysqluser>',
"password":'<mysqlpassword>',
"port":'<mysqlport>',
"database":"<mysqldatabase>"
}

reportPath=r"C:\temp"
intervalDay=1
smtpServer="smtp.gmail.com"
smtpPort=587
smtpUser="<maildid>"
smtpUserPassword="<mialidpassword>"
fromMailID="<frommailid>"
toMailId="<tomailid>"


def SendMail(mailbody, subjectline):

    msg = EmailMessage()
    msg['From'] = fromMailID
    msg['To'] = toMailId
    msg['Subject'] = subjectline
    msg.set_content(mailbody)
    filenames=["CountPerCarrierAvgCost.xlsx","DelayedShipment.xlsx","ShipmentDoneYesterday.xlsx"]
    for file_path in filenames:
        with open(os.path.join(reportPath,file_path), "rb") as f:
            file_data = f.read()
            file_name = f.name
        msg.add_attachment(file_data, maintype="application", subtype="octet-stream", filename=file_name)

    server=smtplib.SMTP(smtpServer, smtpPort)
    server.starttls()
    server.login(smtpUser,smtpUserPassword)
    server.send_message(msg)
    server.quit()


def FetchReport():

    os.makedirs(reportPath, exist_ok=True) # create folder if not exists
    mysqlcon=mysql.connector.connect(**mysqlConnection)

    if mysqlcon.is_connected():
        cur=mysqlcon.cursor()
        # Total shipments processed yesterday
        query=f"Select id,order_id,carrier_name,ship_date,delivery_date,weight,origin_province,destination_province,status,cost  from shipments where  STATUS = 'Delivered' and delivery_date >= concat(current_date-interval {intervalDay} day, ' 00:00:00') and delivery_date <= concat(current_date-interval {intervalDay} day, ' 23:59:59')"
        cur.execute(query)
        columns = [column[0] for column in cur.description] # columns of reports
        yesterdayDoneReport=cur.fetchall()
        shipmentdoneReport=pd.DataFrame(yesterdayDoneReport, columns=columns)
        shipmentdoneReport.to_excel(os.path.join(reportPath,"ShipmentDoneYesterday.xlsx"), index=False)

        #Count per carrier and average cost

        query="SELECT carrier_name as Carrier_Name, COUNT(id) as Count, AVG(cost) as AverageCost FROM shipments GROUP BY carrier_name"
        cur.execute(query)
        columns = [column[0] for column in cur.description] # columns of report xlsx file
        countPercarrier=cur.fetchall() # fetch all records and save in variable
        countPerCarrierReport=pd.DataFrame(countPercarrier, columns=columns) # save data in pandas frame to save as excel file
        countPerCarrierReport.to_excel(os.path.join(reportPath,"CountPerCarrierAvgCost.xlsx"), index=False) # Save file as excel

        # Delayed shipments (status != ‘Delivered’ and delivery_date < CURDATE()).

        query="Select id,order_id,carrier_name,ship_date,delivery_date,weight,origin_province,destination_province,status,cost  from shipments where  STATUS <> 'Delivered' and delivery_date <= now()"

        cur.execute(query)
        columns=[column[0] for column in cur.description] # columns of report xlsx file
        delayShipment=cur.fetchall() # fetch all records and save in variable
        delayShipmentReport=pd.DataFrame(delayShipment, columns=columns) # save data in pandas frame to save as excel file
        delayShipmentReport.to_excel(os.path.join(reportPath,"DelayedShipment.xlsx"), index=False)

FetchReport()
msg="""Dear Team,

Please find the attached report of shipments.

Regards,
Dharmendra mehto"""
SendMail(msg,"Shipment Reports!")

