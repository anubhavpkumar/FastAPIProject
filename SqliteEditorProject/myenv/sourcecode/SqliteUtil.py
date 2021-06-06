import sqlite3
import logging

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.DEBUG)

class SqliteUtil:
    def __init__(self, databasePath):
        self.databasePath = databasePath

    def createConnection(self):
        return sqlite3.connect(self.databasePath)

    def executeQuery(self, query):
        con = self.createConnection() 
        cursorObj = con.cursor()
        logging.debug('Executing Query: ' + query)
        queryResponse = cursorObj.execute(query).fetchall()
        con.commit()
        con.close()
        return queryResponse

    def getColumnDefinitionString(self, tableObject):
        columnCreateStatements = []
        for column in tableObject:
            columnCreateStatement = column.columnName + " " + column.columnType + " PRIMARY KEY" if column.isPrimaryKey else ""
            columnCreateStatements.append(columnCreateStatement)
        return "(" + ", ".join(columnCreateStatements) + ');'

    def createTableInDatabase(self, tableName, tableObject):
        columnDefinitionString = getColumnDefinitionString(tableObject)
        tableCreateQuery = "CREATE TABLE " + tableName + columnDefinitionString
        return self.executeQuery(tableCreateQuery)
    
    def convertListItemsToStr(self, listOfItems):
        for items in listOfItems:
            items = str(items.strip())

    def insertRowIntoTable(self, tableName, rowObject):
        columnNames = list(rowObject.keys())
        columnValues = list(rowObject.values())
        self.convertListItemsToStr(columnValues)
        insertStmTableName = "INSERT INTO " + tableName + " "
        insertStmColumnNames = "( " + ", ".join(columnNames) + " )"
        insertStmColumnValues = " VALUES ( \'" + "\', \'".join(columnValues) + "\');"
        insertStatement = insertStmTableName + insertStmColumnNames + insertStmColumnValues
        queryResponse = self.executeQuery(insertStatement)
