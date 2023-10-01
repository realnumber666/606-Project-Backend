

**User Table**

| Field Name        | Data Type | Key         |
| ----------------- | --------- | ----------- |
| UserID            | INT       | Primary Key |
| Username          | VARCHAR   |             |
| Email             | VARCHAR   |             |
| Password Hash     | VARCHAR   |             |
| Registration Date | DATE      |             |

**Transaction Table**

| Field Name    | Data Type | Key         | References                  |
| ------------- | --------- | ----------- | --------------------------- |
| TransactionID | INT       | Primary Key |                             |
| UserID        | INT       | Foreign Key | User Table (UserID)         |
| CategoryID    | INT       | Foreign Key | Category Table (CategoryID) |
| Amount        | DECIMAL   |             |                             |
| Date          | DATE      |             |                             |
| Note          | VARCHAR   |             |                             |

**Category Table**

| Field Name    | Data Type | Key         | References          |
| ------------- | --------- | ----------- | ------------------- |
| CategoryID    | INT       | Primary Key |                     |
| UserID        | INT       | Foreign Key | User Table (UserID) |
| Category Name | VARCHAR   |             |                     |
| Category Type | VARCHAR   |             |                     |

