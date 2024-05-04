# Application Configuration

app.config.from_envvar('YOURAPPLICATION_SETTINGS')
## Bash
$ export OURAPPLICATION_SETTINGS=/path/to/settings.cfg
$ flask run
 * Running on http://127.0.0.1:5000/

## CMD
> set OURAPPLICATION_SETTINGS=\path\to\settings.cfg
> flask run
 * Running on http://127.0.0.1:5000/

## Powershell
> $env:OURAPPLICATION_SETTINGS = "\path\to\settings.cfg"
> flask run
 * Running on http://127.0.0.1:5000/


# Flask WT Forms
intigrity error
form validation


# Models
User
    - sl(autoincrement : int)
    - id(randomly generated 7 digit number : int)
    - First name(str)
    - Last name(str)
    - Email(str)
    - Password(str)
    - Address(str)
    - Next order address(str)
    - Is email verified(boolean)

Product
    - sl(autoincrement : int)
    - id(randomly generated 3 digit number : int)
    - Name(str)
    - Price(float)
    - Description(str)
    - Quantity(int)
    - Category(str)

Cart(Before placing order)
    - CustomerId(Foreign key refering to Users table)
    - ProductId(Foreign key refering to Products table)
    - Quantity(int)

Orderd items:
    - OrderId
    - ProductId(Foreign key refering to Products table)
    - Quantity(int)

Orders
    - OrderId(randomly generate 7 digit number: int)
    - CustomerId(Foreign key refering to the user)
    - Amount paid(float)

    Iam Sandeep







