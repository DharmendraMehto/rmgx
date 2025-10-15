# rmgx
Assignment divided into two parts, first part having documented scenario and solution and second part having code using python.
Two folders available in this repo one is for document with the name document and second is code.
Document folder having one doc file having scenario and its solution.
Code folder having python script part2.py it is the solution of part2 requirement of given assignment and part3.py it is the solution of part3 requirement of given assignment.

##########################################################

Below is requirement to run the code:
1) python 3.8.10 installation in windows system
2) install python library which is available in code folder in requirement.txt
3) create database in mysql server.
4) create table and index from below command

CREATE TABLE `shipments` (  `id` bigint NOT NULL AUTO_INCREMENT,  `order_id` varchar(50) DEFAULT NULL,  `carrier_name` varchar(50) DEFAULT NULL,  `ship_date` datetime DEFAULT NULL,  `delivery_date` datetime EFAULT NULL,  `weight` decimal(10,2) DEFAULT NULL,  `origin_province` varchar(20) DEFAULT NULL,  `destination_province` varchar(20) DEFAULT NULL,  `status` varchar(20) DEFAULT NULL,  `cost` decimal(10,2) DEFAULT NULL,  PRIMARY KEY (`id`),  KEY `multi` (`ship_date`,`carrier_name`,`delivery_date`),  KEY `idx_order_id` (`order_id`),  KEY `idx_status_delivery_date` (`status`,`delivery_date`));

###########################################################

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



