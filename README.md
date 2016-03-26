# Student wireless access check
## Description


## Setup
Set the SITWIFI_STAFF_USERNAME and SITWIFI_STAFF_PASSWORD environment variables.

Example (note doing it this way will be temporary and will be lost when you log out):

```
export SITWIFI_STAFF_USERNAME=yourusername
export SITWIFI_STAFF_PASSWORD=yourpassword
```

To make it permanent add it to your bashrc file.

## Usage

### Examples
#### Student can access UniWireless

```
>> python check_wireless.py --student-username studentusername
studentusername (studentid) can access UniWireless.
```


#### Student cannot access UniWireless

```
>> python check_wireless.py --student-username studentusername
studentusername (studentid) can not access UniWireless.
```

#### Student doesn't exist

```
>> python check_wireless.py --student-username studentusername
No student with username studentusername exists.
```

