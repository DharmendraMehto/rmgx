import os.path
import shutil
import mysql.connector
import pandas as pd
from tqdm import tqdm
import datetime
import smtplib
from email.mime.text import MIMEText

mysqlConnection={
"host":"<mysqlserverip>",
"user":'<mysqluser>',
"password":'<mysqluserpassword>',
"port":'<mysqlport>',
"database":"<mysqldatabase>"
} # mysql connection variables
csvDataPath=r"C:\temp\file.csv" # path of data
successCSVFileMovePath=r"c:\temp\completed" # path of folder where file will move after completion of upload
validProvince=['NewDelhi', 'Lucknow', 'UP', 'Mumbai', 'Keral'] # filtering valid data from csv file
totalRecords=0 # Variables for total records of csv which will use later
smtpServer="smtp.gmail.com" # mail setup
smtpPort=587 #
smtpUser="<usermailid>"
smtpUserPassword="<mailidpassword>"
fromMailID="<fromMailid>"
toMailId="<tomailid>"

def CleanData(csvfilepath):
    try:
        if not os.path.exists(csvfilepath):
            print("File not available on path, please keep file on path.")
            exit()
        global totalRecords
        df=pd.read_csv(csvfilepath) # read csv files records and create data frame
        totalRecords=len(df) # Total records available in csv
        df=df.drop_duplicates(subset=["order_id"]) # remove duplicate records.
        df=df[df["origin_province"].isin(validProvince) & df["destination_province"].isin(validProvince)] # filter valid province data
        df['cost']  =df['cost'].fillna(0) # fill 0 where na available for cost field
        return df
    except Exception as ax:
        print(f"Exception caught while data cleanup: {str(ax)}")
        exit()

def LoadDataToMysql(CleanedData):
    mysqlCon = mysql.connector.connect(**mysqlConnection) # connect to mysql server
    rejectedCount = totalRecords - len(CleanedData)  # rejectedrecords count after cleaning the data
    if mysqlCon.is_connected():
        insertQuery="Insert into shipments(order_id, carrier_name, ship_date, delivery_date, weight, origin_province, destination_province, status, cost) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        validrecords=[] #store multiple records for bulk insert
        cur = mysqlCon.cursor()
        for i, v in tqdm(CleanedData.iterrows(), total=len(CleanedData), desc="Loading data to mysql server .."):
            record=(v["order_id"],v["carrier_name"],v["ship_date"],v["delivery_date"],v["weight"],v["origin_province"],v["destination_province"], v["status"], v["cost"])
            validrecords.append(record)
            if len(validrecords) > 10000:
                try:
                    cur.executemany(insertQuery,validrecords) # bulk data insertion
                    mysqlCon.commit() # commit the changes
                    validrecords=[] #blank the record list
                except Exception as ex:
                    rejectedCount=rejectedCount+len(validrecords) #store rejected record count

        try:
            cur.executemany(insertQuery,validrecords) # remaining records bulk upload
            mysqlCon.commit() # commit the changes.
        except Exception as ex:
            rejectedCount=rejectedCount+len(validrecords) # store rejected records
    mysqlCon.close() # close connection
    return rejectedCount # return rejected count

def SendMail(mailbody, subjectline):

    msg = MIMEText(mailbody)
    msg['From'] = fromMailID
    msg['To'] = toMailId
    msg['Subject'] = subjectline

    server=smtplib.SMTP(smtpServer, smtpPort)
    server.starttls()
    server.login(smtpUser,smtpUserPassword)
    server.send_message(msg)
    server.quit()

if __name__=="__main__":
    os.makedirs(successCSVFileMovePath, exist_ok=True) # Checked fodler available if not create folder.
    starttime=datetime.datetime.now() #store datetime in variable of start time of execution
    validdata=CleanData(csvDataPath) # validate data remove duplicate and validate with province
    rejectedcount=LoadDataToMysql(validdata)
    endtime=datetime.datetime.now() #store date time in variable of execution completed
    timeDifference=endtime-starttime #store difference of datetime start and end of execution
    summary={"TotalRecordsInCsv":totalRecords,"ProcessedRecords":totalRecords-rejectedcount,
             "RejectedCount":rejectedcount,"TotalProcessedTimeInSeconds":timeDifference.total_seconds()}
    shutil.move(csvDataPath, os.path.join(successCSVFileMovePath, os.path.basename((csvDataPath+"_"+datetime.datetime.now().strftime("%Y%m%d"))))) # move file to completed directory
    SendMail(str(summary),"Shipment Upload Summary!") # send mail of upload report



