### Task 1: Unique Launch Sites
**Query:**
```sql
SELECT DISTINCT Launch_Site FROM SPACEXTBL;
```
**Result:**
| Launch_Site   |
|:--------------|
| CCAFS LC-40   |
| VAFB SLC-4E   |
| KSC LC-39A    |
| CCAFS SLC-40  |

### Task 2: Launch Sites Beginning with 'CCA'
**Query:**
```sql
SELECT Launch_Site FROM SPACEXTBL WHERE Launch_Site LIKE 'CCA%' LIMIT 5;
```
**Result:**
| Launch_Site   |
|:--------------|
| CCAFS LC-40   |
| CCAFS LC-40   |
| CCAFS LC-40   |
| CCAFS LC-40   |
| CCAFS LC-40   |

### Task 3: Total Payload Mass Carried by NASA (CRS)
**Query:**
```sql
SELECT SUM(PAYLOAD_MASS__KG_) AS Total_Payload_Mass_KG FROM SPACEXTBL WHERE Customer = 'NASA (CRS)';
```
**Result:**
|   Total_Payload_Mass_KG |
|------------------------:|
|                   45596 |

### Task 4: Average Payload Mass for Booster Version F9 v1.1
**Query:**
```sql
SELECT AVG(PAYLOAD_MASS__KG_) AS Average_Payload_Mass_KG FROM SPACEXTBL WHERE Booster_Version LIKE 'F9 v1.1%';
```
**Result:**
|   Average_Payload_Mass_KG |
|--------------------------:|
|                   2534.67 |

### Task 5: Date of First Successful Ground Pad Landing
**Query:**
```sql
SELECT MIN(Date) AS First_Successful_Ground_Pad_Landing_Date FROM SPACEXTBL WHERE Landing_Outcome = 'Success (ground pad)';
```
**Result:**
| First_Successful_Ground_Pad_Landing_Date   |
|:-------------------------------------------|
| 2015-12-22                                 |

### Task 6: Drone Ship Boosters with Payload between 4000 and 6000 kg
**Query:**
```sql
SELECT Booster_Version, PAYLOAD_MASS__KG_ FROM SPACEXTBL WHERE Landing_Outcome = 'Success (drone ship)' AND PAYLOAD_MASS__KG_ BETWEEN 4000 AND 6000;
```
**Result:**
| Booster_Version   |   PAYLOAD_MASS__KG_ |
|:------------------|--------------------:|
| F9 FT B1022       |                4696 |
| F9 FT B1026       |                4600 |
| F9 FT  B1021.2    |                5300 |
| F9 FT  B1031.2    |                5200 |

### Task 7: Total Successful and Failure Mission Outcomes
**Query:**
```sql
SELECT Mission_Outcome, COUNT(*) AS Total_Count FROM SPACEXTBL GROUP BY Mission_Outcome;
```
**Result:**
| Mission_Outcome                  |   Total_Count |
|:---------------------------------|--------------:|
| Failure (in flight)              |             1 |
| Success                          |            98 |
| Success                          |             1 |
| Success (payload status unclear) |             1 |

### Task 8: Boosters Carrying Maximum Payload Mass
**Query:**
```sql
SELECT Booster_Version, PAYLOAD_MASS__KG_ FROM SPACEXTBL WHERE PAYLOAD_MASS__KG_ = (SELECT MAX(PAYLOAD_MASS__KG_) FROM SPACEXTBL);
```
**Result:**
| Booster_Version   |   PAYLOAD_MASS__KG_ |
|:------------------|--------------------:|
| F9 B5 B1048.4     |               15600 |
| F9 B5 B1049.4     |               15600 |
| F9 B5 B1051.3     |               15600 |
| F9 B5 B1056.4     |               15600 |
| F9 B5 B1048.5     |               15600 |
| F9 B5 B1051.4     |               15600 |
| F9 B5 B1049.5     |               15600 |
| F9 B5 B1060.2     |               15600 |
| F9 B5 B1058.3     |               15600 |
| F9 B5 B1051.6     |               15600 |
| F9 B5 B1060.3     |               15600 |
| F9 B5 B1049.7     |               15600 |

### Task 9: Drone Ship Failures in 2015
**Query:**
```sql
SELECT Booster_Version, Launch_Site, Landing_Outcome, Date FROM SPACEXTBL WHERE Landing_Outcome = 'Failure (drone ship)' AND Date LIKE '%2015%';
```
**Result:**
| Booster_Version   | Launch_Site   | Landing_Outcome      | Date       |
|:------------------|:--------------|:---------------------|:-----------|
| F9 v1.1 B1012     | CCAFS LC-40   | Failure (drone ship) | 2015-01-10 |
| F9 v1.1 B1015     | CCAFS LC-40   | Failure (drone ship) | 2015-04-14 |

### Task 10: Rank Count of Landing Outcomes (2010-06-04 to 2017-03-20)
**Query:**
```sql
SELECT Landing_Outcome, COUNT(*) AS Outcome_Count FROM SPACEXTBL WHERE Date BETWEEN '2010-06-04' AND '2017-03-20' GROUP BY Landing_Outcome ORDER BY Outcome_Count DESC;
```
**Result:**
| Landing_Outcome        |   Outcome_Count |
|:-----------------------|----------------:|
| No attempt             |              10 |
| Success (drone ship)   |               5 |
| Failure (drone ship)   |               5 |
| Success (ground pad)   |               3 |
| Controlled (ocean)     |               3 |
| Uncontrolled (ocean)   |               2 |
| Failure (parachute)    |               2 |
| Precluded (drone ship) |               1 |
