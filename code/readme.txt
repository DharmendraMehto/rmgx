Configure below variable in part2.py to run this script.

mysqlConnection={
"host":"<mysqlserverip>",
"user":'<mysqluser>',
"password":'<mysqluserpassword>',
"port":'<mysqlport>',
"database":"<databasewhichcreatedearlier>"
} # mysql connection variables

csvDataPath=r"C:\temp\file.csv" # path of data
successCSVFileMovePath=r"c:\temp\completed" # path of folder where file will move after completion of upload
validProvince=['NewDelhi', 'Lucknow', 'UP', 'Mumbai', 'Keral'] # filtering valid data from csv file
totalRecords=0 # Variables for total records of csv which will use later
smtpServer="<smtpmailserverip>" # smpt mail server ip
smtpPort=<smptport> # smtp port
smtpUser="<emailuserid>"
smtpUserPassword="<emailpassword>"
fromMailID="<emmailuserid>" # mail id of user
toMailId="<receipientaddress>" # enter mail id recepient

##########################################################

Configure below variable in part3.py to run this script.

mysqlConnection={
"host":"<mysqlserverip>",
"user":'<mysqluser>',
"password":'<mysqluserpassword>',
"port":'<mysqlport>',
"database":"<databasewhichcreatedearlier>"
} # mysql connection variables

reportPath=r"C:\temp" # path where report will save
intervalDay=1 # it is require for how many days back report require currently it will fetch report of yesterday
smtpServer="<smtpmailserverip>" # smpt mail server ip
smtpPort=<smptport> # smtp port
smtpUser="<emailuserid>"
smtpUserPassword="<emailpassword>"
fromMailID="<emmailuserid>" # mail id of user
toMailId="<receipientaddress>" # enter mail id recepient
